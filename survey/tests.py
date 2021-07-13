from otree.api import Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Tokens
        yield Time
        yield Questions, dict(age="18", gender="Female", subject="Social Sciences")
