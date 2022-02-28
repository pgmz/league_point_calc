from enum import Enum
from typing import Dict, List, Tuple
from leaguepointcalc.input_parser import MatchEntry, TeamEntry


class MatchResult(Enum):
    """
    Enum class for match result points.

    Methods
    -------
    matchResult(points1:int, points2: int) -> MatchResult
        compares points1 and points2, and defines if
        points1 is WIN, LOSS or DRAW
    """
    WIN = 3
    LOSS = 0
    DRAW = 1

    @staticmethod
    def matchResult(points1: int, points2: int):
        """
        Returns wether team 1 is WIN, LOSS or DRAW

        Parameters
        -------
        points1: int
            game points of first team
        points2: int
            game points of second team
        """
        return (MatchResult.WIN if points1 > points2
                else (MatchResult.LOSS if points1 < points2
                      else MatchResult.DRAW))


class TeamMatchResult():
    """
    Wrapper class for TeamEntry, which has the actual match result for entry

    Attributes
    -------
    matchId: str
        id for match from where the points are
    matchResult: MatchResult
        match result for this team (WIN, LOSS or DRAW)
    teamEntry: TeamEntry
        information of team (name, gamePoints)
    """
    matchId: str
    matchResult: MatchResult
    teamEntry: TeamEntry

    def __init__(self, matchId: str, teamEntry: TeamEntry,
                 matchResult: MatchResult):
        """
        Parameters
        ----------
        matchId: str
            id for match from where the points and results are
        teamEntry: TeamEntry
            information of the team (name, gamePoints)
        matchResult: MatchResult
            result of the team int the match (WIN, LOSS or DRAW)
        """
        self.matchId = matchId
        self.teamEntry = teamEntry
        self.matchResult = matchResult


class TeamStatus:
    """
    Class to keep track of the status of a team
    has total gamePoints and matchPoints,
    and the list of entries where this team
    has participated

    Attributes
    -------
    totalMatchPoints: int
        total match points (from WIN, LOSS or DRAW) points
    totalGamePoints: int
        total game points (from input)
    teamMatchEntries: List[TeamMatchResult]
        list of teamMatchResults where the team has participated
    """
    totalMatchPoints: int
    totalGamePoints: int
    teamMatchEntries: List[TeamMatchResult]

    def __init__(self, totalMatchPoints=0, totalGamePoints=0,
                 teamMatchEntries=[]):
        """
        Parameters
        ----------
        totalMatchPoints: int
            accumulated match points for a team (default is 0)
        totalGamePoints: int
            accumulated game points for a team (default is 0)
        teamMatchEntries: List[TeamMatchResult]
            entries where the team has participated (default is [])
        """
        self.totalMatchPoints = totalMatchPoints
        self.totalGamePoints = totalGamePoints
        self.teamMatchEntries = teamMatchEntries

    def addMatchResult(self, teamMatchResult: TeamMatchResult):
        """
        Adds a TeamMatchResult to the team status history

        Parameters
        ----------
        teamMatchResult: TeamMatchResult
            new Team match result object to be added
            to team status history
        """
        # add new gamePoints to accumulated gamePoints
        self.totalGamePoints = (self.totalGamePoints +
                                teamMatchResult.teamEntry.gamePoints)
        # add new matchPoints to accumulated matchPoints
        self.totalMatchPoints = (self.totalMatchPoints +
                                 teamMatchResult.matchResult.value)
        # add new teamMatchResult to status list
        self.teamMatchEntries.append(teamMatchResult)


class LeagueStatus:
    """
    Class to keep track of the league,
    has a dictionary of teams with their points and status
    has a dictionary of points that is used to print leaderBoard

    Attributes
    -------
    teamStatus: Dict[str, TeamStatus]
        Dict where key is teamName and value is TeamStatus
    leaderBoard: Dict[int, List[str]]
        Dict where key is totalMatchPoints and
        value is a list of teamName
    """
    teamStatus: Dict[str, TeamStatus] = {}
    leaderBoard: Dict[int, List[str]] = {}

    def getTeamMatchResult(self,
                           matchEntry: MatchEntry) -> Tuple[TeamMatchResult,
                                                            TeamMatchResult]:
        """
        get the teams from the matchEntry and return as TeamMatchResult,
        which indicates if team WIN, LOSS or DRAW

        Parameters
        -------
        matchEntry : MatchEntry
            matchEntry input
        """
        team1, team2 = matchEntry.teams
        team1Result = MatchResult.matchResult(team1.gamePoints,
                                              team2.gamePoints)
        team2Result = MatchResult.matchResult(team2.gamePoints,
                                              team1.gamePoints)
        return (TeamMatchResult(matchEntry.matchId, team1, team1Result),
                TeamMatchResult(matchEntry.matchId, team2, team2Result))

    def addMatchEntries(self, matchEntries: List[MatchEntry]):
        """
        Gets the teams from a matchEntry,
        and adds them to the team status

        Parameters
        -------
        matchEntries : List[MatchEntry]
            list of match entries from input
        """
        # for each matchEntry, get the match results
        for matchEntry in matchEntries:
            teamStatus1, teamStatus2 = self.getTeamMatchResult(matchEntry)
            # for each match result, update the status
            for team in [teamStatus1, teamStatus2]:
                self.updateTeamStatus(team)

    # have a leaderboard updated
    def updateLeaderBoard(self, teamName: str, prevMatchPoints: int,
                          currentMatchPoints: int):
        """
        update the self leaderboard, by removing teamName from
        previous matchPoints key and adding to current matchPoints.
        This can be called continuously to keep self leaderboard updated

        Parameters
        -------
        teamName: str
            teamName to be updated in the leaderboard
        prevMatchPoints: int
            previous Match Points of team
        currentMatchPoints: int
            current Match Points of team
        """
        # check if points exist in leaderboard
        if prevMatchPoints not in self.leaderBoard:
            self.leaderBoard[prevMatchPoints] = []
        if currentMatchPoints not in self.leaderBoard:
            self.leaderBoard[currentMatchPoints] = []
        # remove team from dictionary at previous points,
        # and add at new points
        if teamName in self.leaderBoard[prevMatchPoints]:
            self.leaderBoard[prevMatchPoints].remove(teamName)
        self.leaderBoard[currentMatchPoints].append(teamName)

    def updateTeamStatus(self, teamMatchResult: TeamMatchResult):
        """
        add teamMatchResult and points to team status

        Parameters
        -------
        teamMatchResult: TeamMatchResult
            team result for the match,
            indicates if team has WIN, LOSS or DRAW points
        """
        # get team name, and add to teamStatus dictionary
        teamName = teamMatchResult.teamEntry.teamName
        if teamName not in self.teamStatus:
            self.teamStatus[teamName] = TeamStatus()

        # keep track of prev and current points to update the leaderboard
        prevMatchPoints = self.teamStatus[teamName].totalMatchPoints
        self.teamStatus[teamName].addMatchResult(teamMatchResult)
        currentMatchPoints = self.teamStatus[teamName].totalMatchPoints
        self.updateLeaderBoard(teamName, prevMatchPoints, currentMatchPoints)

    def generateLeaderBoardFromTeamStatus(self) -> Dict[int, List[str]]:
        """
        generate leaderBoard from teamStatus.
        This can be called to generate leaderboard once
        """
        matchPoints: Dict[int, List[str]] = {}
        # save teams based on the scores
        for team in self.teamStatus:
            teamMatchPoints = self.teamStatus[team].totalMatchPoints
            if teamMatchPoints not in matchPoints:
                matchPoints[teamMatchPoints] = []
            matchPoints[teamMatchPoints].append(team)
        return matchPoints

    def printLeaderBoard(self, leaderBoard: Dict[int, List[str]]):
        """
        add teamMatchResult and points to team status

        Parameters
        -------
        leaderBoard : Dict[int, List[str]]
            leader board is a dictionary where the key are the match points,
            and value is the list of teams that have those match points
        """
        # rank Carry, is used for teams that have the same rank
        rankCarry = 1
        # enumerate rank and matchpoints
        for rank, matchPoint in enumerate(sorted(leaderBoard, reverse=True)):
            # sort teams in that have matchPoints
            leaderBoard[matchPoint].sort()
            for team in self.leaderBoard[matchPoint]:
                print(str(rank+rankCarry) + ".",
                      team + ",", matchPoint, " pts")
            # increase rankCarry
            rankCarry = rankCarry + len(leaderBoard[matchPoint]) - 1
