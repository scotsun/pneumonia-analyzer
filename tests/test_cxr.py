"""Test CXR objects.

The test part of this project is limited as most of the work is about graphics and GUI.
"""

import sys

sys.path.append("../final_project")  # noqa: E402
from chest_radiography import CXR, db

cxr0 = CXR(pid="00436515-870c-4b36-a041-de91049b9ab4")
cxr1 = CXR(pid="00313ee0-9eaa-42f4-b0ab-c148ed3241cd")
cxr2 = CXR(pid="some-random-pid")


def test_cxr_is_diagnosed() -> None:
    """Test CXR object init."""
    assert cxr0.is_diagnosed
    assert cxr1.is_diagnosed
    assert not cxr2.is_diagnosed


def test_cxr_db() -> None:
    """Test if correction information (annot.csv) input into db."""
    cxr0_record = db.cxr.find_one({"pid": cxr0.pid})
    cxr1_record = db.cxr.find_one({"pid": cxr1.pid})
    cxr2_record = db.cxr.find_one({"pid": cxr2.pid})
    if cxr0_record:
        assert cxr0_record["diagnose"] == 1
        assert len(cxr0_record["x"]) == 2
    else:
        assert False
    if cxr1_record:
        assert cxr1_record["diagnose"] == 0
        assert len(cxr1_record["x"]) == 0
    else:
        assert False
    assert cxr2_record is None
