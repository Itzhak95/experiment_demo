from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class TimedPage(Page):
    timeout_seconds = Constants.seconds_for_timed_page

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['is_dropout'] = True

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('is_dropout'):
            return upcoming_apps[-1]


class Welcome(Page):
    pass


class Tokens(Page):
    pass


class Time(Page):
    pass


class Questions(TimedPage):
    form_model = "player"
    form_fields = ["age", "gender", "subject"]


page_sequence = [Welcome, Tokens, Time, Questions]
