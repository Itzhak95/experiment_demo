from otree.api import Bot, Submission, SubmissionMustFail
from . import *


class PlayerBot(Bot):

    def play_round(self):
        yield Decision, dict(decision=randint(Constants.decision_min, Constants.decision_max))
        yield Explanation, dict(explanation='test')
        yield Results
