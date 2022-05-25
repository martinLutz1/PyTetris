class Player:
    score: int = 0

    def add_to_score(self, points: int):
        self.score += points

    def reset(self):
        self.score = 0
