from api.db_scripts import add_dhaval as D


def test_remove_its():
    assert D.remove_its("dfSi!r") == "dfS"
    assert D.remove_its("qukfY") == "kf"
    assert D.remove_its("BU") == "BU"
    assert D.remove_its("RIY") == "nI"


def test_num_agama():
    assert D.num_agama("vad") == "vand"
    assert D.num_agama("gaq") == "gaRq"
    assert D.num_agama("ah") == "aMh"
