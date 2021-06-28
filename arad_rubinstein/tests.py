from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from random import randint


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Decision, dict(decision=randint(Constants.decision_min, Constants.decision_max))
        yield pages.Explanation, dict(explanation='test')
        yield pages.Results
