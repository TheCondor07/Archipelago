import random
import typing

from typing import List, Set, Tuple, Dict
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import StarcraftWoLItem, item_table, filler_items, item_name_groups, get_full_item_list, \
    get_basic_units
from .Locations import get_locations
from .Regions import create_regions
from .Options import sc2wol_options, get_option_value, get_option_set_value
from .LogicMixin import SC2WoLLogic
from .PoolFilter import filter_missions, filter_items, get_item_upgrades
from .MissionTables import get_starting_mission_locations, MissionInfo


class Starcraft2WoLWebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor"]
    )

    tutorials = [setup]


class SC2WoLWorld(World):
    """
    StarCraft II: Wings of Liberty is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Command Raynor's Raiders in collecting pieces of the Keystone in order to stop the zerg threat posed by the Queen of Blades.
    """

    game = "Starcraft 2 Wings of Liberty"
    web = Starcraft2WoLWebWorld()
    data_version = 4

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    option_definitions = sc2wol_options

    item_name_groups = item_name_groups
    locked_locations: typing.List[str]
    location_cache: typing.List[Location]
    mission_req_table = {}
    final_mission_id: int
    victory_item: str
    required_client_version = 0, 3, 6

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2WoLWorld, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftWoLItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.mission_req_table, self.final_mission_id, self.victory_item = create_regions(
            self.multiworld, self.player, get_locations(self.multiworld, self.player), self.location_cache
        )

    def generate_basic(self):
        excluded_items = get_excluded_items(self.multiworld, self.player)

        starter_items = assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)

        pool = get_item_pool(self.multiworld, self.player, self.mission_req_table, starter_items, excluded_items, self.location_cache)

        fill_item_pool_with_dummy_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.victory_item, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in sc2wol_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        slot_req_table = {}
        for mission in self.mission_req_table:
            slot_req_table[mission] = self.mission_req_table[mission]._asdict()

        slot_data["mission_req"] = slot_req_table
        slot_data["final_mission"] = self.final_mission_id
        return slot_data


def setup_events(player: int, locked_locations: typing.List[str], location_cache: typing.List[Location]):
    for location in location_cache:
        if location.address is None:
            item = Item(location.name, ItemClassification.progression, None, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_excluded_items(multiworld: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    # Exclude modded items if not using them
    if not get_option_value(multiworld, player, "modded_unlocks"):
        for name, data in item_table.items():
            if data.type == "Extras":
                excluded_items.add(name)

    for item in multiworld.precollected_items[player]:
        excluded_items.add(item.name)

    excluded_items_option = getattr(multiworld, 'excluded_items', [])

    excluded_items.update(excluded_items_option[player].value)

    packages = {}
    yaml_locked_items = get_option_set_value(multiworld, player, 'locked_items')

    for name, data in item_table.items():
        if data.package and name not in excluded_items:
            if data.package in packages:
                packages[data.package].append(name)
            else:
                packages[data.package] = [name]


    if get_option_value(multiworld, player, "more_laboratory_research"):
        max_lab_choices = 2
    else:
        max_lab_choices = 1

    # A package is category of unlocks that can only have a max amount in the item pool at once
    for package in packages:
        if package.startswith("Protoss Tier") or package.startswith("Zerg Tier"):
            max_choices = max_lab_choices
        else:
            # Currently all packages that can be replaced that isn't lab requires 2, if this changes will need to redo
            max_choices = 2

        choices = []

        # check to see if any items are locked
        for item in packages[package]:
            if item in yaml_locked_items:
                choices.append(item)
                packages[package].remove(item)

        while len(choices) < max_choices and len(packages[package]) > 0:
            item = random.choice(packages[package])
            packages[package].remove(item)

            valid_choice = True

            for restriction in item_table[item].restrictions:
                if restriction in choices:
                    valid_choice = False

            for check_item in choices:
                if item in item_table[check_item].restrictions:
                    valid_choice = False

            if valid_choice:
                choices.append(item)
            else:
                excluded_items.add(item)

        for item in packages[package]:
            excluded_items.add(item)

    return excluded_items


def assign_starter_items(multiworld: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]) -> List[Item]:
    non_local_items = multiworld.non_local_items[player].value
    if get_option_value(multiworld, player, "early_unit"):
        local_basic_unit = sorted(item for item in get_basic_units(multiworld, player) if item not in non_local_items and item not in excluded_items)
        if not local_basic_unit:
            raise Exception("At least one basic unit must be local")

        # The first world should also be the starting world
        first_mission = list(multiworld.worlds[player].mission_req_table)[0]
        starting_mission_locations = get_starting_mission_locations(multiworld, player)
        if first_mission in starting_mission_locations:
            first_location = starting_mission_locations[first_mission]
        elif first_mission == "In Utter Darkness":
            first_location = first_mission + ": Defeat"
        else:
            first_location = first_mission + ": Victory"

        return [assign_starter_item(multiworld, player, excluded_items, locked_locations, first_location, local_basic_unit)]
    else:
        return []


def assign_starter_item(multiworld: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str],
                        location: str, item_list: Tuple[str, ...]) -> Item:

    item_name = multiworld.random.choice(item_list)

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(player, item_name)

    multiworld.get_location(location, player).place_locked_item(item)

    locked_locations.append(location)

    return item


def get_item_pool(multiworld: MultiWorld, player: int, mission_req_table: Dict[str, MissionInfo],
                  starter_items: List[str], excluded_items: Set[str], location_cache: List[Location]) -> List[Item]:
    pool: List[Item] = []

    # For the future: goal items like Artifact Shards go here
    locked_items = []

    # YAML items
    yaml_locked_items = get_option_set_value(multiworld, player, 'locked_items')

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.quantity):
                item = create_item_with_correct_settings(player, name)
                if name in yaml_locked_items:
                    locked_items.append(item)
                else:
                    pool.append(item)

    existing_items = starter_items + [item for item in multiworld.precollected_items[player]]
    existing_names = [item.name for item in existing_items]
    # Removing upgrades for excluded items
    for item_name in excluded_items:
        if item_name in existing_names:
            continue
        invalid_upgrades = get_item_upgrades(pool, item_name)
        for invalid_upgrade in invalid_upgrades:
            pool.remove(invalid_upgrade)

    filtered_pool = filter_items(multiworld, player, mission_req_table, location_cache, pool, existing_items, locked_items)
    return filtered_pool


def fill_item_pool_with_dummy_items(self: SC2WoLWorld, multiworld: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = item_table[name]

    item = Item(name, data.classification, data.code, player)

    return item
