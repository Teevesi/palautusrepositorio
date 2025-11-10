import requests
from player import Player
from rich.console import Console
from rich.table import Table

def main():
    user_input = UserInput()
    season = user_input.get_season()
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationalities = reader.get_nationalities()

    user_input = UserInput()

    nationality = user_input.get_nationality(nationalities)

    players = stats.top_scorers_by_nationality(nationality)


    player_table = PlayerTable(players)
    player_table.print_table()

class UserInput:

    def __init__(self):
        pass

    def get_season(self):
        seasons = "[2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26]"
        season = input(f" Choose season: {seasons}")
        return season

    def get_nationality(self, nationalities):
        nationality = input(f" Choose nationality: {nationalities}")
        return nationality


class PlayerReader:

    def __init__(self, url):
        self.url = url
        self.players = []
        self.nationalities = set()
        
    def get_players(self):
        response = requests.get(self.url).json()

        for player in response:
            self.players.append(Player(player))

        return self.players
    
    def get_nationalities(self):
        response = requests.get(self.url).json()

        for player in response:
            self.nationalities.add(player['nationality'])

        formatted_nationalities = f"[{'/'.join(sorted(self.nationalities))}]"

        return formatted_nationalities

class PlayerStats:

    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        filtered_players = [player for player in self.players if player.nationality == nationality]
        filtered_players.sort(key=lambda p: p.goals + p.assists, reverse=True)
        top10 = filtered_players[:10]
        return top10

class PlayerTable:

    def __init__(self,players):
        self.players = players
        self.console = Console()

        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("Name", style="bold dim", width=20)
        self.table.add_column("Teams", style="cyan", width=16)
        self.table.add_column("Goals", justify="right")
        self.table.add_column("Assists", style="white", justify="right")
        self.table.add_column("Points", style="blue",justify="right")

    def print_table(self):
        for player in self.players:
            color = "green" if player.goals >= 20 else "red"
            self.table.add_row(
                player.name,
                player.team,
                f"[{color}]{player.goals}[/{color}]",
                str(player.assists),
                str(player.goals + player.assists)
            )
        self.console.print(self.table)









if __name__ == "__main__":
    main()
