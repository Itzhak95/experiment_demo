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


class Intro(TimedPage):
    pass


class Page1(TimedPage):
    def vars_for_template(self):
        x = randint(11, 20)
        return dict(x=x, y=10*x)


class Page2(TimedPage):
    pass


class Question1(TimedPage):
    form_model = 'player'
    form_fields = ['q1a', 'q1b']

    live_method = 'live_quiz'

    def vars_for_template(self):
        question_n = 1
        self.participant.vars['q'] = self.player.set_quiz_q(question_n)
        return dict(q=self.participant.vars['q'], question_n=question_n)


class Correct(TimedPage):
    pass


class Question2(TimedPage):
    form_model = 'player'
    form_fields = ['q2a', 'q2b']

    live_method = 'live_quiz'

    def vars_for_template(self):
        question_n = 2
        self.participant.vars['q'] = self.player.set_quiz_q(question_n)
        return dict(q=self.participant.vars['q'], question_n=question_n)


page_sequence = [Intro, Page1, Page2, Question1, Correct, Question2, Correct]
