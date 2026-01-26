import pytest
from datetime import datetime, timedelta

from eck.memory import WorldModel
from eck.task import TaskState
from eck.config import ECKConfig, PolicyMode


@pytest.fixture
def world_model():
    return WorldModel()


def test_record_stores_fields_and_timestamp(world_model):
    world_model.record(
        task_id="t1",
        task_text="Explore objective",
        prediction="pred",
        outcome="outcome",
        success=True,
        feedback="good",
        state=TaskState.SUCCEEDED,
    )

    # Internal storage uses datetime timestamp (not isoformat)
    raw = world_model.tasks["t1"]
    assert raw["task"] == "Explore objective"
    assert raw["state"] == TaskState.SUCCEEDED.value
    assert raw["prediction"] == "pred"
    assert raw["outcome"] == "outcome"
    assert raw["success"] is True
    assert raw["feedback"] == "good"
    assert raw["timestamp"] is not None  # datetime object


def test_get_serializes_timestamp_to_isoformat(world_model):
    world_model.record(
        task_id="t1",
        task_text="test",
        prediction="",
        outcome="",
        success=False,
        feedback="",
        state=TaskState.CREATED,
    )
    entry = world_model.get("t1")
    assert entry is not None
    assert isinstance(entry["timestamp"], str)  # isoformat boundary serialization


def test_get_recent_ordering(world_model):
    world_model.record("t1", "first", "", "", False, "", TaskState.CREATED)
    world_model.record("t2", "second", "", "", False, "", TaskState.CREATED)

    # Force deterministic timestamps
    base = datetime(2020, 1, 1, 0, 0, 0)
    world_model.tasks["t1"]["timestamp"] = base
    world_model.tasks["t2"]["timestamp"] = base + timedelta(seconds=1)

    recent = world_model.get_recent(2)
    assert [e["task"] for e in recent] == ["second", "first"]  # newest first


def test_get_similar_thresholding_and_ordering(world_model):
    world_model.record("t1", "apple fruit", "", "", False, "", TaskState.CREATED)
    world_model.record("t2", "banana fruit", "", "", False, "", TaskState.CREATED)
    world_model.record("t3", "carrot vegetable", "", "", False, "", TaskState.CREATED)

    # Force deterministic timestamps for ordering
    base = datetime(2020, 1, 1, 0, 0, 0)
    world_model.tasks["t1"]["timestamp"] = base
    world_model.tasks["t2"]["timestamp"] = base + timedelta(seconds=1)
    world_model.tasks["t3"]["timestamp"] = base + timedelta(seconds=2)

    # "fruit salad" overlaps by 1 token with each "... fruit":
    # union size 3 => similarity = 1/3, so threshold must be <= 1/3
    similar = world_model.get_similar("fruit salad", threshold=1/3, limit=10)
    assert [e["task"] for e in similar] == ["banana fruit", "apple fruit"]


def test_retrieve_similar_prefer_failures_orders_failures_first(world_model):
    world_model.record("t1", "apple fruit", "", "", True, "", TaskState.CREATED)    # success
    world_model.record("t2", "banana fruit", "", "", False, "", TaskState.CREATED) # failure

    items = world_model.retrieve_similar(
        task_text="fruit salad",
        threshold=1/3,
        limit=2,
        prefer_failures=True,
    )
    assert [e["success"] for e in items] == [False, True]


def test_retrieve_scored_drops_score_zero_and_sorts_desc(world_model):
    world_model.record("t1", "apple fruit", "", "", False, "", TaskState.CREATED)
    world_model.record("t2", "banana fruit", "", "", True, "", TaskState.CREATED)
    world_model.record("t3", "carrot vegetable", "", "", False, "", TaskState.CREATED)

    scored = world_model.retrieve_scored(
        task_text="fruit salad",
        policy_mode=PolicyMode.NORMAL,
        config=ECKConfig(),
        threshold=1/3,
        limit=10,
        prefer_failures=False,
    )

    # carrot has 0 overlap => score 0 => dropped
    assert [e["task"] for e in scored] == ["apple fruit", "banana fruit"]

    # Failures score higher than successes (severity 2.0 vs 1.0 in score_memory_entry)
    assert scored[0]["task"] == "apple fruit"

    # scores present and sorted descending
    assert scored[0]["score"] >= scored[1]["score"]
    assert scored[0]["score"] > 0
    assert scored[1]["score"] > 0
