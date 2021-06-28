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


class MatchingPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_groups_for_curr_round'

    def app_after_this_page(self, upcoming_apps):
        if any(k in self.participant.vars for k in ('is_dropout', 'is_unmatched')):
            return upcoming_apps[-1]


class Decision(TimedPage):
    form_model = "player"
    form_fields = ["decision"]


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Explanation(TimedPage):
    form_model = "player"
    form_fields = ["explanation"]


class Results(TimedPage):
    def vars_for_template(self):
        previous_tokens = self.participant.vars.get('tokens_so_far', 0)
        tokens_so_far = previous_tokens + self.player.payoff
        earnings_so_far = tokens_so_far * self.session.config["real_world_currency_per_point"]
        return dict(tokens_so_far=tokens_so_far, earnings_so_far=earnings_so_far.to_real_world_currency(self.session),
                    previous_tokens=previous_tokens)

    def before_next_page(self):
        previous_tokens = self.participant.vars.get('tokens_so_far', 0)
        tokens_so_far = previous_tokens + self.player.payoff
        self.participant.payoff = tokens_so_far
        print('*********', tokens_so_far, '*************')


page_sequence = [MatchingPage, Decision, ResultsWaitPage, Explanation, Results]
