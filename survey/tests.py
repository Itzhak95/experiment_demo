from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Welcome
        yield pages.Tokens
        yield pages.Time
        yield pages.Questions, dict(age="18", gender="Female", subject="Social Sciences")
