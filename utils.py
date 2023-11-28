# Imports.
from PIL import Image
from itertools import zip_longest, cycle
import globals
import time
import sys
import os


# Clear console function.
def clear():
    os.system("cls")


# Functions that returns tile map of a image, depending de colors.
def label_pixels(img_path: str):
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
            if color == (1, 1, 1, 255):  # Cave.
                label = "cave"
            elif color == (239, 228, 176, 255):  # Coast.
                label = "coast"
            elif color == (34, 177, 76, 255):  # Forest.
                label = "forest"
            elif color == (200, 191, 231, 255):  # Gates.
                label = "gates"
            elif color == (195, 195, 195, 255):  # Highlands.
                label = "highlands"
            elif color == (185, 122, 87, 255):  # Elina's Hut.
                label = "hut"
            elif color == (201, 237, 92, 255):  # Island.
                label = "island"
            elif color == (127, 127, 127, 255):  # Mountains.
                label = "mountains"
            elif color == (181, 230, 29, 255):  # Plains.
                label = "plains"
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
            elif color == (163, 73, 164, 255):  # Workers.
                label = "workers"
            else:
                label = "red"

            # Assign a label based on the color.
            img_row.append(label)

        tl_map.append(img_row)

    return tl_map


# Function that returns a dictionary from a list generated with label_pixels.
def tl_map_set(tl_map: list):
    # Create empety dict.
    dictionary = {}

    # Fill the dictionary
    for i in range(len(tl_map)):
        for j in range(len(tl_map[i])):
            key = str((i, j))
            value = {
                    "t": None,
                    "e": False,
                    "e_list": [],
                    "e_chance": [],
                    "r": [],
                    "d": None,
                    "items": [],
                    "npc": [],
                    "entries": [],
                    "c": None}
            dictionary[key] = value

    return dictionary


# Functions that simplifies moving options.
def draw_move(x, y, map_heigt, map_width, inventory, tl_map) -> list:
    active_moves = [0, 0, 0, 0]
    if y > 0 and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y - 1][x]]["r"]):
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            active_moves[0] = 1

    if x < map_heigt and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y][x + 1]]["r"]):
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            active_moves[1] = 1

    if y < map_width and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y + 1][x]]["r"]):
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            active_moves[2] = 1

    if x > 0 and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y][x - 1]]["r"]):
        if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
            active_moves[3] = 1

    return active_moves


# Function that left justify a text.
def text_ljust(msg: str, width: int = 20) -> list:
    lines = msg.split('\n')
    text = []

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

    return text


# Function that puts two messages in two paralels columns.
def text_2_col(msg1: str, msg2: str, width: int = 20, ch: str = "") -> list:
    lines1 = text_ljust(msg1, width)
    lines2 = text_ljust(msg2, width)

    max_lines = max(len(lines1), len(lines2))

    lines1 += [" " * width] * (max_lines - len(lines1))
    lines2 += [" " * width] * (max_lines - len(lines2))

    return [t1 + " " + str(ch) + " " + t2 for t1, t2 in zip(lines1, lines2)]


# Function that concatenates two lists of str elements.
def concatenate_lists(list1: list[str], list2: list[str]) -> list[str]:
    concatenated_list = ["".join(pair) for pair in zip_longest(list1, list2, fillvalue="")]
    return concatenated_list


# Functions that returns coordinates as text separete by comma.
def text_coord(x, y) -> str:
    return str(x) + "," + str(y)


# Function that calculates the part of the day.
def day_est(actual_hs: int, add_hs: int) -> tuple[int, str]:
    hs = (actual_hs + add_hs) % 24
    if 0 <= hs < 6:
        return hs, "NIGHT"
    elif 6 <= hs < 12:
        return hs, "MORNING"
    elif 12 <= hs < 18:
        return hs, "AFTERNOON"
    elif 18 <= hs < 22:
        return hs, "EVENING"
    return hs, "NIGHT"


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


# Import dictionary from txt.
def load_dict_from_txt(file_path: str) -> dict:
    reloaded_dictionary = {}
    current_key = []
    try:
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

    except OSError:
        print(" No loadable save file!")
        input(" > ")

    return reloaded_dictionary


# Typewriter function.
def typewriter(text: str, speed: float = 0.01) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


# Print patron in column function.
def patron_print(elements, n):
    patron = []
    elements_cycle = cycle(elements)
    for _ in range(n):
        patron.append(next(elements_cycle))
    return patron
