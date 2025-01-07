import json
import os


class Leaderboard:
    def __init__(self):
        self.scores = []
        self.leaderboard_file = "leaderboard.json"
        self.load_leaderboard()

    def initialize_default_scores(self):
        default_scores = [
            {"name": "NAV", "score": 20000},
            {"name": "NAV", "score": 15000},
            {"name": "NAV", "score": 10000},
            {"name": "NAV", "score": 5000},
            {"name": "NAV", "score": 1000}
        ]
        return default_scores

    def load_leaderboard(self):
        try:
            if os.path.exists(self.leaderboard_file) and os.path.getsize(self.leaderboard_file) > 0:
                with open(self.leaderboard_file, 'r') as file:
                    self.scores = json.load(file)
            else:
                self.scores = self.initialize_default_scores()
                self.save_leaderboard()

        except (json.JSONDecodeError, FileNotFoundError):
            self.scores = self.initialize_default_scores()
            self.save_leaderboard()

    def save_leaderboard(self):
        with open(self.leaderboard_file, 'w') as file:
            json.dump(self.scores, file)

    def check_high_score(self, score):
        for entry in self.scores[:5]:
            if score > entry["score"]:
                return True
        return len(self.scores) < 5

    def add_score(self, name, score):

        new_entry = {"name": name, "score": score}

        insert_index = len(self.scores)
        for i, entry in enumerate(self.scores):
            if score > entry["score"]:
                insert_index = i
                break

        if insert_index < 5:
            self.scores.insert(insert_index, new_entry)
            self.scores = self.scores[:5]
            self.save_leaderboard()
