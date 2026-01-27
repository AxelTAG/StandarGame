# Imports.
# Local imports.
from .enums import NpcTypes, QuestStatus, TimeOfDay
from .quest import Quest

# External imports
from attrs import define, field, fields, has


@define
class Npc:
    # General attributes.
    name: str = field(default="...")
    npc_type: NpcTypes = field(default=None)
    messages: dict[int, list[str, str]] = field(default=None)
    answers: dict[int, str] = field(default=None)
    leave_message: list[str] = field(default=None)
    place: list = field(default=None)
    id: str = field(default=None)

    # Trading attributes.
    buy_items: dict[str, dict[str, int]] = field(default=None)
    quantity_message: str = field(default=None)

    buy_beds: dict[str, dict[str, int]] = field(default=None)
    room_expirations: dict[str, tuple] = field(default=None)
    bed_key_message: str = field(default=None)
    bed_low_message: str = field(default=None)

    # Crafting items attributes.
    crafting_items: dict[str, dict[str, int]] = field(default=None)

    # Transporting places attributes.
    transport_time_of_day: list[int] = field(default=None)
    transport_places: dict[tuple, dict] = field(factory=dict)
    transport_confirm_message: list[str] = field(default=None)
    transport_arrive_message: list[str] = field(default=None)

    # Talking attributes.
    hist_messages: dict = field(init=False)

    # Temporal and placing attriubtes.
    hour_morning: int = field(default=6)
    place_morning: list = field(default=None)
    messages_morning: dict[int: list[str]] = field(default=None)
    answers_morning: dict[int: list[str]] = field(default=None)

    hour_afternoon: int = field(default=12)
    place_afternoon: list = field(default=None)
    messages_afternoon: dict[int: list[str]] = field(default=None)
    answers_afternoon: dict[int: list[str]] = field(default=None)

    hour_evening: int = field(default=18)
    place_evening: list = field(default=None)
    messages_evening: dict[int: list[str]] = field(default=None)
    answers_evening: dict[int: list[str]] = field(default=None)

    hour_night: int = field(default=22)
    place_night: list = field(default=None)
    messages_night: dict[int: list[str]] = field(default=None)
    answers_night: dict[int: list[str]] = field(default=None)

    # Listen attributes.
    tracks: dict = field(default=None)

    # Quests.
    quests: list[Quest] = field(factory=list)

    # Update attributes.
    __updatable__: tuple[str, ...] = field(init=False, repr=False, default=())
    __migration_map__: dict[str, str] = field(init=False, repr=False, factory=dict)

    def __attrs_post_init__(self):
        if self.buy_beds is None:
            self.buy_beds = {}

        if self.leave_message is None:
            self.leave_message = []

        if self.buy_items is None:
            self.buy_items = {}

        if self.answers is None:
            self.answers = {}

        if self.messages is None:
            self.messages = {0: ["...", "..."]}

        if self.id is None:
            self.id = self.name.replace(" ", "_").lower()

        if self.room_expirations is None:
            self.room_expirations = {}

        if self.tracks is not None:
            for key in range(0, 8):
                self.tracks.setdefault(key, None)

        # Talking attributes.
        self.hist_messages = {}
        self.reset_hist_messages()
        self.refresh_temporal(hour=6)

        # Update attributes.
        self.__updatable__ = (
            # General attributes.
            "messages",
            "answers",
            "leave_message",
            "place",

            # Trading attributes.
            "room_expirations",

            # Transporting places attributes.
            "transport_time_of_day",
            "transport_places",
            "transport_confirm_message",
            "transport_arrive_message",

            # Talking attributes.
            "hist_messages",

            # Temporal and placing attributes.
            "hour_morning",
            "place_morning",
            "messages_morning",
            "answers_morning",

            "hour_afternoon",
            "place_afternoon",
            "messages_afternoon",
            "answers_afternoon",

            "hour_evening",
            "place_evening",
            "messages_evening",
            "answers_evening",

            "hour_night",
            "place_night",
            "messages_night",
            "answers_night",

            # Listen attributes.
            "tracks",

            # Quests.
            "quests",
        )

    # Messages and answer methods.
    def clear_messages_answers(self, messages: bool = True, answers: bool = True) -> None:
        if messages:
            self.messages = {}
            self.messages_morning = None
            self.messages_afternoon = None
            self.messages_evening = None
            self.messages_night = None
        if answers:
            self.answers = {}
            self.answers_morning = None
            self.answers_afternoon = None
            self.answers_evening = None
            self.answers_night = None

    def reset_hist_messages(self):
        self.hist_messages = {}
        for _ in self.messages.keys():
            self.hist_messages[_] = False

    # Refresh and status methods.
    def current_temporal(self, hour: int) -> int:
        if self.hour_night < self.hour_morning:
            if self.hour_night <= hour < self.hour_morning:
                return TimeOfDay.NIGHT.value

        if self.hour_morning <= hour < self.hour_afternoon:
            return TimeOfDay.MORNING.value

        elif self.hour_afternoon <= hour < self.hour_evening:
            return TimeOfDay.AFTERNOON.value

        elif self.hour_evening <= hour < self.hour_night:
            return TimeOfDay.EVENING.value

        else:
            return TimeOfDay.NIGHT.value

    def refresh_temporal(self, hour: int) -> None:
        current_temporal = self.current_temporal(hour=hour)

        if current_temporal == TimeOfDay.MORNING.value:
            if self.messages_morning is not None:
                self.messages = self.messages_morning
            if self.answers_morning is not None:
                self.answers = self.answers_morning
            if self.place_morning is not None:
                self.place = self.place_morning
            return

        if current_temporal == TimeOfDay.AFTERNOON.value:
            if self.messages_afternoon is not None:
                self.messages = self.messages_afternoon
            if self.answers_afternoon is not None:
                self.answers = self.answers_afternoon
            if self.place_afternoon is not None:
                self.place = self.place_afternoon
            return

        if current_temporal == TimeOfDay.EVENING.value:
            if self.messages_evening is not None:
                self.messages = self.messages_evening
            if self.answers_evening is not None:
                self.answers = self.answers_evening
            if self.place_evening is not None:
                self.place = self.place_evening
            return

        if current_temporal == TimeOfDay.NIGHT.value:
            if self.messages_night is not None:
                self.messages = self.messages_night
            if self.answers_night is not None:
                self.answers = self.answers_night
            if self.place_night is not None:
                self.place = self.place_night
            return

    # Buy/sell/craft methods.
    def get_quantity_message(self, item: str, buy: bool = False, craft: bool = False, sell: bool = False) -> str:
        if buy:
            return self.quantity_message.replace("#item", item.title()).replace("#action", "buy")
        if craft:
            return self.quantity_message.replace("#item", item.title()).replace("#action", "craft")
        if sell:
            return self.quantity_message.replace("#item", item.title()).replace("#action", "sell")
        raise ValueError("You must to pass buy, craft or sell argument.")

    def get_trading_items(self, item_base: dict) -> dict:
        items = {}
        if self.buy_items:
            items = self.buy_items

        if self.crafting_items:
            for k, v in self.crafting_items.items():
                items[k] = v | item_base[k].crafting_materials
        return items

    def get_bed_items(self) -> dict:
        return self.buy_beds

    # Transport methods.
    def add_transport_place(self, place_coordinate: tuple, place_price: dict[str, int]) -> None:
        self.transport_places[place_coordinate] = place_price

    def get_transport_places(self) -> dict[tuple, dict]:
        return self.transport_places

    # Quest methods.
    def has_quest(self, completed: bool = False) -> bool:
        if completed:
            return bool(self.quests)
        return any([not quest.is_rewarded() for quest in self.quests])

    def add_quest(self, quest: Quest) -> None:
        self.quests.append(quest)

    def remove_quest(self, quest: Quest | str) -> None:
        if isinstance(quest, str):
            for q in self.quests:
                if q.id == quest:
                    self.quests.remove(q)
                    return
        if quest in self.quests:
            self.quests.remove(quest)

    def get_first_quest(self):
        quests = [quest for quest in self.quests if not quest.is_rewarded()]
        return quests[0]

    def give_quest(self, quest: Quest) -> Quest | None:
        if quest in self.quests:
            if quest.status == QuestStatus.NOT_STARTED:
                quest.start()
                return quest
        return None

    def check_quests(self) -> list[Quest]:
        return [quest for quest in self.quests if quest.status in (QuestStatus.IN_PROGRESS, QuestStatus.COMPLETED)]

    def complete_quest(self, quest: Quest) -> dict | None:
        if quest in self.quests:
            if quest.status == QuestStatus.COMPLETED:
                return quest.claim_reward()
        return None

    # Update methods.
    def update_from_instance(self, old):
        if has(old.__class__):
            old_attrs = {f.name: getattr(old, f.name, None) for f in fields(old.__class__)}
        else:
            old_attrs = {
                name: getattr(old, name)
                for name in dir(old)
                if not name.startswith("__") and hasattr(old, name)
            }

        for attr, value in old_attrs.items():
            new_attr = self.__migration_map__.get(attr, attr)

            if new_attr in self.__updatable__:
                setattr(self, new_attr, value)

        self._after_migration(old=old)

    @staticmethod
    def _after_migration(old) -> None:
        def update_instances(entities: list) -> None:
            for entitie in entities:
                entitie.update()
