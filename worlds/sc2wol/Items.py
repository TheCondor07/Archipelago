from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: typing.Optional[str]
    number: typing.Optional[int]
    slot: str
    classification: ItemClassification = ItemClassification.filler
    quantity: int = 1


class StarcraftWoLItem(Item):
    game: str = "Starcraft 2 Wings of Liberty"


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000

item_table = {
    "Marine": ItemData(0 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, "Barracks Unit", classification=ItemClassification.progression),
    "Medic": ItemData(1 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, "Barracks Unit", classification=ItemClassification.progression),
    "Firebat": ItemData(2 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, "Barracks Unit", classification=ItemClassification.progression),
    "Marauder": ItemData(3 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, "Barracks Unit", classification=ItemClassification.progression),
    "Reaper": ItemData(4 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, "Barracks Unit", classification=ItemClassification.progression),
    "Hellion": ItemData(5 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, "Factory Unit", classification=ItemClassification.progression),
    "Vulture": ItemData(6 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, "Factory Unit", classification=ItemClassification.progression),
    "Goliath": ItemData(7 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, "Factory Unit", classification=ItemClassification.progression),
    "Diamondback": ItemData(8 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, "Factory Unit", classification=ItemClassification.progression),
    "Siege Tank": ItemData(9 + SC2WOL_ITEM_ID_OFFSET, "Unit", 9, "Factory Unit", classification=ItemClassification.progression),
    "Medivac": ItemData(10 + SC2WOL_ITEM_ID_OFFSET, "Unit", 10, "Starport Unit", classification=ItemClassification.progression),
    "Wraith": ItemData(11 + SC2WOL_ITEM_ID_OFFSET, "Unit", 11, "Starport Unit", classification=ItemClassification.progression),
    "Viking": ItemData(12 + SC2WOL_ITEM_ID_OFFSET, "Unit", 12, "Starport Unit", classification=ItemClassification.progression),
    "Banshee": ItemData(13 + SC2WOL_ITEM_ID_OFFSET, "Unit", 13, "Starport Unit", classification=ItemClassification.progression),
    "Battlecruiser": ItemData(14 + SC2WOL_ITEM_ID_OFFSET, "Unit", 14, "Starport Unit", classification=ItemClassification.progression),
    "Ghost": ItemData(15 + SC2WOL_ITEM_ID_OFFSET, "Unit", 15, "Barracks Unit", classification=ItemClassification.progression),
    "Spectre": ItemData(16 + SC2WOL_ITEM_ID_OFFSET, "Unit", 16, "Barracks Unit", classification=ItemClassification.progression),
    "Thor": ItemData(17 + SC2WOL_ITEM_ID_OFFSET, "Unit", 17, "Factory Unit", classification=ItemClassification.progression),

    "Progressive Infantry Weapon": ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, "Progressive Infantry Weapon", quantity=3),
    "Progressive Infantry Armor": ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, "Progressive Infantry Weapon", quantity=3),
    "Progressive Vehicle Weapon": ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, "Progressive Infantry Weapon", quantity=3),
    "Progressive Vehicle Armor": ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, "Progressive Infantry Weapon", quantity=3),
    "Progressive Ship Weapon": ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, "Progressive Infantry Weapon", quantity=3),
    "Progressive Ship Armor": ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, "Progressive Infantry Weapon", quantity=3),

    "Projectile Accelerator (Bunker)": ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, "Armory"),
    "Neosteel Bunker (Bunker)": ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, "Armory"),
    "Titanium Housing (Missile Turret)": ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, "Armory"),
    "Hellstorm Batteries (Missile Turret)": ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, "Armory"),
    "Advanced Construction (SCV)": ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4, "Armory"),
    "Dual-Fusion Welders (SCV)": ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5, "Armory"),
    "Fire-Suppression System (Building)": ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6, "Armory"),
    "Orbital Command (Building)": ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7, "Armory"),
    "Stimpack (Marine)": ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, "Armory"),
    "Combat Shield (Marine)": ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, "Armory"),
    "Advanced Medic Facilities (Medic)": ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, "Armory"),
    "Stabilizer Medpacks (Medic)": ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, "Armory"),
    "Incinerator Gauntlets (Firebat)": ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, "Armory", classification=ItemClassification.useful),
    "Juggernaut Plating (Firebat)": ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, "Armory"),
    "Concussive Shells (Marauder)": ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, "Armory"),
    "Kinetic Foam (Marauder)": ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, "Armory"),
    "U-238 Rounds (Reaper)": ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, "Armory"),
    "G-4 Clusterbomb (Reaper)": ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, "Armory", classification=ItemClassification.useful),

    "Twin-Linked Flamethrower (Hellion)": ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, "Armory", classification=ItemClassification.useful),
    "Thermite Filaments (Hellion)": ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, "Armory"),
    "Cerberus Mine (Vulture)": ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, "Armory"),
    "Replenishable Magazine (Vulture)": ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3, "Armory"),
    "Multi-Lock Weapons System (Goliath)": ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4, "Armory"),
    "Ares-Class Targeting System (Goliath)": ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5, "Armory"),
    "Tri-Lithium Power Cell (Diamondback)": ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, "Armory", classification=ItemClassification.useful),
    "Shaped Hull (Diamondback)": ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, "Armory", classification=ItemClassification.useful),
    "Maelstrom Rounds (Siege Tank)": ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8, "Armory"),
    "Shaped Blast (Siege Tank)": ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9, "Armory"),
    "Rapid Deployment Tube (Medivac)": ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, "Armory", classification=ItemClassification.useful),
    "Advanced Healing AI (Medivac)": ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11, "Armory"),
    "Tomahawk Power Cells (Wraith)": ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, "Armory", classification=ItemClassification.useful),
    "Displacement Field (Wraith)": ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13, "Armory"),
    "Ripwave Missiles (Viking)": ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14, "Armory"),
    "Phobos-Class Weapons System (Viking)": ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15, "Armory"),
    "Cross-Spectrum Dampeners (Banshee)": ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 16, "Armory", classification=ItemClassification.useful),
    "Shockwave Missile Battery (Banshee)": ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, "Armory"),
    "Missile Pods (Battlecruiser)": ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, "Armory", classification=ItemClassification.useful),
    "Defensive Matrix (Battlecruiser)": ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, "Armory", classification=ItemClassification.useful),
    "Ocular Implants (Ghost)": ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, "Armory"),
    "Crius Suit (Ghost)": ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, "Armory"),
    "Psionic Lash (Spectre)": ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, "Armory"),
    "Nyx-Class Cloaking Module (Spectre)": ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, "Armory"),
    "330mm Barrage Cannon (Thor)": ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, "Armory", classification=ItemClassification.useful),
    "Immortality Protocol (Thor)": ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, "Armory", classification=ItemClassification.useful),

    "Bunker": ItemData(400 + SC2WOL_ITEM_ID_OFFSET, "Building", 0, "Building", classification=ItemClassification.progression),
    "Missile Turret": ItemData(401 + SC2WOL_ITEM_ID_OFFSET, "Building", 1, "Building", classification=ItemClassification.progression),
    "Sensor Tower": ItemData(402 + SC2WOL_ITEM_ID_OFFSET, "Building", 2, "Building"),

    "War Pigs": ItemData(500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0, "Mercenary"),
    "Devil Dogs": ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, "Mercenary", classification=ItemClassification.useful),
    "Hammer Securities": ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2, "Mercenary"),
    "Spartan Company": ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3, "Mercenary"),
    "Siege Breakers": ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4, "Mercenary"),
    "Hel's Angel": ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5, "Mercenary"),
    "Dusk Wings": ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6, "Mercenary"),
    "Jackson's Revenge": ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7, "Mercenary"),

    "Ultra-Capacitors": ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0, "Laboratory P1"),
    "Vanadium Plating": ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1, "Laboratory P1"),
    "Orbital Depots": ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2, "Laboratory P2"),
    "Micro-Filtering": ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3, "Laboratory P2"),
    "Automated Refinery": ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4, "Laboratory P3"),
    "Command Center Reactor": ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5, "Laboratory P3"),
    "Raven": ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6, "Laboratory P4"),
    "Science Vessel": ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, "Laboratory P4", classification=ItemClassification.progression),
    "Tech Reactor": ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8, "Laboratory P5"),
    "Orbital Strike": ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9, "Laboratory P5"),
    "Shrike Turret": ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, "Laboratory Z1"),
    "Fortified Bunker": ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, "Laboratory Z1"),
    "Planetary Fortress": ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, "Laboratory Z2"),
    "Perdition Turret": ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 13, "Laboratory Z2"),
    "Predator": ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 14, "Laboratory Z3", classification=ItemClassification.useful),
    "Hercules": ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 15, "Laboratory Z3", classification=ItemClassification.progression),
    "Cellular Reactor": ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 16, "Laboratory Z4", classification=ItemClassification.useful),
    "Regenerative Bio-Steel": ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 17, "Laboratory Z4", classification=ItemClassification.useful),
    "Hive Mind Emulator": ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 18, "Laboratory Z5"),
    "Psi Disrupter": ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 19, "Laboratory Z5", classification=ItemClassification.useful),

    "Zealot": ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 0, "Protoss", classification=ItemClassification.progression),
    "Stalker": ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 1, "Protoss", classification=ItemClassification.progression),
    "High Templar": ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 2, "Protoss", classification=ItemClassification.progression),
    "Dark Templar": ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 3, "Protoss", classification=ItemClassification.progression),
    "Immortal": ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 4, "Protoss", classification=ItemClassification.progression),
    "Colossus": ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 5, "Protoss", classification=ItemClassification.progression),
    "Phoenix": ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 6, "Protoss", classification=ItemClassification.progression),
    "Void Ray": ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 7, "Protoss", classification=ItemClassification.progression),
    "Carrier": ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 8, "Protoss", classification=ItemClassification.progression),

    "+15 Starting Minerals": ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, "Filler", quantity=0),
    "+15 Starting Vespene": ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, "Filler", quantity=0),
    "+2 Starting Supply": ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, "Filler", quantity=0),
}

basic_unit: typing.Tuple[str, ...] = (
    'Marine',
    'Marauder',
    'Firebat',
    'Hellion',
    'Vulture'
)

item_name_groups = {}
for item, data in item_table.items():
    item_name_groups.setdefault(data.type, []).append(item)
item_name_groups["Missions"] = ["Beat Liberation Day", "Beat The Outlaws", "Beat Zero Hour", "Beat Evacuation",
                         "Beat Outbreak", "Beat Safe Haven", "Beat Haven's Fall", "Beat Smash and Grab", "Beat The Dig",
                         "Beat The Moebius Factor", "Beat Supernova", "Beat Maw of the Void", "Beat Devil's Playground",
                         "Beat Welcome to the Jungle", "Beat Breakout", "Beat Ghost of a Chance",
                         "Beat The Great Train Robbery", "Beat Cutthroat", "Beat Engine of Destruction",
                         "Beat Media Blitz", "Beat Piercing the Shroud"]

filler_items: typing.Tuple[str, ...] = (
    '+15 Starting Minerals',
    '+15 Starting Vespene'
)

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}
