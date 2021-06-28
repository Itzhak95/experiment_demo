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


class MatchingPage (WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_groups_for_curr_round'

    def app_after_this_page(self, upcoming_apps):
        if any(k in self.participant.vars for k in ('is_dropout', 'is_unmatched')):
            return upcoming_apps[-1]


class Bid(TimedPage):
    form_model = 'player'
    form_fields = [f'b{n+1}' for n in range(Constants.num_bids)]

    def vars_for_template(self):
        return dict(bid_step=self.session.config['bid_step'],
                    values=self.participant.vars['values_first_price'][self.round_number-1])

    def before_next_page(self):
        super(self.__class__, self).before_next_page()
        self.player.set_bid()


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Question(TimedPage):
    form_model = 'player'
    form_fields = ['answer1', 'answer2']

    def is_displayed(self):
        return self.round_number == 2


class Choice(TimedPage):
    pass


class Results(TimedPage):
    def vars_for_template(self):
        previous_tokens = self.participant.vars['tokens_so_far']

        other_bids = [str(p.bid) for p in self.player.get_others_in_group()]
        return dict(
            payoff_abs=abs(self.player.payoff),
            tokens_so_far=previous_tokens + self.player.payoff,
            previous_tokens=previous_tokens,
            other_bids=', '.join(other_bids)
        )

    def before_next_page(self):
        self.participant.vars['tokens_so_far'] += self.player.payoff


page_sequence = [MatchingPage, Bid, ResultsWaitPage, Question, Choice, Results]
