from __future__ import annotations

import sys
import multiprocessing
import os
import subprocess
import logging
import asyncio
import nest_asyncio

import sc2

from sc2.main import run_game
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.player import Bot, Difficulty, AbstractPlayer
from worlds.sc2wol.Items import lookup_id_to_name, item_table
from worlds.sc2wol.Locations import SC2WOL_ITEM_ID_OFFSET

from NetUtils import NetworkItem
from Utils import init_logging

if __name__ == "__main__":
    init_logging("SNIClient", exception_logger="Client")

logger = logging.getLogger("Client")

import colorama

from NetUtils import *
import Utils
from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor, gui_enabled, get_base_parser

from MultiServer import mark_raw

nest_asyncio.apply()

class StarcraftClientProcessor(ClientCommandProcessor):
    ctx: Context

    def _cmd_wol(self, wol_options: str = "") -> bool:
        """Start a Starcraft 2 mission"""

        options = wol_options.split()
        num_options = len(options)

        if num_options > 0:
            mission_number = int(options[0])

        asyncio.create_task(starcraft_launch(self.ctx, mission_number), name="SNES Connect")
        return True


class Context(CommonContext):
    command_processor = StarcraftClientProcessor
    game = "Starcraft2WoL"
    items_handling = 0b111
    difficulty = -1
    items_rec_to_announce = []
    rec_announce_pos = 0
    items_sent_to_announce = []
    sent_announce_pos = 0
    announcements = []
    announcement_pos = 0

    def __init__(self, snes_address, server_address, password):
        super(Context, self).__init__(server_address, password)

    async def connection_closed(self):
        await super(Context, self).connection_closed()

    def event_invalid_slot(self):
        if self.snes_socket is not None and not self.snes_socket.closed:
            asyncio.create_task(self.snes_socket.close())
        raise Exception('Invalid ROM detected, '
                        'please verify that you have loaded the correct rom and reconnect your snes (/snes)')

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Context, self).server_auth(password_requested)
        if not self.auth:
            logger.info('Enter slot name:')
            self.auth = await self.console_input()

        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.difficulty = args["slot_data"]["game_difficulty"]
#        if cmd in {"ReceivedItems"}:
#            self.items_rec_to_announce += args["items"]
#        if cmd in {"LocationInfo"}:
#            self.items_sent_to_announce += args["locations"]
        if cmd in {"PrintJSON"}:
            noted = False
            if "receiving" in args:
                if args["receiving"] == self.slot:
                    self.announcements.append(args["data"])
                    noted = True
            if not noted and "item" in args:
                if args["item"].player == self.slot:
                    self.announcements.append(args["data"])


def launch_sni(ctx: Context):
    sni_path = Utils.get_options()["lttp_options"]["sni"]

    if not os.path.isdir(sni_path):
        sni_path = Utils.local_path(sni_path)
    if os.path.isdir(sni_path):
        dir_entry: os.DirEntry
        for dir_entry in os.scandir(sni_path):
            if dir_entry.is_file():
                lower_file = dir_entry.name.lower()
                if (lower_file.startswith("sni.") and not lower_file.endswith(".proto")) or (lower_file == "sni"):
                    sni_path = dir_entry.path
                    break

    if os.path.isfile(sni_path):
        snes_logger.info(f"Attempting to start {sni_path}")
        import sys
        if not sys.stdout:  # if it spawns a visible console, may as well populate it
            subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path))
        else:
            subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path), stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
    else:
        snes_logger.info(
            f"Attempt to start SNI was aborted as path {sni_path} was not found, "
            f"please start it yourself if it is not running")


async def main():
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('--snes', default='localhost:8080', help='Address of the SNI server.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    ctx = Context(args.snes, args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    input_task = None
    if gui_enabled:
        from kvui import SC2Manager
        ctx.ui = SC2Manager(ctx)
        ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
    else:
        ui_task = None
    if sys.stdin:
        input_task = asyncio.create_task(console_loop(ctx), name="Input")

    await ctx.exit_event.wait()

    ctx.server_address = None
    ctx.snes_reconnect_address = None
    await ctx.shutdown()

    if ui_task:
        await ui_task

    if input_task:
        input_task.cancel()

maps_table = ["traynor01", "traynor02", "traynor03", "thanson01", "thanson02", "thanson03a", "thanson03b", "ttychus01"]


def calculate_items(items):
    unit_unlocks = 0
    armory1_unlocks = 0
    armory2_unlocks = 0
    upgrade_unlocks = 0
    building_unlocks = 0
    merc_unlocks = 0
    lab_unlocks = 0
    protoss_unlock = 0
    minerals = 0
    vespene = 0

    for item in items:
        data = lookup_id_to_name[item.item]

        if item_table[data].type == "Unit":
            unit_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Upgrade":
            upgrade_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Armory 1":
            armory1_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Armory 2":
            armory2_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Building":
            building_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Mercenary":
            merc_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Laboratory":
            lab_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Protoss":
            protoss_unlock += (1 << item_table[data].number)
        elif item_table[data].type == "Minerals":
            minerals += item_table[data].number
        elif item_table[data].type == "Vespene":
            vespene += item_table[data].number

    return [unit_unlocks, upgrade_unlocks, armory1_unlocks, armory2_unlocks, building_unlocks, merc_unlocks,
            lab_unlocks, protoss_unlock, minerals, vespene]


def calc_difficulty(difficulty):
    if difficulty == 0:
        return 'C'
    elif difficulty == 1:
        return 'N'
    elif difficulty == 2:
        return 'H'
    elif difficulty == 3:
        return 'B'

    return 'X'


async def starcraft_launch(ctx: Context, mission_id):
    ctx.rec_announce_pos = len(ctx.items_rec_to_announce)
    ctx.sent_announce_pos = len(ctx.items_sent_to_announce)
    ctx.announcements_pos = len(ctx.announcements)

    run_game(sc2.maps.get(maps_table[mission_id-1]), [
        Bot(Race.Terran, ArchipelagoBot(ctx, mission_id), name="Archipelago")], realtime=True)


class ArchipelagoBot(sc2.bot_ai.BotAI):
    game_running = False
    mission_completed = False
    first_bonus = False
    second_bonus = False
    third_bonus = False
    fourth_bonus = False
    fifth_bonus = False
    sixth_bonus = False
    ctx: Context = None
    mission_id = 0

    can_read_game = False

    last_received_update = 0

    def __init__(self, ctx: Context, mission_id):
        self.ctx = ctx
        self.mission_id = mission_id

        super(ArchipelagoBot, self).__init__()

    async def on_step(self, iteration: int):
        game_state = 0
        if iteration == 0:
            start_items = calculate_items(self.ctx.items_received)
            difficulty = calc_difficulty(self.ctx.difficulty)
            await self.chat_send("ArchipelagoLoad {} {} {} {} {} {} {} {} {} {} {}".format(
                difficulty, start_items[0], start_items[1], start_items[2], start_items[3], start_items[4], start_items[5],
                start_items[6], start_items[7], start_items[8], start_items[9]))
            self.last_received_update = len(self.ctx.items_received)

        else:
            if self.ctx.announcement_pos < len(self.ctx.announcements):
                index = 0
                message = ""
                while index < len(self.ctx.announcements[self.ctx.announcement_pos]):
                    message += self.ctx.announcements[self.ctx.announcement_pos][index]["text"]
                    index += 1

                index = 0
                start_rem_pos = -1
                # Remove unneeded [Color] tags
                while index < len(message):
                    if message[index] == '[':
                        start_rem_pos = index
                        index += 1
                    elif message[index] == ']' and start_rem_pos > -1:
                        temp_msg = ""

                        if start_rem_pos > 0:
                            temp_msg = message[:start_rem_pos]
                        if index < len(message) - 1:
                            temp_msg += message[index+1:]

                        message = temp_msg
                        index += start_rem_pos - index
                        start_rem_pos = -1
                    else:
                        index += 1

                await self.chat_send("SendMessage " + message)
                self.ctx.announcement_pos += 1

            # Archipelago reads the health
            for unit in self.all_own_units():
                if unit.health_max == 38281:
                    game_state = int(38281 - unit.health)
                    can_read_game = True

            if self.last_received_update < len(self.ctx.items_received):
                #for i in range(self.last_received_update, len(self.ctx.items_received))
                #    await self.chat_send("SendMessage Received {}")
                current_items = calculate_items(self.ctx.items_received)
                await self.chat_send("UpdateTech {} {} {} {} {} {} {} {}".format(
                    current_items[0], current_items[1], current_items[2], current_items[3], current_items[4], current_items[5],
                    current_items[6], current_items[7]))
                self.last_received_update = len(self.ctx.items_received)

            if game_state & (1):
                if not self.game_running:
                    print("Archipelago Connected")
                    self.game_running = True

                if can_read_game:
                    if game_state & (1 << 1) and not self.mission_completed:
                        print("Mission Completed")
                        await self.ctx.send_msgs([
                            {"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id]}])
                        self.mission_completed = True

                    if game_state & (1 << 2) and not self.first_bonus:
                        print("1st Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 1]}])
                        self.first_bonus = True

                    if not self.second_bonus and game_state & (1 << 3):
                        print("2nd Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 2]}])
                        self.second_bonus = True

                    if not self.third_bonus and game_state & (1 << 4):
                        print("3rd Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 3]}])
                        self.third_bonus = True

                    if not self.fourth_bonus and game_state & (1 << 5):
                        print("4th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 4]}])
                        self.fourth_bonus = True

                    if not self.fifth_bonus and game_state & (1 << 6):
                        print("5th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 5]}])
                        self.fifth_bonus = True

                    if not self.sixth_bonus and game_state & (1 << 7):
                        print("6th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks', "locations": [SC2WOL_ITEM_ID_OFFSET + 100 * self.mission_id + 6]}])
                        self.sixth_bonus = True

                else:
                    await self.chat_send("LostConnection - Lost connection to game.")


if __name__ == '__main__':
    colorama.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    colorama.deinit()
