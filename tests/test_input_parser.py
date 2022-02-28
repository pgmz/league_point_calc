from types import NoneType
import pytest
from leaguepointcalc.input_parser import MatchEntry, parseTextEntry


@pytest.mark.parametrize("text,output", [
    ('Lions 3, Snakes 3', MatchEntry),
    ('Lions -3, Snakes 3', NoneType),
    ('Lions 3, Snakes ?', NoneType),
    ('Lions 3, sometext', NoneType),
    ('sometext', NoneType),
])
def test_parse_text_entry(text, output):
    assert type(parseTextEntry(text)) is output
