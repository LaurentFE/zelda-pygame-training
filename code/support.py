import sys
import pygame
import re
import settings as cfg
from csv import reader


def import_csv_layout(path, ignore_non_existing_file=False):
    layout = []
    try:
        with open(path) as file:
            parsed = reader(file, delimiter=',')
            for row in parsed:
                layout.append(list(row))
    except FileNotFoundError:
        if not ignore_non_existing_file:
            print(f'FileNotFoundError: No such file or directory: \'{path}\'', file=sys.stderr)
            pygame.quit()
            sys.exit()

    return layout


def str_to_dict(str_in: str):
    dictionary = {}
    if str_in != "{}":
        dict_entries = str_in[1:-1].split(', ')

        for entry in dict_entries:
            data = entry.split(': ', 1)
            level_id = data[0][1:-1]
            if data[1] == "True" or data[1] == "False":
                dictionary[level_id] = eval(data[1])
            else:
                match_int = re.findall('-?[0-9]+', data[1])
                if match_int and match_int[0] == data[1]:
                    dictionary[level_id] = int(data[1])
                else:
                    dictionary[level_id] = data[1][1:-1]

    return dictionary


def shop_str_to_dict(str_in: str):
    dictionary = {}
    items_dict_regex = "({['a-zA-Z0-9 :,-]+})"
    items_dict_str = re.findall(items_dict_regex, str_in)
    dictionary[cfg.ITEMS_LABEL] = str_to_dict(items_dict_str[0])
    str_in = str_in.replace('{\'' + cfg.ITEMS_LABEL + '\': ' + items_dict_str[0] + ', \'' + cfg.NPC_ID_LABEL
                            + '\': ', '', 1)
    npc_id = int(str_in.split(', ', 1)[0])
    dictionary[cfg.NPC_ID_LABEL] = npc_id
    str_in = str_in.replace(str(npc_id) + ', \'' + cfg.TEXT_LABEL + '\': ', '', 1)
    text = str_in[1:-2]
    text = text.replace('\\n', '\n')
    dictionary[cfg.TEXT_LABEL] = text

    return dictionary


def load_from_save_file(player):
    try:
        with open(cfg.SAVE_FILE_PATH) as file:
            save_data = file.read().splitlines()
            player.current_max_health = int(save_data[0])
            player.health = int(save_data[1])
            player.bombs = int(save_data[2])
            player.keys = int(save_data[3])
            player.money = int(save_data[4])
            player.has_boomerang = eval(save_data[5])
            player.has_bombs = eval(save_data[6])
            player.has_candle = eval(save_data[7])
            player.has_ladder = eval(save_data[8])
            player.has_wood_sword = eval(save_data[9])
            player.itemA = str(save_data[10])
            player.itemB = str(save_data[11])

            secrets_revealed = save_data[12]
            cfg.MAP_SECRETS_REVEALED.clear()
            cfg.MAP_SECRETS_REVEALED = str_to_dict(secrets_revealed)

            map_items = save_data[13][1:-1]
            cfg.MAP_ITEMS.clear()
            subdict_regex = "({'[a-zA-Z0-9 ]+': ((?:True)|(?:False))((, '[a-zA-Z0-9 ]+': ((?:True)|(?:False)))*)})"
            sub_dicts = re.findall(subdict_regex, map_items)
            for entry in sub_dicts:
                key = map_items.split(': ' + entry[0])[0]
                level_id = key[1:-1]
                item_list = entry[0]
                cfg.MAP_ITEMS[level_id] = str_to_dict(item_list)
                map_items = map_items.replace(key + ': ', '', 1)
                map_items = map_items.replace(entry[0], '', 1)
                map_items = map_items.replace(', ', '', 1)

            shop_list = save_data[14][1:-1]
            cfg.SHOPS.clear()
            subdict_regex = "('[a-zA-Z0-9_]+': {'(?:items)': {'[a-zA-Z0-9_ ]+': -*[0-9]+(, '[a-zA-Z0-9_ ]+': [0-9]+)*}, '(?:npc_id)': [0-9]+, '(?:text)': ('|\")[a-zA-z0-9\ ',!.?]+('|\")})"
            sub_dicts = re.findall(subdict_regex, shop_list)
            for entry in sub_dicts:
                split_entry = entry[0].split(': ', 1)
                key = split_entry[0]
                level_id = key[1:-1]
                shop_data = split_entry[1]
                cfg.SHOPS[level_id] = shop_str_to_dict(shop_data)
                shop_list = shop_list.replace(entry[0], '', 1)
                shop_list = shop_list.replace(', ', '', 1)

            monster_killed = save_data[15]
            cfg.MONSTER_KILL_EVENT.clear()
            cfg.MONSTER_KILL_EVENT = str_to_dict(monster_killed)

            decimated_dungeons = save_data[16]
            cfg.DUNGEON_DECIMATION.clear()
            cfg.DUNGEON_DECIMATION = str_to_dict(decimated_dungeons)

            doors = save_data[17][1:-1]
            cfg.DUNGEON_DOORS.clear()
            subdict_regex = "(({})|{'((?:right)|(?:left)|(?:up)|(?:down))': '[a-zA-Z ]+'(, '((?:right)|(?:left)|(?:up)(?:down))': '[a-zA-Z ]+')*})"
            sub_dicts = re.findall(subdict_regex, doors)
            for entry in sub_dicts:
                key = doors.split(': ' + entry[0])[0]
                level_id = key[1: -1]
                door_list = entry[0]
                cfg.DUNGEON_DOORS[level_id] = str_to_dict(door_list)
                doors = doors.replace(key + ': ', '', 1)
                doors = doors.replace(entry[0], '', 1)
                doors = doors.replace(', ', '', 1)

        file.close()
    except OSError as error:
        raise OSError(error)


def save_to_file(player):
    try:
        with open(cfg.SAVE_FILE_PATH, "w") as file:
            save_content = (f'{player.current_max_health}\n'
                            + f'{player.health}\n'
                            + f'{player.bombs}\n'
                            + f'{player.keys}\n'
                            + f'{player.money}\n'
                            + f'{player.has_boomerang}\n'
                            + f'{player.has_bombs}\n'
                            + f'{player.has_candle}\n'
                            + f'{player.has_ladder}\n'
                            + f'{player.has_wood_sword}\n'
                            + f'{player.itemA}\n'
                            + f'{player.itemB}\n'
                            + f'{cfg.MAP_SECRETS_REVEALED}\n'
                            + f'{cfg.MAP_ITEMS}\n'
                            + f'{cfg.SHOPS}\n'
                            + f'{cfg.MONSTER_KILL_EVENT}\n'
                            + f'{cfg.DUNGEON_DECIMATION}\n'
                            + f'{cfg.DUNGEON_DOORS}\n')
            file.write(save_content)
            file.close()
    except OSError as error:
        raise OSError(error)
