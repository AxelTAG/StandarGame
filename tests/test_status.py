# tests/test_status.py

from src.enums import StatusType
from src.status import Status

from pytest import fixture


@fixture
def standar_status():
    return Status(status_type=StatusType.POISON,
                  name="StandarStatus",
                  duration=3)


def test_attributes_standarstatus(standar_status):
    assert standar_status.name == "StandarStatus"
    assert standar_status.duration == 3
    assert standar_status.stacks == 1
    assert standar_status.max_stacks == 1
    assert standar_status.damaging is True
    assert standar_status.stunner is False


def test_tick_reduces_duration_standarstatus():
    called = {}

    def on_tick(entity, status):
        called["OK"] = True

    status = Status(status_type=StatusType.POISON,
                    name="Tick",
                    duration=2,
                    on_tick=on_tick)
    status.tick(entity="dummy")

    assert called["OK"] is True
    assert status.duration == 1


def test_apply_stack_increases_stacks_and_refreshes_duration():
    s1 = Status(status_type=StatusType.POISON, name="Poison", duration=2, stacks=1, max_stacks=3)
    s2 = Status(status_type=StatusType.POISON, name="Poison", duration=5, stacks=2, max_stacks=5)

    s1.apply_stack(s2)

    assert s1.max_stacks == 5
    assert s1.stacks == 3
    assert s1.duration == 5


def test_is_damaging_and_stunner():
    s = Status(status_type=StatusType.POISON, name="Check")
    assert s.is_damaging() is True
    assert s.is_sttuner() is False


def test_gen_poison_factory():
    s = Status.gen_poison(duration=4, stacks=1, max_stacks=3, source="enemy")
    assert s.name == "Poison"
    assert s.status_type == StatusType.POISON
    assert s.duration == 4
    assert s.stacks == 1
    assert s.max_stacks == 3
    assert s.priority == 1
    assert s.source == "enemy"
    assert s.damaging is True
    assert s.stunner is False
