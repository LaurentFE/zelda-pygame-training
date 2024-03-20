import sys
import pygame
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
