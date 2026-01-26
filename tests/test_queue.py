import pytest

from eck.queue import TaskQueue


@pytest.fixture
def queue():
    return TaskQueue(max_size=3)


def test_push_drops_oldest_when_over_max(queue):
    queue.push({"id": "t1", "text": "first"})
    queue.push({"id": "t2", "text": "second"})
    queue.push({"id": "t3", "text": "third"})
    queue.push({"id": "t4", "text": "fourth"})  # pushes over max_size

    assert len(queue) == 3
    assert [t["text"] for t in queue.as_list()] == ["second", "third", "fourth"]  # oldest dropped


def test_fifo_order(queue):
    queue.push({"id": "t1", "text": "first"})
    queue.push({"id": "t2", "text": "second"})
    queue.push({"id": "t3", "text": "third"})

    assert queue.pop()["text"] == "first"
    assert queue.pop()["text"] == "second"
    assert queue.pop()["text"] == "third"
    assert queue.pop() is None  # empty


def test_clear_empty_queue(queue):
    queue.push({"id": "t1", "text": "first"})
    queue.clear()
    assert len(queue) == 0
    assert queue.pop() is None


def test_as_list_returns_copy(queue):
    queue.push({"id": "t1", "text": "first"})
    lst = queue.as_list()
    assert lst == [{"id": "t1", "text": "first"}]
    lst.append({"id": "t2", "text": "second"})  # mutate copy
    assert len(queue) == 1  # original unchanged


def test_repr_shows_count_and_max(queue):
    queue.push({"id": "t1", "text": "first"})
    assert str(queue) == "TaskQueue(1/3 tasks)"
