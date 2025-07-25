# Imports.
# Locals imports.
import globals
import displays
import enums
import management
import actions
from actions import *
from map import Map
from player import Player
from utils import draw_move, clear, check_name, find_full_name, reset_map

# External imports.
import copy
import matplotlib.pyplot as plt
import os
import random
import time
from attrs import define, field
from datetime import datetime

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


@define
class Game:
    # Game variables.
    run: bool = field(default=True)
    menu: bool = field(default=True)
    play: bool = field(default=False)
    rules: bool = field(default=False)
    music: bool = field(default=True)
    settings: bool = field(default=False)
    first_setting: bool = field(default=False)
    loaded_game: bool = field(init=False)

    # Play variables.
    fight: bool = field(default=False)
    standing: bool = field(default=True)
    mapgame: Map = field(init=False)

    # Admin.
    admin: bool = field(default=False)

    # Existent player.
    existent_player: Player = field(default=None)
    player_name: str = field(default=None)

    def __attrs_post_init__(self):
        # Init pygame music.
        pygame.mixer.init()
        pygame.mixer.music.set_volume(globals.MUSIC_VOLUME)

        # Game variables.
        self.loaded_game = False

        # Existent player.
        if self.existent_player is None:
            self.existent_player = management.import_player(path="./cfg_save.pkl")

    def show_intro(self) -> None:
        # Enter screen.
        displays.clear()
        displays.disp_intro()
        input()

    def show_menu(self) -> None:
        # Music background.
        self.play_music(filepath="./rsc/media/Echoes_of_the_Ancient_Lanes.mp3",
                        volume=globals.MUSIC_VOLUME,
                        bucle=True,
                        busy=True)

        # Main screen.
        displays.clear()
        displays.disp_title()
        displays.disp_main_screen()

        # Choice selection.
        selection = input(" # ")

        if selection == "1":
            self.show_new_game()
        if selection == "2":
            self.show_load_game()
        if selection == "3":
            self.show_rules()
        if selection == "4":
            self.show_settings()
        if selection == "5":
            self.close()

    def show_new_game(self) -> None:
        displays.clear()
        displays.disp_title()
        displays.disp_new_game(existent_player=self.existent_player)

        selection = ""
        if self.existent_player:
            selection = input(" # ")

        if self.existent_player is None or selection == "1":
            player_name = ""
            while not check_name(player_name):
                print()
                player_name = input(" # What's your NAME, hero? ").title()

            self.player_name = player_name

            self.menu = False
            self.play = True
            self.first_setting = True

    def show_load_game(self) -> None:
        displays.clear()
        displays.disp_title()
        displays.disp_load_game()

        load_state, load_msg, player, map_game = management.load(check_hash=False)

        if load_state:
            self.loaded_game = load_state
            self.menu = False
            self.play = True
            self.existent_player = player
            self.mapgame = map_game

        print(load_msg)
        input(" > ")

    def main(self):
        self.show_intro()
        while self.run:
            if self.menu:
                self.show_menu()
            if self.rules:
                self.show_rules()
            if self.settings:
                self.show_settings()
            if self.play:
                self.show_play()
        self.close()

    def show_play(self):
        # Loading existent map.
        if self.loaded_game:
            player = self.existent_player
            map_game = self.mapgame

        # Introduction of new game.
        if self.first_setting:
            # Stop of background music.
            self.stop_music()
            time.sleep(1.5)

            # Initial settings.
            # Map settings.
            map_game = Map(mobs=globals.MOBS.copy(),
                           biomes=globals.BIOMES.copy(),
                           npcs=globals.NPCS.copy(),
                           entries=globals.ENTRIES.copy())

            # Player.
            player = Player(name=self.player_name,
                            place=map_game.map_settings[(0, 0)].entries["hut"],
                            last_place=map_game.map_settings[(0, 0)].entries["hut"],
                            last_entry=map_game.map_settings[(0, 0)].entries["hut"])

            # Location setting.
            map_game.map_settings[(0, 0)].entries["hut"].name = player.name + "'s Hut"

            # Introduction setting.
            map_game.npcs["whispers"].messages = {
                0: [player.name + "...", player.name + "...",
                    "...your destiny awaits.",
                    "Follow the whispers of the wind, and come to me.",
                    "Secrets untold and challenges unknown lie ahead.",
                    "Trust in the unseen path...",
                    "... come to me."]}

            # Dragon Firefrost setting.
            map_game.npcs["dragon_firefrost"].messages = {
                0: [player.name + "...", "You finally come to me...",
                    "Destiny calls for a dance of fire and frost between us...",
                    "Ready your blade..."]}

            # Introduction.
            if player.name:
                screen = talk(npc=map_game.npcs["whispers"],
                              player=player,
                              map_game=map_game)

        # Previous setting before start playing.
        # First screen massage.
        screen = random.choices(population=[msg.value for msg in enums.FirstMessages],
                                weights=[1, 1],
                                k=1)[0]

        # Music background.
        action = ["nothing"]

        # Set hours.
        hours = map_game.get_hours

        displays.clear()
        while self.play:
            # Time setting.
            time_init = datetime.now()

            # Event handler and map control.
            self.play, self.menu = management.event_handler(player=player,
                                                            map_game=map_game,
                                                            time_init=time_init)
            management.map_control_handling(player=player,
                                            map_game=map_game)

            if not (map_game.get_hours == hours):
                # Map refresh.
                map_game.refresh_npcs()
                map_game.refresh_biomes()

                # Player status refresh.
                player.refresh_status()
                player.refresh_hungry(hour=map_game.get_hours,
                                      last_hour=hours)
                player.refresh_thirsty(hour=map_game.get_hours,
                                       last_hour=hours)

            # Setting reinit.
            if player.hp <= 0:
                self.play = False
                self.menu = True
                player.hp, player.x, player.y = int(player.hpmax), player.x_cp, player.y_cp
                player.status = 0
                player.poison = 0
                player.hungry = 48
                player.thirsty = 48
                player.exp = 0
                reset_map(ms=map_game.map_settings,
                          keys=[(2, 1), (6, 2)])
                displays.disp_game_loss()

            hours = map_game.get_hours

            if action[0] != "listen":
                pygame.mixer.music.stop()

            # Autosave.
            management.save(player=player,
                            map_game=map_game,
                            time_init=time_init)  # Autosave.
            clear()

            # Fight chances of moving, and player status refreshing.
            if not player.standing:
                # Fight.
                if player.place.fight and player.place.mobs_respawned:
                    if random.randint(a=0, b=100) < max(player.place.mobs_chances):
                        enemy = random.choices(player.place.mobs_respawned, k=1)[0]
                        play, menu, win = battle(player=player,
                                                 map_game=map_game,
                                                 enemy=copy.deepcopy(map_game.mobs[enemy]))
                        if win:
                            player.place.mobs_respawned.remove(enemy)
                        management.save(player=player,
                                        map_game=map_game,
                                        time_init=time_init)

            if self.play:
                # Draw of general stats.
                clear()
                displays.disp_play(player=player,
                                   map_game=map_game,
                                   reg="NAIWAT",
                                   x=player.x,
                                   y=player.y,
                                   mdir=draw_move(x=player.x,
                                                  y=player.y,
                                                  map_height=map_game.x_len,
                                                  map_width=map_game.y_len,
                                                  player=player,
                                                  tl_map=map_game.map_labels,
                                                  ms=map_game.map_settings),
                                   screen_text=screen,
                                   width=38)

                # Input action.
                print()
                action = input(" " * 2 + "# ").lower().split()
                if not action:
                    action = ["None"]
                    player.standing = True

                # Action ejecution.
                if action[0] == "0":  # Save game.
                    self.play = False
                    self.menu = True
                    management.save(player=player, map_game=map_game, time_init=time_init)

                if action[0] in ["1", "2", "3", "4"]:  # Move action.
                    if not player.move_available:
                        screen = "You're carrying too much weight to move."

                    elif player.outside:
                        screen, player.standing = move(player=player, map_game=map_game, mv=action[0])

                    else:
                        screen = "You are in " + player.place.name.title().replace("'S", "'s")

                elif action[0] in ["5", "6"]:  # Fast use object action.
                    if action[0] == "5":
                        screen, _ = use(player=player, map_game=map_game, item=player.slot1)
                    if action[0] == "6":
                        screen, _ = use(player=player, map_game=map_game, item=player.slot2)
                    player.standing = True

                elif action[0] == "assign":  # Assign action.
                    if len(action) < 2:
                        screen = displays.disp_assign(player.st_points)
                    elif player.st_points:
                        if action[1] in ["strength", "str"]:
                            player.strength += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to strength."
                        elif action[1] in ["agility", "agi"]:
                            player.agility += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to agility."
                        elif action[1] in ["resistance", "res"]:
                            player.resistance += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to resistance."
                        elif action[1] in ["vitality", "vit"]:
                            player.vitality += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to vitality."
                    elif player.st_points == 0:
                        screen = "You have no more skill points left."
                    else:
                        "That is not posible."
                    player.standing = True

                elif action[0] == "attack":  # Attack action.
                    if len(action) == 1:
                        screen = displays.disp_attack()
                    else:
                        mob = " ".join(action[1:])
                        if player.place.has_mob_respawned(mob=mob):
                            play, menu, win = actions.attack(player=player,
                                                             map_game=map_game,
                                                             mob=copy.deepcopy(map_game.mobs[mob]))

                            if win:
                                player.place.mobs_respawned.remove(mob)
                            else:
                                management.save(player=player,
                                                map_game=map_game,
                                                time_init=time_init)
                        else:
                            screen = f"There is no {mob} here."

                elif action[0] == "check":  # Check action.
                    if len(action) == 1:
                        screen = check(player=player, item=" ".join(action[1:]))

                    elif action[1] in ["inv", "inventory"]:
                        screen = check(player=player, item="_".join(action[2:]), inventory=True)

                    else:
                        screen = check(player=player, item="_".join(action[1:]))

                elif action == ["draw", "map"]:  # Update of map action.
                    tower_of_eldra = map_game.map_settings[(22, 18)].entries["tower_of_eldra"].entries[
                        "tower_of_eldra_second_floor"]
                    tower_of_karun = map_game.map_settings[(2, 12)].entries["tower"].entries["second_floor"]
                    if player.place == tower_of_eldra:
                        exploration_radius = 10
                    elif player.place == tower_of_karun:
                        exploration_radius = 10
                    else:
                        exploration_radius = player.exploration_radius
                    player.standing = False
                    screen = draw_map(player=player, map_game=map_game, exploration_radius=exploration_radius)

                elif action[0] == "drink":
                    item = "_".join(action[1:])
                    if len(action) == 1:
                        screen = "DRINK ITEM to eat something."
                    else:
                        screen = drink(player=player, item=item)
                        player.standing = False

                elif action[0] == "drop":  # Drop action.
                    try:  # Converting input in proper clases and form.
                        item = "_".join(action[2:])
                        quantity = int(action[1])
                        screen = drop(player=player, item=item, quantity=quantity)  # Doing drop action.
                        player.standing = True

                    except ValueError:
                        screen = displays.disp_drop()  # Printing drop instructions.
                    except IndexError:
                        screen = displays.disp_drop()  # Printing drop instructions.

                elif action[0] == "eat":
                    item = "_".join(action[1:])
                    if len(action) == 1:
                        screen = "EAT ITEM to eat something."
                    else:
                        screen = eat(player=player, item=item)
                        player.standing = False

                elif action[0] == "enter":  # Enter action.
                    if len(action) <= 2:
                        screen = displays.disp_enter(player.place)
                        player.standing = True

                    else:
                        place_entries = [*player.place.entries.keys()]
                        entry_name = find_full_name(partial_name="_".join(action[2:]), names_list=place_entries)
                        screen, player.standing = enter(player=player, entrie=entry_name, map_game=map_game)

                elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
                    if len(action) <= 1:
                        screen = displays.disp_equip(player.equip)
                        player.standing = True

                    else:
                        screen = equip(player=player, item="_".join(action[1:]))
                        player.standing = True

                elif action[0] == "exit":  # Exit entrie action:
                    screen, player.standing = exit_entry(player=player, map_game=map_game)

                elif action[0] == "explore":  # Explore action:
                    screen = explore(player=player, map_game=map_game)
                    player.standing = False if player.outside else True

                elif action[0] == "fish":
                    screen = fish(player=player, map_game=map_game)
                    player.standing = False

                elif action[0] == "land":  # Land action.
                    screen = land(player=player, map_game=map_game)
                    player.standing = False

                elif action[0] == "listen":  # Listen action.
                    entities = player.place.npc + player.place.items
                    entitie_name = find_full_name(partial_name=" ".join(action[2:]).lower(), names_list=entities)
                    if len(action) <= 2:
                        screen = "What do you want to listen? LISTEN TO something."
                    else:
                        screen = listen(player=player, map_game=map_game, entitie=entitie_name)

                elif action == ["look", "around"]:  # Look around action.
                    look_around(player=player, map_game=map_game)
                    screen = displays.disp_look_around(player.place)
                    player.standing = False

                elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                    player.map[player.y][player.x] = globals.PINK
                    plt.figure(player.name + "'s map")
                    plt.imshow(player.map)
                    plt.title("Map")
                    plt.show()
                    player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].color
                    player.standing = True

                elif action[:2] == ["pick", "up"]:  # Pick up action.
                    screen = pick_up(player=player, item="_".join(action[2:]))

                elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                    screen = displays.disp_show_inventory(player)
                    player.standing = True

                elif action[0] == "slot1":  # Selection slot1 action.
                    item_select = "_".join(action[1:])
                    item_object = get_item(item_name=item_select)
                    if (
                            item_object.consumable or item_object.equippable) and item_select in player.inventory.items.keys():
                        player.slot1 = item_select
                    else:
                        screen = f"You cannot equip {item_object.name} in the belt."
                    player.standing = True

                elif action[0] == "slot2":  # Selection slot1 action.
                    item_select = "_".join(action[1:])
                    item_object = get_item(item_name=item_select)
                    if item_object.consumable or item_object.equippable and item_select in player.inventory.items.keys():
                        player.slot2 = item_select
                    else:
                        screen = f"You cannot equip {item_object.name} in the belt."
                    player.standing = True

                elif action[0] == "sleep":  # Sleep action.
                    if len(action) <= 2:
                        screen = displays.disp_sleep(player.x, player.y, player.place)
                        player.standing = True

                    else:
                        if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
                            screen = sleep_in_bed(player=player,
                                                  map_game=map_game,
                                                  time_of_day=enums.TimeOfDay[action[2].upper()].value)
                            player.x_cp, player.y_cp = player.x, player.y
                            player.standing = True

                        else:
                            screen = f"{action[2].title()} is not a time of day."
                            player.standing = True

                elif action[0] == "talk":  # Talk action.
                    npc_name = find_full_name(partial_name="_".join(action[2:]).lower(),
                                              names_list=player.place.npc)

                    if len(action) <= 2:
                        screen = displays.disp_talk(player.place)
                        player.standing = True

                    elif npc_name is None:
                        screen = "You need to specify the name more clearly."
                        player.standing = True

                    elif npc_name in player.place.npc:
                        screen = talk(npc=map_game.npcs[npc_name], player=player, map_game=map_game)
                        player.standing = True

                    else:
                        screen = f"Here no one is called {npc_name.title()}."
                        player.standing = True

                elif action[0] == "unequip":  # Unequip action.
                    if len(action) <= 1:
                        screen = displays.disp_equip(player.equip)
                        player.standing = True

                    else:
                        screen = unequip(player=player, item="_".join(action[1:]))
                        player.standing = True

                elif action == ["use", "boat"]:  # Use boat action.
                    screen = use_boat(player=player, map_game=map_game)
                    player.standing = True

                elif action[0] == "use":  # Use object action.
                    screen, _ = use(player, map_game=map_game, item="_".join(action[1:]))
                    player.standing = True

                elif action[0] == "wait":  # Wait action.
                    if len(action) <= 2:
                        screen = displays.disp_wait()
                        player.standing = True

                    else:
                        if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
                            screen = wait(map_game=map_game,
                                          time_of_day=enums.TimeOfDay[action[2].upper()].value)
                            player.standing = False
                        else:
                            screen = f"{action[2].title()} is not a time of day."
                            player.standing = True

                # --- admin commans.
                if action[0] == "poweradmin":
                    self.admin = True

                if self.admin:
                    if action[0] == "events":
                        screen = f"{player.events}"

                    elif action[0] == "estimate":
                        screen = f"{map_game.estimate_date(days=int(action[1]))}"

                    elif action[:2] == ["lvl", "up"]:
                        player.lvl_up()
                        screen = f"{map_game.estimate_date(days=int(action[1]))}"

                    elif action[0] == "precision":
                        screen = f"{player.precision}"

                    elif action[0] == "teleport":
                        player.set_place(map_game.map_settings[(int(action[1]), int(action[2]))])
                        screen = f"You have teleported to {action[1]} {action[2]}."

                    elif action[0] == "update":
                        opt = "_".join(action[1:])
                        screen, player, map_game = management.update(player=player, map_game=map_game, option=opt)

                    elif action[0] == "repair":
                        map_game.map_settings[(24, 18)].entries = {
                            "cave": map_game.map_settings[(27, 19)].entries["cave"]
                        }
                        map_game.map_settings[(24, 18)].entries["cave"].leave_entry = map_game.map_settings[
                            (24, 18)]
                        screen = "Game repaired."
            else:
                player.standing = True

    def events(self):
        pass

    def close(self):
        exit()

    def show_rules(self):
        displays.clear()
        displays.disp_title()
        displays.disp_rules()
        self.rules = False
        input(" > ")

    def show_settings(self):
        pass

    def play_music(self,
                   filepath: str,
                   volume: float = globals.MUSIC_VOLUME,
                   bucle: bool = False,
                   busy: bool = False):
        if busy:
            if pygame.mixer.music.get_busy():
                return
        pygame.mixer.music.load(filename=filepath)
        pygame.mixer.music.set_volume(volume)
        if bucle:
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def change_music_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume=volume)


#
# # Game variables.
# run = True
# menu = True
# play = False
# rules = False
#
# # Play variables.
# fight = False
# standing = True
# admin = False
#
# # Enter screen.
# displays.clear()
# displays.disp_logo(width=60)
# print(" < PRESS ENTER > ".center(60))
# input()
#
# # Music background.
# pygame.mixer.init()
# pygame.mixer.music.set_volume(globals.MUSIC_VOLUME)
#
# # Main loop of the game.
# while run:
#     # Menu loop.
#     while menu:
#         # Music background.
#         if not pygame.mixer.music.get_busy():
#             pygame.mixer.music.load("./rsc/media/Echoes_of_the_Ancient_Lanes.mp3")
#             pygame.mixer.music.play(-1)
#
#         # Main screen.
#         clear()
#         displays.disp_title()
#         displays.disp_main_screen()
#
#         # Rules.
#         if rules:
#             clear()
#             displays.disp_title()
#             displays.disp_rules()
#             rules = False
#             choice = ""
#             input(" > ")
#
#         # Choice selection.
#         choice = input(" # ")
#
#         # New game choice.
#         if choice == "1":
#             clear()
#             displays.disp_title()
#             existent_player = management.import_player("cfg_save.pkl")
#             displays.disp_new_game(existent_player=existent_player)
#
#             action_choice = ""
#             if existent_player:
#                 action_choice = input(" # ")
#
#             if existent_player is None or action_choice == "1":
#                 player_name = ""
#                 while not check_name(player_name):
#                     print()
#                     player_name = input(" # What's your NAME, hero? ").title()
#
#                 menu = False
#                 play = True
#
#             # Introduction of new game.
#             if play:
#                 # Stop of background musin.
#                 pygame.mixer.music.stop()
#                 time.sleep(1.5)
#
#                 # Initial settings.
#                 # Map settings.
#                 map_game = Map(mobs=globals.MOBS.copy(),
#                                biomes=globals.BIOMES.copy(),
#                                npcs=globals.NPCS.copy(),
#                                entries=globals.ENTRIES.copy())
#
#                 # Player.
#                 player = Player(name=player_name,
#                                 place=map_game.map_settings[(0, 0)].entries["hut"],
#                                 last_place=map_game.map_settings[(0, 0)].entries["hut"],
#                                 last_entry=map_game.map_settings[(0, 0)].entries["hut"])
#
#                 # Location setting.
#                 map_game.map_settings[(0, 0)].entries["hut"].name = player.name + "'s Hut"
#
#                 # Introduction setting.
#                 map_game.npcs["whispers"].messages = {
#                     0: [player.name + "...", player.name + "...",
#                         "...your destiny awaits.",
#                         "Follow the whispers of the wind, and come to me.",
#                         "Secrets untold and challenges unknown lie ahead.",
#                         "Trust in the unseen path...",
#                         "... come to me."]}
#
#                 # Dragon Firefrost setting.
#                 map_game.npcs["dragon_firefrost"].messages = {
#                     0: [player.name + "...", "You finally come to me...",
#                         "Destiny calls for a dance of fire and frost between us...",
#                         "Ready your blade..."]}
#
#                 # Introduction.
#                 if player.name:
#                     screen = talk(npc=map_game.npcs["whispers"], player=player, map_game=map_game)
#
#         elif choice == "2":  # Load game choice.
#             clear()
#             displays.disp_title()
#             displays.disp_load_game()
#
#             load_state, load_msg, player, map_game = management.load(check_hash=False)
#
#             if load_state:
#                 menu = False
#                 play = True
#
#             print(load_msg)
#             input(" > ")
#
#         elif choice == "3":  # Show rules option.
#             rules = True
#
#         elif choice == "4":  # Quit option.
#             pass
#
#         elif choice == "5":  # Quit option.
#             quit()
#
#     # Previous setting before start playing.
#     if play:
#         # First screen massage.
#         screen = random.choices(population=[msg.value for msg in enums.FirstMessages], weights=[1, 1], k=1)[0]
#
#         # Music background.
#         action = ["nothing"]
#
#         # Set hours.
#         hours = map_game.get_hours
#
#     while play:
#         # Time setting.
#         time_init = datetime.now()
#
#         # Event handler and map control.
#         play, menu = management.event_handler(player=player, map_game=map_game, time_init=time_init)
#         management.map_control_handling(player=player, map_game=map_game)
#
#         if not (map_game.get_hours == hours):
#             # Map refresh.
#             map_game.refresh_npcs()
#             map_game.refresh_biomes()
#
#             # Player status refresh.
#             player.refresh_status()
#             player.refresh_hungry(hour=map_game.get_hours, last_hour=hours)
#             player.refresh_thirsty(hour=map_game.get_hours, last_hour=hours)
#
#         # Setting reinit.
#         if player.hp <= 0:
#             play = False
#             menu = True
#             player.hp, player.x, player.y = int(player.hpmax), player.x_cp, player.y_cp
#             player.status = 0
#             player.poison = 0
#             player.hungry = 48
#             player.thirsty = 48
#             player.exp = 0
#             reset_map(ms=map_game.map_settings, keys=[(2, 1), (6, 2)])
#             print()
#             print("    YOU HAVE DIED")
#             print("    GAME OVER")
#             input("     > ")
#
#         hours = map_game.get_hours
#
#         if action[0] != "listen":
#             pygame.mixer.music.stop()
#
#         # Autosave.
#         management.save(player=player,
#                         map_game=map_game,
#                         time_init=time_init)  # Autosave.
#         clear()
#
#         # Fight chances of moving, and player status refreshing.
#         if not standing:
#             # Fight.
#             if player.place.fight and player.place.mobs_respawned:
#                 if random.randint(a=0, b=100) < max(player.place.mobs_chances):
#                     enemy = random.choices(player.place.mobs_respawned, k=1)[0]
#                     play, menu, win = battle(player=player,
#                                              map_game=map_game,
#                                              enemy=copy.deepcopy(map_game.mobs[enemy]))
#                     if win:
#                         player.place.mobs_respawned.remove(enemy)
#                     management.save(player=player,
#                                     map_game=map_game,
#                                     time_init=time_init)
#
#         if play:
#             # Draw of general stats.
#             clear()
#             displays.disp_play(player=player,
#                                map_game=map_game,
#                                reg="NAIWAT",
#                                x=player.x,
#                                y=player.y,
#                                mdir=draw_move(x=player.x,
#                                               y=player.y,
#                                               map_height=map_game.x_len,
#                                               map_width=map_game.y_len,
#                                               player=player,
#                                               tl_map=map_game.map_labels,
#                                               ms=map_game.map_settings),
#                                screen_text=screen,
#                                width=38)
#
#             # Input action.
#             print()
#             action = input(" " * 2 + "# ").lower().split()
#             if not action:
#                 action = ["None"]
#                 standing = True
#
#             # Action ejecution.
#             if action[0] == "0":  # Save game.
#                 play = False
#                 menu = True
#                 management.save(player=player, map_game=map_game, time_init=time_init)
#
#             if action[0] in ["1", "2", "3", "4"]:  # Move action.
#                 if not player.move_available:
#                     screen = "You're carrying too much weight to move."
#
#                 elif player.outside:
#                     screen, standing = move(player=player, map_game=map_game, mv=action[0])
#
#                 else:
#                     screen = "You are in " + player.place.name.title().replace("'S", "'s")
#
#             elif action[0] in ["5", "6"]:  # Fast use object action.
#                 if action[0] == "5":
#                     screen, _ = use(player=player, map_game=map_game, item=player.slot1)
#                 if action[0] == "6":
#                     screen, _ = use(player=player, map_game=map_game, item=player.slot2)
#                 standing = True
#
#             elif action[0] == "assign":  # Assign action.
#                 if len(action) < 2:
#                     screen = displays.disp_assign(player.st_points)
#                 elif player.st_points:
#                     if action[1] in ["strength", "str"]:
#                         player.strength += 1
#                         player.st_points -= 1
#                         screen = "You have assigned a skill point to strength."
#                     elif action[1] in ["agility", "agi"]:
#                         player.agility += 1
#                         player.st_points -= 1
#                         screen = "You have assigned a skill point to agility."
#                     elif action[1] in ["resistance", "res"]:
#                         player.resistance += 1
#                         player.st_points -= 1
#                         screen = "You have assigned a skill point to resistance."
#                     elif action[1] in ["vitality", "vit"]:
#                         player.vitality += 1
#                         player.st_points -= 1
#                         screen = "You have assigned a skill point to vitality."
#                 elif player.st_points == 0:
#                     screen = "You have no more skill points left."
#                 else:
#                     "That is not posible."
#                 standing = True
#
#             elif action[0] == "attack":  # Attack action.
#                 if len(action) == 1:
#                     screen = displays.disp_attack()
#                 else:
#                     win = False
#                     mob = " ".join(action[1:])
#                     if mob in map_game.mobs.keys():
#                         play, menu, win = actions.attack(player=player,
#                                                          map_game=map_game,
#                                                          mob=copy.deepcopy(map_game.mobs[mob]))
#
#                         if win:
#                             player.place.mobs_respawned.remove(mob)
#                         else:
#                             management.save(player=player,
#                                             map_game=map_game,
#                                             time_init=time_init)
#                     else:
#                         screen = f"There is no {mob} here."
#
#             elif action[0] == "check":  # Check action.
#                 if len(action) == 1:
#                     screen = check(player=player, item=" ".join(action[1:]))
#
#                 elif action[1] in ["inv", "inventory"]:
#                     screen = check(player=player, item="_".join(action[2:]), inventory=True)
#
#                 else:
#                     screen = check(player=player, item="_".join(action[1:]))
#
#             elif action == ["draw", "map"]:  # Update of map action.
#                 tower_of_eldra = map_game.map_settings[(22, 18)].entries["tower_of_eldra"].entries[
#                     "tower_of_eldra_second_floor"]
#                 tower_of_karun = map_game.map_settings[(2, 12)].entries["tower"].entries["second_floor"]
#                 if player.place == tower_of_eldra:
#                     exploration_radius = 10
#                 elif player.place == tower_of_karun:
#                     exploration_radius = 10
#                 else:
#                     exploration_radius = player.exploration_radius
#                 standing = False
#                 screen = draw_map(player=player, map_game=map_game, exploration_radius=exploration_radius)
#
#             elif action[0] == "drink":
#                 item = "_".join(action[1:])
#                 if len(action) == 1:
#                     screen = "DRINK ITEM to eat something."
#                 else:
#                     screen = drink(player=player, item=item)
#                     standing = False
#
#             elif action[0] == "drop":  # Drop action.
#                 try:  # Converting input in proper clases and form.
#                     item = "_".join(action[2:])
#                     quantity = int(action[1])
#                     screen = drop(player=player, item=item, quantity=quantity)  # Doing drop action.
#                     standing = True
#
#                 except ValueError:
#                     screen = displays.disp_drop()  # Printing drop instructions.
#                 except IndexError:
#                     screen = displays.disp_drop()  # Printing drop instructions.
#
#             elif action[0] == "eat":
#                 item = "_".join(action[1:])
#                 if len(action) == 1:
#                     screen = "EAT ITEM to eat something."
#                 else:
#                     screen = eat(player=player, item=item)
#                     standing = False
#
#             elif action[0] == "enter":  # Enter action.
#                 if len(action) <= 2:
#                     screen = displays.disp_enter(player.place)
#                     standing = True
#
#                 else:
#                     place_entries = [*player.place.entries.keys()]
#                     entry_name = find_full_name(partial_name="_".join(action[2:]), names_list=place_entries)
#                     screen, standing = enter(player=player, entrie=entry_name, map_game=map_game)
#
#             elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
#                 if len(action) <= 1:
#                     screen = displays.disp_equip(player.equip)
#                     standing = True
#
#                 else:
#                     screen = equip(player=player, item="_".join(action[1:]))
#                     standing = True
#
#             elif action[0] == "exit":  # Exit entrie action:
#                 screen, standing = exit_entry(player=player, map_game=map_game)
#
#             elif action[0] == "explore":  # Explore action:
#                 screen = explore(player=player, map_game=map_game)
#                 standing = False if player.outside else True
#
#             elif action[0] == "fish":
#                 screen = fish(player=player, map_game=map_game)
#                 standing = False
#
#             elif action[0] == "land":  # Land action.
#                 screen = land(player=player, map_game=map_game)
#                 standing = False
#
#             elif action[0] == "listen":  # Listen action.
#                 entities = player.place.npc + player.place.items
#                 entitie_name = find_full_name(partial_name=" ".join(action[2:]).lower(), names_list=entities)
#                 if len(action) <= 2:
#                     screen = "What do you want to listen? LISTEN TO something."
#                 else:
#                     screen = listen(player=player, map_game=map_game, entitie=entitie_name)
#
#             elif action == ["look", "around"]:  # Look around action.
#                 look_around(player=player, map_game=map_game)
#                 screen = displays.disp_look_around(player.place)
#                 standing = False
#
#             elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
#                 player.map[player.y][player.x] = globals.PINK
#                 plt.figure(player.name + "'s map")
#                 plt.imshow(player.map)
#                 plt.title("Map")
#                 plt.show()
#                 player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].color
#                 standing = True
#
#             elif action[:2] == ["pick", "up"]:  # Pick up action.
#                 screen = pick_up(player=player, item="_".join(action[2:]))
#
#             elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
#                 screen = displays.disp_show_inventory(player)
#                 standing = True
#
#             elif action[0] == "slot1":  # Selection slot1 action.
#                 item_select = "_".join(action[1:])
#                 item_object = get_item(item_name=item_select)
#                 if (item_object.consumable or item_object.equippable) and item_select in player.inventory.items.keys():
#                     player.slot1 = item_select
#                 else:
#                     screen = f"You cannot equip {item_object.name} in the belt."
#                 standing = True
#
#             elif action[0] == "slot2":  # Selection slot1 action.
#                 item_select = "_".join(action[1:])
#                 item_object = get_item(item_name=item_select)
#                 if item_object.consumable or item_object.equippable and item_select in player.inventory.items.keys():
#                     player.slot2 = item_select
#                 else:
#                     screen = f"You cannot equip {item_object.name} in the belt."
#                 standing = True
#
#             elif action[0] == "sleep":  # Sleep action.
#                 if len(action) <= 2:
#                     screen = displays.disp_sleep(player.x, player.y, player.place)
#                     standing = True
#
#                 else:
#                     if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
#                         screen = sleep_in_bed(player=player,
#                                               map_game=map_game,
#                                               time_of_day=enums.TimeOfDay[action[2].upper()].value)
#                         player.x_cp, player.y_cp = player.x, player.y
#                         standing = True
#
#                     else:
#                         screen = f"{action[2].title()} is not a time of day."
#                         standing = True
#
#             elif action[0] == "talk":  # Talk action.
#                 npc_name = find_full_name(partial_name="_".join(action[2:]).lower(), names_list=player.place.npc)
#
#                 if len(action) <= 2:
#                     screen = displays.disp_talk(player.place)
#                     standing = True
#
#                 elif npc_name is None:
#                     screen = "You need to specify the name more clearly."
#                     standing = True
#
#                 elif npc_name in player.place.npc:
#                     screen = talk(npc=map_game.npcs[npc_name], player=player, map_game=map_game)
#                     standing = True
#
#                 else:
#                     screen = f"Here no one is called {npc_name.title()}."
#                     standing = True
#
#             elif action[0] == "unequip":  # Unequip action.
#                 if len(action) <= 1:
#                     screen = displays.disp_equip(player.equip)
#                     standing = True
#
#                 else:
#                     screen = unequip(player=player, item="_".join(action[1:]))
#                     standing = True
#
#             elif action == ["use", "boat"]:  # Use boat action.
#                 screen = use_boat(player=player, map_game=map_game)
#                 standing = True
#
#             elif action[0] == "use":  # Use object action.
#                 screen, _ = use(player, map_game=map_game, item="_".join(action[1:]))
#                 standing = True
#
#             elif action[0] == "wait":  # Wait action.
#                 if len(action) <= 2:
#                     screen = displays.disp_wait()
#                     standing = True
#
#                 else:
#                     if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
#                         screen = wait(map_game=map_game,
#                                       time_of_day=enums.TimeOfDay[action[2].upper()].value)
#                         standing = False
#                     else:
#                         screen = f"{action[2].title()} is not a time of day."
#                         standing = True
#
#             # --- admin commans.
#             if action[0] == "poweradmin":
#                 admin = True
#
#             if admin:
#                 if action[0] == "events":
#                     screen = f"{player.events}"
#
#                 elif action[0] == "estimate":
#                     screen = f"{map_game.estimate_date(days=int(action[1]))}"
#
#                 elif action[:2] == ["lvl", "up"]:
#                     player.lvl_up()
#                     screen = f"{map_game.estimate_date(days=int(action[1]))}"
#
#                 elif action[0] == "precision":
#                     screen = f"{player.precision}"
#
#                 elif action[0] == "teleport":
#                     player.set_place(map_game.map_settings[(int(action[1]), int(action[2]))])
#                     screen = f"You have teleported to {action[1]} {action[2]}."
#
#                 elif action[0] == "update":
#                     opt = "_".join(action[1:])
#                     screen, player, map_game = management.update(player=player, map_game=map_game, option=opt)
#
#                 elif action[0] == "repair":
#                     map_game.map_settings[(24, 18)].entries = {
#                         "cave": map_game.map_settings[(27, 19)].entries["cave"]
#                     }
#                     map_game.map_settings[(24, 18)].entries["cave"].leave_entry = map_game.map_settings[(24, 18)]
#                     screen = "Game repaired."
#         else:
#             standing = True


if __name__ == "__main__":
    game = Game()
    game.main()
    game.close()
