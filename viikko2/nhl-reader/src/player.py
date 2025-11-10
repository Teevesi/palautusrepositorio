
class Player:
    def __init__(self, dict_players):
        self.name = dict_players['name']
        self.nationality = dict_players['nationality']
        self.team = dict_players['team']
        self.goals = dict_players['goals']
        self.assists = dict_players['assists']
        self.games = dict_players['games']

    def __str__(self):
        score = f"{self.goals:>2} + {self.assists:>2} = {self.goals + self.assists:>2}"
        return f"{self.name:20} {self.team:16} {score}"

    def hmm(self):
        pass
