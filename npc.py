# Imports.
# Local imports.
from enums import NpcTypes, TimeOfDay

# External imports
from attrs import define, field


@define
class Npc:
    # General attributes.
    name: str = field(default="...")
    npc_type: NpcTypes = field(default=None)
    messages: dict[int, list[str, str]] = field(default=None)
    answers: dict[int, str] = field(default=None)
    leave_message: list[str] = field(default=None)
    place: list = field(default=None)

    # Merchants or Innkeepers.
    buy_items: dict[str, int] = field(default=None)
    buy_beds: dict[str, tuple[int, str]] = field(default=None)
    room_expirations: dict[str, tuple] = field(default=None)

    # Crafting items.
    crafting_items: dict[str, int] = field(default=None)

    # Talking attributes.
    hist_messages: dict = field(init=False)

    # Temporal and placing attriubtes.
    hour_morning: int = field(default=6)
    place_morning: list = field(default=None)
    messages_morning: list[int: list[str]] = field(default=None)
    answers_morning: list[int: list[str]] = field(default=None)

    hour_afternoon: int = field(default=12)
    place_afternoon: list = field(default=None)
    messages_afternoon: list[int: list[str]] = field(default=None)
    answers_afternoon: list[int: list[str]] = field(default=None)

    hour_evening: int = field(default=18)
    place_evening: list = field(default=None)
    messages_evening: list[int: list[str]] = field(default=None)
    answers_evening: list[int: list[str]] = field(default=None)

    hour_night: int = field(default=22)
    place_night: list = field(default=None)
    messages_night: list[int: list[str]] = field(default=None)
    answers_night: list[int: list[str]] = field(default=None)

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

        if self.room_expirations is None:
            self.room_expirations = {}

        # Talking attributes.
        self.hist_messages = {}
        self.reset_hist_messages()
        self.refresh_temporal(hour=6)

    def reset_hist_messages(self):
        self.hist_messages = {}
        for _ in self.messages.keys():
            self.hist_messages[_] = False

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
            if self.place_afternoon:
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
