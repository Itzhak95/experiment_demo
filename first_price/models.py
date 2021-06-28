from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from random import randint

from random import choice, sample, shuffle
from itertools import combinations



author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'first_price'
    players_per_group = None
    num_rounds = 5

    seconds_for_timed_page = 60 * 5

    num_bids = 5
    max_value = 100
    endowment = 200

    bid_steps = [1, 5]
    num_bidders = 2


class Subsession(BaseSubsession):
    def set_groups_for_all_rounds(self):
        size = Constants.num_bidders
        players = [p.participant.id_in_session for p in self.get_players()]
        all_g = [[p for p in g] for g in list(combinations(players, size))]
        # shuffle(all_g)
        self.session.vars['first_price_all_g'] = all_g

    def set_groups_for_curr_round(self):

        print('******************************************************************************')
        print('CURRENT ROUND =', self.round_number)

        players = self.get_players()
        all_g = self.session.vars['first_price_all_g']
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

        self.session.vars['first_price_all_g'] = all_g

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

        self.set_group_matrix(new_matrix)

    def creating_session(self):
        if self.round_number == 1:
            self.set_groups_for_all_rounds()

        for p in self.get_players():
            if self.round_number == 1:
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

    def set_bid(self):
        values = self.participant.vars['values_first_price'][self.round_number-1]
        i = values.index(self.value)
        self.bid = getattr(self, f'b{i+1}')

    def get_other(self):
        return self.get_others_in_group()[0]

    # TODO: this method should be moved to the Group class
    def set_payoff(self):
        alter = self.get_other()
        alter_bid = alter.bid if alter.bid else 0
        if self.cancelled == 1:
            self.is_winner = False
        else:
            if alter.cancelled == 1 and self.bid:
                self.is_winner = True
            else:
                if self.bid:
                    self.is_winner = True if self.bid > alter_bid else False
                else:
                    self.is_winner = False
        self.payoff = self.value - self.bid if self.is_winner else 0
