class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.p1_name = player1_name
        self.p2_name = player2_name
        self.p1_score = 0
        self.p2_score = 0

    def won_point(self, player_name):
        if self.p1_name == player_name:
            self.p1_score = self.p1_score + 1
        elif self.p2_name == player_name:
            self.p2_score = self.p2_score + 1
        else:
            raise ValueError("Player not found")
    
    def get_score(self):

        if self.is_tied(self.p1_score, self.p2_score):
            return self.return_tied_score(self.p1_score)
        
        if self.p1_score >= 4 or self.p2_score >= 4:
            win_result = self.check_win(self.p1_score, self.p2_score)
            if win_result != 0:
                return win_result
            return self.score_advantage(self.p1_score, self.p2_score)
        else:
            return f"{self.score_to_tennis_score(self.p1_score)}-{self.score_to_tennis_score(self.p2_score)}"
    
    def score_to_tennis_score(self, score):
        score_list = ["Love", "Fifteen", "Thirty", "Forty"]
        return score_list[score]

    def return_tied_score(self, score):
        score_list = ["Love-All", "Fifteen-All", "Thirty-All"]
        if score <= 2:
            return score_list[score]
        return "Deuce"

    def is_tied(self, p1_score, p2_score):
        return p1_score == p2_score

    def score_advantage(self, p1_score, p2_score):
        if p1_score > p2_score:
            return "Advantage player1"
        return "Advantage player2"

    def check_win(self, p1_score, p2_score):
        if p1_score >= p2_score + 2:
            return "Win for player1"
        elif p2_score >= p1_score + 2:
            return "Win for player2"
        else:
            return 0
