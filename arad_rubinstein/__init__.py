from otree.api import *
from random import shuffle, randint


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'arad_rubinstein'
    players_per_group = 2
    num_rounds = 1
    small_bonus = 10
    large_bonus = 20

    decision_min = 11
    decision_max = 20

    seconds_for_timed_page = 60 * 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.IntegerField(label="What number will you choose?",
                                   min=Constants.decision_min, max=Constants.decision_max)
    explanation = models.LongStringField(label="")


# FUNCTIONS
def set_groups_for_curr_round(subsession: Subsession):
    size = Constants.players_per_group
    players = subsession.get_players()
    unmatched = [p.participant.id_in_session for p in players if p.participant.vars.get('is_unmatched')]
    active_players = [p.participant.id_in_session for p in players if
                      not p.participant.vars.get('is_dropout') and not p.participant.vars.get('is_unmatched')]
    shuffle(active_players)
    if len(active_players) % 2 == 1:
        unmatched.append(active_players.pop())
    new_matrix = [active_players[n:n+size] for n in range(0, len(active_players), size)]
    if unmatched:
        for p in players:
            if p.participant.id_in_session in unmatched:
                p.participant.vars['is_unmatched'] = True
        new_matrix.append(unmatched)
    dropouts = [p.participant.id_in_session for p in players if p.participant.vars.get('is_dropout')]
    if dropouts:
        new_matrix.append(dropouts)
    subsession.set_group_matrix(new_matrix)


def get_other(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    alter_decision = get_other(player).decision
    if not alter_decision:
        alter_decision = randint(Constants.decision_min, Constants.decision_min)
    payoff = player.decision if player.decision else 0
    payoff += Constants.large_bonus if player.decision == alter_decision - 1 else 0
    payoff += Constants.small_bonus if player.decision == alter_decision else 0
    player.payoff = payoff


# PAGES
class TimedPage(Page):
    timeout_seconds = Constants.seconds_for_timed_page

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars['is_dropout'] = True

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.vars.get('is_dropout'):
            return upcoming_apps[-1]


class MatchingPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_groups_for_curr_round'

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if any(k in player.participant.vars for k in ('is_dropout', 'is_unmatched')):
            return upcoming_apps[-1]


class Decision(Page):
    form_model = "player"
    form_fields = ["decision"]


class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            set_payoff(p)


class Explanation(Page):
    form_model = "player"
    form_fields = ["explanation"]


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        previous_tokens = player.participant.vars.get('tokens_so_far', 0)
        tokens_so_far = previous_tokens + player.payoff
        earnings_so_far = tokens_so_far * player.session.config["real_world_currency_per_point"]
        return dict(
            other_decision=player.get_others_in_group()[0].decision,
            tokens_so_far=tokens_so_far,
            earnings_so_far=earnings_so_far.to_real_world_currency(player.session),
            previous_tokens=previous_tokens
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        previous_tokens = player.participant.vars.get('tokens_so_far', 0)
        tokens_so_far = previous_tokens + player.payoff
        player.participant.payoff = tokens_so_far
        if 'tokens_so_far' in player.participant.vars:
            player.participant.vars['tokens_so_far'] = tokens_so_far


page_sequence = [MatchingPage, Decision, ResultsWaitPage, Explanation, Results]
