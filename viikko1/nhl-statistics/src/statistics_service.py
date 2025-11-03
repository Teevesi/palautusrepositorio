from enum import Enum

class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3

class StatisticsService:
    def __init__(self, reader):

        self._players = reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name):
        players_of_team = filter(
            lambda player: player.team == team_name,
            self._players
        )

        return list(players_of_team)

    def top(self, how_many, method=SortBy.POINTS):
        # Handle the case where how_many is 0
        if how_many <= 0:
            return []

        # Define sort key based on method
        if method == SortBy.GOALS:
            sort_key = lambda player: player.goals
        elif method == SortBy.ASSISTS:
            sort_key = lambda player: player.assists
        else:  # default to POINTS
            sort_key = lambda player: player.goals + player.assists

        # Sort players using the selected key
        sorted_players = sorted(
            self._players,
            reverse=True,
            key=sort_key
        )

        # Return at most how_many players
        return sorted_players[:min(how_many, len(sorted_players))]
