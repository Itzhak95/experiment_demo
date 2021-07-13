from otree.api import Bot, Submission
from . import *
from random import randint


class PlayerBot(Bot):
    def play_round(self):
        if not any(k in self.participant.vars for k in ('is_dropout', 'is_unmatched')):
            bids = {f'b{n+1}': randint(0, Constants.max_value) for n in range(Constants.num_bids)}
            if self.participant.id_in_session in [10, 2] and self.round_number == 2:
                yield Submission(Bid, bids, timeout_happened=True)
            else:
                yield Bid, bids
            if not self.participant.vars.get('is_dropout'):
                if self.round_number == 2:
                    yield Question, dict(answer1='Test xxx', answer2='test yyy')
                yield Choice
                yield Results
