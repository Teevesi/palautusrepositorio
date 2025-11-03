
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

    def top(self, how_many):
        def sort_by_points(player):
            return player.goals + player.assists

        sorted_players = sorted(
            self._players,
            reverse=True,
            key=sort_by_points
        )

        # Handle the case where how_many is 0
        if how_many <= 0:
            return []

        # Return at most how_many players
        return sorted_players[:min(how_many, len(sorted_players))]
