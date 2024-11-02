# Imports.
# External imports

# Local imports.


class Npc:
    def __init__(self,
                 name: str = "...",
                 npc_type: str = "traveler",
                 messages=None,
                 answers=None,
                 leave_message=None,
                 buy_items=None,
                 buy_beds=None,
                 room_expirations=None):

        if buy_beds is None:
            buy_beds = {}

        if leave_message is None:
            leave_message = []

        if buy_items is None:
            buy_items = {}

        if answers is None:
            answers = {}

        if messages is None:
            messages = {0: ["...", "..."]}

        # General attributs.
        self.name = name
        self.npc_type = npc_type
        self.messages = messages
        self.answers = answers
        self.leave_message = leave_message

        self.hist_messages = {}
        self.reset_hist_messages()
        self.talk_active = True

        # Merchants or Innkeepers.
        self.buy_items = buy_items
        self.buy_beds = buy_beds
        self.room_expirations = room_expirations

    def reset_hist_messages(self):
        self.hist_messages = {}
        for _ in self.messages.keys():
            self.hist_messages[_] = False


