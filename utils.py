# Imports.
# Local imports.
from player import Player

# Externals imports.
import copy
import hashlib
from itertools import zip_longest, cycle
import numpy as np
import os
import pickle
from PIL import Image
import platform
import sys
import time


# Assign a value to a key of a dict.
def assign_value_dict(dictionary: dict, keys: list, value) -> dict:
    current_dict = dictionary

    # Traverse the dictionary using keys[:-1] to reach the nested dictionary.
    for key in keys[:-1]:
        current_dict = current_dict[key]

    # Assign the value to the last key in the list.
    current_dict[keys[-1]] = value

    # Return the original dictionary (which is now updated).
    return dictionary


# Validation of name.
def check_name(text: str, max_length: int = 12):
    # Check if text is empty.
    if not text:
        return False

    # Check text length, white space, and numbers.
    if len(text) > max_length or text.isspace() or any(char.isdigit() for char in text):
        return False

    # If it passes all checks, return True
    return True


# Clear console function.
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Coast reset.
def reset_map(ms: dict, keys: list) -> dict:
    ms[keys[0]].description = "Seaside with anchored boat, echoing waves and vibrant coastal life."
    ms[keys[0]].items = ["boat"]

    ms[keys[1]].description = "Seaside with anchored boat, echoing waves and vibrant coastal life."
    ms[keys[1]].items = ["boat"]


# Function that concatenates two lists of str elements.
def concatenate_lists(list1: list[str], list2: list[str]) -> list[str]:
    concatenated_list = ["".join(pair) for pair in zip_longest(list1, list2, fillvalue="")]
    return concatenated_list


# Function that turns a tuple of to int elements to a string, for coord usages in map_set.
def coordstr(x: int, y: int):
    return str(tuple([x, y]))


# Count spaces at first of a text.
def count_first_spaces(string: str) -> int:
    # Initialize a counter to keep track of the number of spaces
    count = 0
    # Iterate through each character in the input string
    for char in string:
        # Check if the character is a whitespace character
        if char.isspace():
            # Increment the counter if it's a space
            count += 1
        else:
            # Exit the loop when a non-space character is encountered
            break

    # Return the final count of spaces at the beginning of the string
    return count


# Functions that simplifies moving options.
def draw_move(x: int, y: int, map_height: int, map_width: int, player: Player, tl_map: list, ms: dict) -> list:
    inventory = player.inventory.items
    events = [*player.events.keys()]
    active_moves = [0, 0, 0, 0]
    if player.outside:
        if y > 0 and all(req in [*inventory.keys()] + events for req in ms[coordstr(x, y - 1)].req) and player.status in ms[coordstr(x, y - 1)].status:
            if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
                active_moves[0] = 1

        if x < map_height and all(req in [*inventory.keys()] + events for req in ms[coordstr(x + 1, y)].req) and player.status in ms[coordstr(x + 1, y)].status:
            if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
                active_moves[1] = 1

        if y < map_width and all(req in [*inventory.keys()] + events for req in ms[coordstr(x, y + 1)].req) and player.status in ms[coordstr(x, y + 1)].status:
            if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
                active_moves[2] = 1

        if x > 0 and all(req in [*inventory.keys()] + events for req in ms[coordstr(x - 1, y)].req) and player.status in ms[coordstr(x - 1, y)].status:
            if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
                active_moves[3] = 1

    return active_moves


# Export dictionary to txt.
def export_dict_to_txt(dictionary: dict, file_path: str) -> None:
    def write_recursive(file, data, depth=0):
        for key, value in data.items():
            if isinstance(value, dict):
                file.write(f"{'  ' * depth}{key}:\n")
                write_recursive(file, value, depth + 1)
            else:
                file.write(f"{'  ' * depth}{key}: {value}\n")

    try:
        with open(file_path, 'w') as doc:
            write_recursive(doc, dictionary)
    except OSError:
        print("Unable to save the file.")
        input(" > ")


# Export player function.
def export_player(player: object, path: str) -> None:
    with open(path, 'wb') as file:
        pickle.dump(player, file)


# Export player function.
def export_settings(setting: object, path: str) -> None:
    with open(path, 'wb') as file:
        pickle.dump(setting, file)


def find_full_name(partial_name: str, names_list: list) -> str | None:
    matching_names = [name for name in names_list if partial_name.lower() in name.lower()]

    if len(matching_names) != 1:
        return None

    return matching_names[0]


# Hash generator of txt file.
def get_hash(file_name, algorithm='sha256', block_size=65536):
    hasher = hashlib.new(algorithm)
    with open(file_name, 'rb') as file:
        block = file.read(block_size)
        while len(block) > 0:
            hasher.update(block)
            block = file.read(block_size)
    return hasher.hexdigest()


# Get label from pixel function.
def get_label(x: int, y: int, matrix: np.array) -> str:
    color = tuple(matrix[y, x])

    # Get the color of the pixel at coordinates (x, y)
    if color == (180, 110, 60, 255):  # Building.
        label = "building"
    elif color == (54, 54, 54, 255):  # Canyon.
        label = "canyon"
    elif color == (1, 1, 1, 255):  # Cave.
        label = "cave"
    elif color == (239, 228, 176, 255):  # Coast.
        label = "coast"
    elif color == (22, 118, 51, 255):  # Dark Forest.
        label = "dark forest"
    elif color == (148, 148, 148, 255):  # Death Valley.
        label = "death valley"
    elif color == (115, 231, 29, 255):  # Fields.
        label = "fields"
    elif color == (34, 177, 76, 255):  # Forest.
        label = "forest"
    elif color == (120, 186, 252, 255):  # Frostvale.
        label = "frostvale"
    elif color == (200, 191, 231, 255):  # Gates.
        label = "gates"
    elif color == (195, 195, 195, 255):  # Highlands.
        label = "highlands"
    elif color == (78, 185, 32, 255):  # Hills.
        label = "hills"
    elif color == (185, 122, 87, 255):  # Hut.
        label = "hut"
    elif color == (201, 237, 92, 255):  # Island.
        label = "island"
    elif color == (127, 127, 127, 255):  # Mountains.
        label = "mountains"
    elif color == (181, 230, 29, 255):  # Plains.
        label = "plains"
    elif color == (82, 249, 11, 255):  # Plateau.
        label = "plateau"
    elif color == (255, 0, 0, 255):  # Red.
        label = "red"
    elif color == (0, 162, 232, 255):  # River.
        label = "river"
    elif color == (85, 80, 85, 255):  # Rocks.
        label = "rocks"
    elif color == (63, 72, 204, 255):  # Sea.
        label = "sea"
    elif color == (250, 250, 250, 255):  # Snow.
        label = "snow"
    elif color == (170, 105, 70, 255):  # Town.
        label = "town"
    elif color == (167, 167, 167, 255):  # Valley.
        label = "valley"
    elif color == (128, 255, 255, 255):  # Water.
        label = "water"
    elif color == (0, 0, 0, 255):  # Unexplored.
        label = "unexplored"
    else:
        label = "red"

    return label


# Import player function.
def import_player(path: str):
    with open(path, 'rb') as archivo:
        return pickle.load(archivo)


# Import settings function.
def import_settings(path: str):
    with open(path, 'rb') as archivo:
        return pickle.load(archivo)


# Functions that returns tile map of a image, depending de colors.
def label_pixels(img_path: str) -> list:
    # Open the image.
    img = Image.open(img_path, mode="r")

    # Get the dimensions of the image
    width, height = img.size

    # Create a list to store pixel tile_map.
    tl_map = []

    # Iterate through each pixel in the image.
    for y in range(height):
        img_row = []
        for x in range(width):
            # Get the color of the pixel at coordinates (x, y)
            color = img.getpixel((x, y))
            if color == (180, 110, 60, 255):  # Building.
                label = "building"
            elif color == (54, 54, 54, 255):  # Canyon.
                label = "canyon"
            elif color == (1, 1, 1, 255):  # Cave.
                label = "cave"
            elif color == (239, 228, 176, 255):  # Coast.
                label = "coast"
            elif color == (22, 118, 51, 255):  # Dark Forest.
                label = "dark forest"
            elif color == (148, 148, 148, 255):  # Death Valley.
                label = "death valley"
            elif color == (115, 231, 29, 255):  # Fields.
                label = "fields"
            elif color == (34, 177, 76, 255):  # Forest.
                label = "forest"
            elif color == (120, 186, 252, 255):  # Frostvale.
                label = "frostvale"
            elif color == (200, 191, 231, 255):  # Gates.
                label = "gates"
            elif color == (195, 195, 195, 255):  # Highlands.
                label = "highlands"
            elif color == (78, 185, 32, 255):  # Hills.
                label = "hills"
            elif color == (185, 122, 87, 255):  # Hut.
                label = "hut"
            elif color == (201, 237, 92, 255):  # Island.
                label = "island"
            elif color == (127, 127, 127, 255):  # Mountains.
                label = "mountains"
            elif color == (181, 230, 29, 255):  # Plains.
                label = "plains"
            elif color == (82, 249, 11, 255):  # Plateau.
                label = "plateau"
            elif color == (255, 0, 0, 255):  # Red.
                label = "red"
            elif color == (0, 162, 232, 255):  # River.
                label = "river"
            elif color == (85, 80, 85, 255):  # Rocks.
                label = "rocks"
            elif color == (63, 72, 204, 255):  # Sea.
                label = "sea"
            elif color == (250, 250, 250, 255):  # Snow.
                label = "snow"
            elif color == (170, 105, 70, 255):  # Town.
                label = "town"
            elif color == (167, 167, 167, 255):  # Valley.
                label = "valley"
            elif color == (128, 255, 255, 255):  # Water.
                label = "water"
            else:
                label = "red"

            # Assign a label based on the color.
            img_row.append(label)

        tl_map.append(img_row)

    return tl_map


# Import dictionary from txt.
def load_dict_from_txt(file_path: str) -> dict:
    reloaded_dictionary = {}
    current_key = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i != 0 and count_first_spaces(lines[i]) < count_first_spaces(lines[i - 1]):
                current_key.pop(-1)
            key, value = line.strip().split(':', 1)
            if value == '':
                current_key.append(key)
                reloaded_dictionary = assign_value_dict(reloaded_dictionary, current_key, {})
            else:
                try:
                    value = eval(value)
                except SyntaxError:
                    value = value.strip()
                except NameError:
                    value = value.strip()
                current_key.append(key)
                reloaded_dictionary = assign_value_dict(reloaded_dictionary, current_key, value)
                current_key.pop(-1)

    return reloaded_dictionary


# Load settings functions.
def load_map_set(ms: dict, setting: dict):
    for i, ii in zip(ms.values(), setting.values()):
        i.__dict__.update(ii.__dict__)


# Print patron in column function.
def patron_print(elements, n):
    patron = []
    elements_cycle = cycle(elements)
    for _ in range(n):
        patron.append(next(elements_cycle))
    return patron


# Function that left justify a text.
def text_ljust(msg: str, width: int = 20, adjust: bool = True) -> list:
    lines = msg.split('\n')
    text = []

    if adjust:
        for line in lines:
            words = line.split()
            current_line = words[0]

            for word in words[1:]:
                if len(current_line) + len(word) + 1 <= width:
                    # Add word to text line.
                    current_line += ' ' + word
                else:
                    # Justify the current line and start a new text line.
                    text.append(current_line.ljust(width))
                    current_line = word

            # Justify the last text line in the current paragraph.
            text.append(current_line.ljust(width))
    else:
        for line in lines:
            text.append(line.ljust(width))
    return text


# Function that puts two messages in two paralels columns.
def text_2_col(msg1: str, msg2: str, width: int = 20, ch: str = "", adjust: bool = True) -> list:
    lines1 = text_ljust(msg1, width, adjust)
    lines2 = text_ljust(msg2, width, adjust)

    max_lines = max(len(lines1), len(lines2))

    lines1 += [" " * width] * (max_lines - len(lines1))
    lines2 += [" " * width] * (max_lines - len(lines2))

    return [t1 + " " + str(ch) + " " + t2 for t1, t2 in zip(lines1, lines2)]


# Functions that returns coordinates as text separete by comma.
def text_coord(x, y) -> str:
    return str(x) + "," + str(y)


# Function that returns a dictionary from a list generated with label_pixels.
def tl_map_set(tl_map: list, biomes: dict) -> dict:
    # Create empty dict.
    dictionary = {}

    # Fill the dictionary
    for i in range(len(tl_map)):
        for j in range(len(tl_map[i])):
            key = coordstr(j, i)
            value = copy.deepcopy(biomes[tl_map[i][j]])
            dictionary[key] = value

    return dictionary


# Typewriter function.
def typewriter(text: str, speed: float = 0.01) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
