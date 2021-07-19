from otree.api import *
from random import choice, sample, randint
from itertools import combinations

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'first_price'
    players_per_group = None
    num_rounds = 2

    seconds_for_timed_page = 60 * 5

    num_bids = 10
    max_value = 100
    endowment = 100

    bid_steps = [1, 5]
    num_bidders = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    for n in range(Constants.num_bids):
        locals()[f'b{n+1}'] = models.CurrencyField(label='', min=0, max=Constants.max_value)
        locals()[f'v{n+1}'] = models.IntegerField()
    del n

    value = models.CurrencyField()
    bid = models.CurrencyField()
    cancelled = models.BooleanField()
    is_winner = models.BooleanField()

    answer1 = models.LongStringField(label="")
    answer2 = models.LongStringField(label="")


# FUNCTIONS
def set_groups_for_all_rounds(subsession: Subsession):
    size = Constants.num_bidders
    players = [p.participant.id_in_session for p in subsession.get_players()]
    all_g = [[p for p in g] for g in list(combinations(players, size))]
    # shuffle(all_g)
    subsession.session.vars['first_price_all_g'] = all_g


def set_groups_for_curr_round(subsession: Subsession):

    print('******************************************************************************')
    print('CURRENT ROUND =', subsession.round_number)

    players = subsession.get_players()
    all_g = subsession.session.vars['first_price_all_g']
    active_players = [p.participant.id_in_session for p in players if
                      not p.participant.vars.get('is_dropout') and not p.participant.vars.get('is_unmatched')]
    print('ACTIVE PLAYERS before MATCHING =', active_players)

    all_g_copy = all_g.copy()
    for g in all_g_copy:
        if not all(p in active_players for p in g):
            i = all_g.index(g)
            all_g.pop(i)
    print('ALL GROUPS after FILTERING =', all_g)

    new_matrix = []
    all_g_copy = all_g.copy()
    while all_g_copy:
        all_g_flat = [p for g in all_g_copy for p in g]
        counts = {p: all_g_flat.count(p) for p in active_players if p in all_g_flat}
        next_p = min(counts, key=counts.get)
        next_pg = iter(g for g in all_g_copy if next_p in g)
        next_g = next(next_pg)

        # Condition
        while next_pg:

            next_next_g = next(next_pg, [])
            len_all_g_if_next_g = len([g for g in all_g_copy if not any(p in g for p in next_g)])
            len_all_g_if_next_next_g = len(
                [g for g in all_g_copy if not any(p in g for p in next_next_g)]) if next_next_g else 0
            if len_all_g_if_next_g >= len_all_g_if_next_next_g:
                break
            else:
                next_g = next_next_g
                break

        i = all_g.index(next_g)
        new_matrix.append(all_g.pop(i))
        all_g_copy = [g for g in all_g_copy if not any(p in g for p in next_g)]

    subsession.session.vars['first_price_all_g'] = all_g

    unmatched = [p.participant.id_in_session for p in players if p.participant.vars.get('is_unmatched')]
    new_unmatched = [p for p in active_players if p not in [p for g in new_matrix for p in g]]
    if new_unmatched:
        for p in players:
            if p.participant.id_in_session in new_unmatched:
                p.participant.vars['is_unmatched'] = True
        unmatched.extend(new_unmatched)
    if unmatched:
        new_matrix.append(unmatched)

    dropouts = [p.participant.id_in_session for p in players if p.participant.vars.get('is_dropout')]
    if dropouts:
        new_matrix.append(dropouts)

    print('UNMATCHED and DROPOUTS =', unmatched, dropouts)

    print('NEW MATRIX =', new_matrix)
    print('******************************************************************************')

    subsession.set_group_matrix(new_matrix)


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        set_groups_for_all_rounds(subsession)

    for p in subsession.get_players():
        if subsession.round_number == 1:
            if not p.participant.vars.get('tokens_so_far'):
                p.participant.vars['tokens_so_far'] = Constants.endowment
            p.participant.vars['values_first_price'] = []
        values = sample(range(Constants.max_value), Constants.num_bids)
        values.sort(reverse=True)
        p.participant.vars['values_first_price'].append(values)
        for n, v in enumerate(values):
            setattr(p, f'v{n+1}', v)
        p.value = choice(values)
        c = randint(0, 1)
        p.cancelled = c


def set_bid(player: Player):
    values = player.participant.vars['values_first_price'][player.round_number-1]
    i = values.index(player.value)
    player.bid = getattr(player, f'b{i+1}')


def get_other(player: Player):
    return player.get_others_in_group()[0]


# TODO: this method should be moved to the Group class
def set_payoff(player: Player):
    alter = get_other(player)
    alter_bid = alter.bid if alter.bid else 0
    if player.cancelled == 1:
        player.is_winner = False
    else:
        if alter.cancelled == 1 and player.bid:
            player.is_winner = True
        else:
            if player.bid:
                player.is_winner = True if player.bid > alter_bid else False
            else:
                player.is_winner = False
    player.payoff = player.value - player.bid if player.is_winner else 0


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


class MatchingPage (WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_groups_for_curr_round'

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if any(k in player.participant.vars for k in ('is_dropout', 'is_unmatched')):
            return upcoming_apps[-1]


class Bid(TimedPage):
    form_model = 'player'
    form_fields = [f'b{n+1}' for n in range(Constants.num_bids)]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(bid_step=player.session.config['bid_step'],
                    values=player.participant.vars['values_first_price'][player.round_number-1])

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        super(Bid, Bid).before_next_page(player, timeout_happened)
        set_bid(player)


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p.set_payoff()


class Question(TimedPage):
    form_model = 'player'
    form_fields = ['answer1', 'answer2']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Choice(TimedPage):
    pass


class Results(TimedPage):

    @staticmethod
    def vars_for_template(player: Player):
        previous_tokens = player.participant.vars['tokens_so_far']

        other_bids = [str(p.bid) for p in player.get_others_in_group()]
        return dict(
            payoff_abs=abs(player.payoff),
            tokens_so_far=previous_tokens + player.payoff,
            previous_tokens=previous_tokens,
            other_bids=', '.join(other_bids)
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        super(Bid, Bid).before_next_page(player, timeout_happened)
        player.participant.vars['tokens_so_far'] += player.payoff


page_sequence = [MatchingPage, Bid, ResultsWaitPage, Question, Choice, Results]
