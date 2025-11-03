import unittest
import os
import sys

# Add the parent directory (src) to the Python path
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.join(dir_path, "..")
sys.path.insert(0, parent_path)

from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def __init__(self):
        self.players = [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

    def get_players(self):
        return self.players

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_player(self):
        # Act
        player = self.stats.search("Semenko")
        # Assert
        self.assertEqual(player.name, "Semenko")

    def test_search_returns_none_for_nonexistent_player(self):
        player = self.stats.search("Selänne")
        self.assertIsNone(player)

    def test_team_returns_correct_players(self):
        edm_players = self.stats.team("EDM")
        
        self.assertEqual(len(edm_players), 3)
        player_names = [player.name for player in edm_players]
        self.assertIn("Semenko", player_names)
        self.assertIn("Kurri", player_names)
        self.assertIn("Gretzky", player_names)

    def test_team_returns_empty_list_for_nonexistent_team(self):
        team_players = self.stats.team("NYR")
        self.assertEqual(len(team_players), 0)

    def test_top_returns_correct_number_of_players(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 3)

    def test_top_returns_players_in_correct_order(self):
        top_players = self.stats.top(5)
        
        self.assertEqual(top_players[0].name, "Gretzky")  # 35 + 89 = 124
        self.assertEqual(top_players[1].name, "Lemieux")  # 45 + 54 = 99
        self.assertEqual(top_players[2].name, "Yzerman") # 42 + 56 = 98
        self.assertEqual(top_players[3].name, "Kurri")   # 37 + 53 = 90
        self.assertEqual(top_players[4].name, "Semenko") # 4 + 12 = 16

    def test_top_handles_zero_players_request(self):
        top_players = self.stats.top(0)
        self.assertEqual(len(top_players), 0)

    def test_top_with_more_players_than_exist(self):
        # Should return all players when requesting more than exist
        top_players = self.stats.top(10)
        self.assertEqual(len(top_players), 5)  # Only 5 players exist in stub