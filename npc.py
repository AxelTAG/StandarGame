# Imports.
# Local imports.
from enums import NpcTypes

# External imports
from attrs import define, field


@define
class Npc:
    # General attributes.
    name: str = field(default="...")
    npc_type: NpcTypes = field(default=None)
    messages: dict[int, list[str, str]] = field(default=None)
    answers: dict[int, str] = field(default=None)
    leave_message = field(default=None)

    # Merchants or Innkeepers.
    buy_items: dict[str, int] = field(default=None)
    buy_beds: dict[str, tuple[int, str]] = field(default=None)
    room_expirations: dict[str, tuple] = field(default=None)

    # Talking attributes.
    hist_messages = field(init=False)
    talk_active = field(default=True)

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

    def reset_hist_messages(self):
        self.hist_messages = {}
        for _ in self.messages.keys():
            self.hist_messages[_] = False
