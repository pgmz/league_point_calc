import pytest
from leaguepointcalc.league_status import MatchResult


@pytest.mark.parametrize("point1,point2,output", [
    (5, 5, MatchResult.DRAW),
    (2, 10, MatchResult.LOSS),
    (10, 3, MatchResult.WIN)
])
def test_match_result(point1, point2, output):
    assert MatchResult.matchResult(point1, point2) is output
