from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint


class TimedPage(Page):
    timeout_seconds = Constants.seconds_for_timed_page

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['is_dropout'] = True

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('is_dropout'):
            return upcoming_apps[-1]


class Page1(TimedPage):
    def vars_for_template(self):
        num_bidders = self.session.config['num_bidders']
        bid_step = self.session.config['bid_step']
        return dict(num_bidders=num_bidders, bid_step=bid_step)


class Page2(TimedPage):
    def vars_for_template(self):
        num_bidders = self.session.config['num_bidders']
        return dict(num_bidders=num_bidders)


class Page3(TimedPage):
    pass


class Question1(TimedPage):
    form_model = 'player'
    form_fields = ['q1']

    def vars_for_template(self):
        num_bidders = self.session.config['num_bidders']
        return dict(num_bidders=num_bidders)

class Answer(TimedPage):
    pass


class Question2(TimedPage):
    form_model = 'player'
    form_fields = ['q2a', 'q2b', 'q2c']

    live_method = 'live_quiz'

    def vars_for_template(self):
        num_bidders = self.session.config['num_bidders']
        self.participant.vars['q'] = self.player.set_quiz_q()
        return dict(q=self.participant.vars['q'], num_bidders=num_bidders)


class Correct(TimedPage):
    pass


class FinalPage(TimedPage):
    pass


page_sequence = [
    Page1, Page2, Page3,
    Question1, Answer,
    Question2, Correct, FinalPage]
