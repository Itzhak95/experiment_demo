from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from random import randint
from otree.api import Submission


class PlayerBot(Bot):
    def play_round(self):
        if not any(k in self.participant.vars for k in ('is_dropout', 'is_unmatched')):
            bids = {f'b{n+1}': randint(0, Constants.max_value) for n in range(Constants.num_bids)}
            if self.participant.id_in_session in [1, 10]:
                yield Submission(pages.Bid, bids, timeout_happened=True)
            else:
                yield pages.Bid, bids
            if not self.participant.vars.get('is_dropout'):
                if self.round_number == 2:
                    yield pages.Question, dict(answer1='Test xxx', answer2='test yyy')
                yield pages.Choice
                yield pages.Results
