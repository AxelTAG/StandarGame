# Imports.
# Local imports.
from .enums import ObjectiveType, QuestStatus

# External imports.
from attrs import define, field


@define
class QuestObjective:
    type: ObjectiveType
    target: str
    amount: int = 1
    progress: int = 0
    deliver_item: str = None
    deliver_amount: int = None

    def update(self, target: str, amount: int = 1,
               deliver_item: str = None,
               deliver_amount: int = None,
               carry: bool = False) -> None:
        if self.type == ObjectiveType.COLLECT:
            if self.target == target:
                if carry:
                    self.progress = amount
                    return
                self.progress = min(self.progress + amount, self.amount)
                return
            return

        if self.type == ObjectiveType.KILL:
            if self.target == target:
                self.progress = min(self.progress + amount, self.amount)
                return
            return

        if self.type == ObjectiveType.TALK:
            if self.target == target:
                self.progress = self.amount
                return
            return

        if self.type == ObjectiveType.DELIVER:
            if self.target == target and self.deliver_item == deliver_item and self.deliver_amount == deliver_amount:
                self.progress = self.amount
                return
            return

    def is_done(self) -> bool:
        return self.progress >= self.amount


@define
class Quest:
    id: str
    title: str
    description: str
    objectives: list[QuestObjective] = field(factory=list)
    rewards: dict[str, int] = field(factory=dict)
    status: QuestStatus = field(default=QuestStatus.NOT_STARTED)
    remove: bool = field(default=False)

    # Messages.
    messages_start: dict = field(default=None)
    answers_start: dict = field(default=None)
    messages_in_progress: dict = field(default=None)
    answers_in_progress: dict = field(default=None)
    messages_reward: dict = field(default=None)
    answers_reward: dict = field(default=None)

    def __attrs_post_init__(self):
        if self.status not in QuestStatus:
            raise ValueError("Status must be a value on QuestStatus enum.")

    def start(self):
        if self.status == QuestStatus.NOT_STARTED:
            self.status = QuestStatus.IN_PROGRESS

    def update_progress(self,
                        target: str,
                        amount: int = 1,
                        deliver_item: str = None,
                        deliver_amount: int = None,
                        carry: bool = False):
        if self.status != QuestStatus.IN_PROGRESS and not carry:
            return
        for obj in self.objectives:
            obj.update(target, amount, deliver_item=deliver_item, deliver_amount=deliver_amount, carry=carry)
        if self.is_completed():
            self.status = QuestStatus.COMPLETED
            return
        self.status = QuestStatus.IN_PROGRESS

    def is_started(self) -> bool:
        return self.status != QuestStatus.NOT_STARTED

    def is_in_progress(self) -> bool:
        return self.status == QuestStatus.IN_PROGRESS

    def is_completed(self) -> bool:
        return all(obj.is_done() for obj in self.objectives)

    def is_rewarded(self) -> bool:
        return self.status == QuestStatus.REWARDED

    def claim_reward(self):
        if self.status == QuestStatus.COMPLETED:
            self.status = QuestStatus.REWARDED
            return self.rewards
        return {}

    def give_items(self) -> dict[str, int]:
        items = {}
        for objetive in self.objectives:
            if objetive.type == ObjectiveType.DELIVER:
                items[objetive.deliver_item] = objetive.deliver_amount
        return items
