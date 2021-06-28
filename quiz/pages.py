from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class TimedPage(Page):
    timeout_seconds = Constants.seconds_for_timed_page

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['is_dropout'] = True

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('is_dropout'):
            return upcoming_apps[-1]


class QuestionN(TimedPage):
    template_name = 'quiz/QuestionN.html'
    form_model = 'player'

    live_method = 'live_quiz'


class Page1(TimedPage):
    pass


class Page2(TimedPage):
    pass


class Page3(TimedPage):
    def vars_for_template(self):
        bid_step = self.session.config['bid_step']
        return dict(bid_step=bid_step)


class Page4(TimedPage):
    pass


class Page5(TimedPage):
    def vars_for_template(self):
        value = random.randrange(self.session.config['bid_step'], 100, 1)
        bid = random.randrange(0, value, self.session.config['bid_step'])
        net = value - bid
        return dict(value=value, bid=bid, net=net)


class Page6(TimedPage):
    def vars_for_template(self):
        bid_step = self.session.config['bid_step']
        return dict(bid_step=bid_step)


class Page7(TimedPage):
    pass


class Question1(TimedPage):
    form_model = 'player'
    form_fields = ['q1']


class Answer1(TimedPage):
    pass


class Question2(QuestionN):
    form_fields = ['q2a', 'q2b', 'q2c']

    def vars_for_template(self):
        alter_bid_cancelled = False
        self.participant.vars['q'] = self.player.set_quiz_q(alter_bid_cancelled)
        return dict(q=self.participant.vars['q'], alter_bid_cancelled=alter_bid_cancelled)


class Correct(Page):
    pass


class Question3(QuestionN):
    form_fields = ['q3a', 'q3b', 'q3c']

    def vars_for_template(self):
        alter_bid_cancelled = True
        self.participant.vars['q'] = self.player.set_quiz_q(alter_bid_cancelled)
        return dict(q=self.participant.vars['q'], alter_bid_cancelled=alter_bid_cancelled)


class FinalPage(TimedPage):
    def vars_for_template(self):
        value = random.randrange(self.session.config['bid_step'], 100, 1)
        bid = random.randrange(0, value, self.session.config['bid_step'])
        return dict(value=value, bid=bid)


page_sequence = [
    Page1, Page2, Page3, Page4, Page5, Page6, Page7,
    Question1, Answer1,
    Question2, Correct, Question3, Correct, FinalPage
]
