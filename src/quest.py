# Imports.
# Local imports.
from enums import ObjectiveType, QuestStatus

# External imports.
from attrs import define, field


@define
class QuestObjective:
    type: ObjectiveType
    target: str
    amount: int = 1
    progress: int = 0
    deliver_to: str = None

    def update(self, target: str, amount: int = 1, receiver: str = None):
        if self.type == ObjectiveType.COLLECT:
            if self.target == target:
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
            if self.target == target and self.deliver_to == receiver:
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
    messages_npc: dict = field(default=None)
    answers_npc: dict = field(default=None)

    def __attrs_post_init__(self):
        if self.status not in QuestStatus:
            raise ValueError("Status must be a value on QuestStatus enum.")

    def start(self):
        if self.status == QuestStatus.NOT_STARTED:
            self.status = QuestStatus.IN_PROGRESS

    def update_progress(self, target: str, amount: int = 1):
        if self.status != QuestStatus.IN_PROGRESS:
            return
        for obj in self.objectives:
            obj.update(target, amount)
        if self.is_completed():
            self.status = QuestStatus.COMPLETED

    def is_started(self) -> bool:
        return self.status != QuestStatus.NOT_STARTED

    def is_completed(self) -> bool:
        return all(obj.is_done() for obj in self.objectives)

    def claim_reward(self):
        if self.status == QuestStatus.COMPLETED:
            self.status = QuestStatus.REWARDED
            return self.rewards
        return {}
