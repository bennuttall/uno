from uno import ReversibleCycle


def test_cycle_forward():
    rc = ReversibleCycle(range(3))
    assert next(rc) == 0
    assert next(rc) == 1
    assert next(rc) == 2
    assert next(rc) == 0
    assert next(rc) == 1
    assert next(rc) == 2


def test_cycle_reverse_mid():
    rc = ReversibleCycle(range(3))
    next(rc)  # 0
    next(rc)  # 1
    next(rc)  # 2
    next(rc)  # 0
    next(rc)  # 1
    next(rc)  # 2
    rc.reverse()
    assert next(rc) == 1
    assert next(rc) == 0
    rc.reverse()
    assert next(rc) == 1


def test_cycle_reverse_from_start():
    rc = ReversibleCycle(range(3))
    rc.reverse()
    assert next(rc) == 2
    assert next(rc) == 1


def test_cycle_double_reverse():
    rc = ReversibleCycle(range(3))
    rc.reverse()
    rc.reverse()
    assert next(rc) == 0
    assert next(rc) == 1
