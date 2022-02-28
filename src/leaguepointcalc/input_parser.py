from typing import Any, List, Optional
import re

MATCH_REGEX = "(.*) ([0-9]*), (.*) ([0-9]*)"


class TeamEntry:
    """
    Class for team status in a match

    ...

    Attributes
    ----------
    teamName: str
        name of the team
    gamePoints: int
        # of game points in the match
    """
    teamName: str
    gamePoints: int

    def __init__(self, teamName: str, gamePoints: str):
        """
        Parameters
        ----------
        teamName: str
            name of the team to create object
        gamePoints: str
            # of game points in the match
        """
        self.teamName = teamName
        self.gamePoints = int(gamePoints)


class MatchEntry:
    """
    Class for match entry input. Has matchId and the list of teams involved

    ...

    Attributes
    ----------
    matchId: str
        id for a match, this can help to prevent having duplicated matches,
        for now is just the input string
    teams: List[TeamEntry]
        list (2) of teams involved in the match, with their names and points
    """
    matchId: str
    teams: List[TeamEntry]

    def __init__(self, matchId: str, team1: str, point1: str,
                 team2: str, point2: str):
        """
        Parameters
        ----------
        matchId: str
            unique id for a match
        team1: str
            name of first team
        point1: str
            game points of first team
        team2: str
            name of second team
        point2: str
            game points of second team
        """
        self.matchId = matchId
        self.teams = [TeamEntry(team1, point1), TeamEntry(team2, point2)]
        pass


def parseTextEntry(textMatchEntry: str) -> Optional[MatchEntry]:
    """
    Returns the text input that represents a match,
    into a MatchEntry object.

    Parameters
    ----------
    textMatchEntry: str
        text input in format 'team1 points1, team2 points2'
    """
    try:
        # If entries are expected to be well-formed,
        # we can assume string is format <team1> <point1>, <team2> <point2>
        # Run regex, and get the groups
        matched = re.match(MATCH_REGEX, textMatchEntry)
        if matched is not None:
            team1, point1, team2, point2 = matched.groups()
            matchObj = MatchEntry(matchId=textMatchEntry,
                                  team1=team1, point1=point1,
                                  team2=team2, point2=point2)
            return matchObj
    except Exception:
        print("Entry: ", textMatchEntry,
              " does not match format '[teamName1] [points1]",
              "[teamName2] [points2]'")
    return None


def parseTextInput(input: List[Any]) -> List[MatchEntry]:
    """
    Gets the entry as iterable, and maps to a MatchEntry
    if an element of the input can't be creates as MatchEntry,
    filter fom return list

    Parameters
    ----------
    inout: List[any]
        input to script
    """
    return [_ for _ in map(lambda inputLine: parseTextEntry(inputLine), input)
            if isinstance(_, MatchEntry)]
