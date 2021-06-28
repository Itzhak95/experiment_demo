from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Page1
        yield pages.Page2
        yield pages.Page3
        yield pages.Page4
        yield pages.Page5
        yield pages.Page6
        yield pages.Page7
        yield pages.Question1, dict(q1=1)
