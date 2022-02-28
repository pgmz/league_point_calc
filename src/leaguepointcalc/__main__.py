from leaguepointcalc.input_parser import parseTextInput
from leaguepointcalc.league_status import LeagueStatus
from leaguepointcalc.cli_aux import parse_parameters


def main():
    matchEntries = parseTextInput(parse_parameters())
    leagueStatus = LeagueStatus()
    leagueStatus.addMatchEntries(matchEntries)
    leagueStatus.printLeaderBoard(leagueStatus.leaderBoard)


if __name__ == "__main__":
    main()
