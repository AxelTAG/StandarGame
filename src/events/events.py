# Imports.
# Local imports.
# External imports.
from attrs import define, field
from typing import Callable, Optional, Any, Dict


@define
class Event:
    """
    Represents an in-game event with a name, description, and an executable action.

    :param id: Identifier for the event.
    :type id: str
    :param name: Human-readable name of the event.
    :type name: str
    :param description: Detailed description of what the event represents.
    :type description: str
    :param action: A callable representing the event's behavior.
                   This function should accept ``**kwargs`` so the event
                   manager can pass contextual data.
    :type action: Callable[..., None] or None
    """

    id: str = field(default=None)
    name: str = field(default="Unnamed Event")
    description: str = field(default="")
    action: Optional[Callable[..., None]] = field(default=None)
    trigger: Optional[Callable[..., bool]] = field(default=None)
    was_executed: bool = field(default=False)
    one_execution: bool = field(default=True)

    def can_execute(self, **kwargs: Dict[str, Any]) -> bool:
        """
        Determine whether the event is allowed to execute.

        If no trigger is set, the event is considered executable.

        :param kwargs: Optional keyword arguments passed to the trigger.
        :type kwargs: dict

        :return: ``True`` if the event can execute, ``False`` otherwise.
        :rtype: bool
        """
        if self.trigger is None:
            return True

        try:
            return bool(self.trigger(**kwargs))
        except Exception as e:
            print(f"Event '{self.id}' trigger raised an exception: {e}")
            raise

    def execute(self, **kwargs: Dict[str, Any]):
        """
        Execute the event's associated action.

        :param kwargs: Optional keyword arguments to pass to the action.
        :type kwargs: dict

        :return: ``True`` if the action executed successfully,
                 ``False`` if no action is defined.
        :rtype: bool

        :raises Exception: If the action raises an unexpected error.
        """
        if self.action is None:
            return False

        if self.was_executed:
            return False

        if not self.can_execute(**kwargs):
            return False

        try:
            not_repeat = self.action(**kwargs)
            if not_repeat:
                self.one_execution = True
            if self.one_execution:
                self.was_executed = True
            return True
        except Exception as e:
            print(f"Event '{self.id}' raised an exception during execution: {e}")
            input()
            raise
