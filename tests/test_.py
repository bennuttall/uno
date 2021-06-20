from uno.utils import ReversibleCycle


def test_reversible_cycle():
    rc = ReversibleCycle(range(3))
    a = next(rc)
    assert a == 0
    a = next(rc)
    assert a == 1
    a = next(rc)
    assert a == 2
    a = next(rc)
    assert a == 0
    a = next(rc)
    assert a == 1
    a = next(rc)
    assert a == 2
    rc.reverse()
    a = next(rc)
    assert a == 1
    a = next(rc)
    assert a == 0
    rc.reverse()
    a = next(rc)
    assert a == 1

    rc = ReversibleCycle(range(3))
    rc.reverse()
    a = next(rc)
    assert a == 2
    a = next(rc)
    assert a == 1

    rc = ReversibleCycle(range(3))
    rc.reverse()
    rc.reverse()
    a = next(rc)
    assert a == 0
    a = next(rc)
    assert a == 1