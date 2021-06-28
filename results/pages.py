from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Dropout(Page):
    def is_displayed(self):
        return True if self.participant.vars.get('is_dropout') else False


class Results(Page):
    form_model = "player"
    form_fields = ["feedback"]


page_sequence = [Dropout, Results]
