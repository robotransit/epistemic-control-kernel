```
import pytest
import logging

from eba.utils import get_recommended_breadth
from eba.config import PolicyMode

def test_get_recommended_breadth_normal_mode():
    # NORMAL mode must always return FULL (no influence)
    assert get_recommended_breadth(0.9, PolicyMode.NORMAL) == "FULL"
    assert get_recommended_breadth(0.5, PolicyMode.NORMAL) == "FULL"
    assert get_recommended_breadth(0.2, PolicyMode.NORMAL) == "FULL"

def test_get_recommended_breadth_guided_mode():
    # GUIDED mode uses mapping for soft guidance
    assert get_recommended_breadth(0.9, PolicyMode.GUIDED) == "FULL"
    assert get_recommended_breadth(0.6, PolicyMode.GUIDED) == "MODERATE"
    assert get_recommended_breadth(0.4, PolicyMode.GUIDED) == "RESTRICTED"
    assert get_recommended_breadth(0.2, PolicyMode.GUIDED) == "DEFERRED"

def test_get_recommended_breadth_enforced_mode():
    # ENFORCED mode allows full mapping range
    assert get_recommended_breadth(0.9, PolicyMode.ENFORCED) == "FULL"
    assert get_recommended_breadth(0.6, PolicyMode.ENFORCED) == "MODERATE"
    assert get_recommended_breadth(0.4, PolicyMode.ENFORCED) == "RESTRICTED"
    assert get_recommended_breadth(0.2, PolicyMode.ENFORCED) == "DEFERRED"

def test_get_recommended_breadth_threshold_boundaries():
    # Pin exact threshold boundaries from mapping doc
    assert get_recommended_breadth(0.8, PolicyMode.GUIDED) == "FULL"  # Boundary high
    assert get_recommended_breadth(0.799, PolicyMode.GUIDED) == "MODERATE"  # Just below
    assert get_recommended_breadth(0.5, PolicyMode.GUIDED) == "MODERATE"  # Boundary mid
    assert get_recommended_breadth(0.499, PolicyMode.GUIDED) == "RESTRICTED"  # Just below
    assert get_recommended_breadth(0.3, PolicyMode.GUIDED) == "RESTRICTED"  # Boundary low
    assert get_recommended_breadth(0.299, PolicyMode.GUIDED) == "DEFERRED"  # Just below

def test_get_recommended_breadth_logging_observability(caplog):
    # Ensure resolver logs recommendation without impact
    caplog.set_level(logging.INFO)

    get_recommended_breadth(0.7, PolicyMode.GUIDED)

    assert len(caplog.records) > 0  # At least one log record emitted
    record = caplog.records[-1]  # Latest record
    assert record.levelno == logging.INFO
    assert record.name == "eba-core"
  ```
