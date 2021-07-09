import discord

class Level:

    def __init__(self, id: int, name: str, creator:str):
        
        self.id = id
        self.name = name
        self.creator = creator

        self.attempts = 0
        self.jumps = 0
        self.difficulty = 0

        self.percent = 0
        self.best_percent = 0

        self.rating = 0
        self.featured = False
        self.epic = False

        self.practice_mode = False
        self.practice_best = 0
        
    def is_practice_mode(self):
        return self.practice_mode

    def is_featured(self):
        return self.featured

    def is_epic(self):
        return self.featured

class Session:

    def __init__(self):

        self.start_attempts = 0
        self.old_best = 0
        self.best = 0