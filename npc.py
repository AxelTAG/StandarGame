# Imports.
# External imports

# Local imports.


class Npc:
    def __init__(self, name: str = "...", npc_type: str = "traveler", messages=None,
                 answers=None, buy_items=None):

        if buy_items is None:
            buy_items = {}

        if answers is None:
            answers = {}

        if messages is None:
            messages = {0: ["...", "..."]}

        self.name = name
        self.npc_type = npc_type
        self.messages = messages
        self.answers = answers
        self.buy_items = buy_items

        self.hist_messages = {}
        self.reset_hist_messages()

    def reset_hist_messages(self):
        self.hist_messages = {}
        for _ in self.messages.keys():
            self.hist_messages[_] = False
