from otree.api import Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        for page in page_sequence:
            if page == Question1:
                yield page, dict(q1=1)
            else:
                yield page
