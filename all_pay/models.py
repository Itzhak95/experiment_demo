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
from groups_matrices import group_matrices
from random import choice, sample, shuffle
from itertools import combinations

import time

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'all_pay'
    players_per_group = None
    num_rounds = 2

    seconds_for_timed_page = 60 * 5

    num_bids = 10
    max_value = 100
    endowment = 200

    bid_steps = [1, 5]
    num_bidders = 2

    four_bidders_group_matrices = [20, 24, 28, 32]


class Subsession(BaseSubsession):
    def get_group_size(self):
        return self.session.config.get('num_bidders', Constants.num_bidders)

    def set_groups_for_all_rounds(self):
        size = self.get_group_size()
        players = [p.participant.id_in_session for p in self.get_players()]
        all_g = [[p for p in g] for g in list(combinations(players, size))]
        #shuffle(all_g)
        self.session.vars['all_pay_all_g'] = all_g

    def set_groups_for_curr_round(self):
        print('******************************************************************************')
        print('CURRENT ROUND =', self.round_number)

        players = self.get_players()
        all_g = self.session.vars['all_pay_all_g']
        active_players = [p.participant.id_in_session for p in players if
                          not p.participant.vars.get('is_dropout') and not p.participant.vars.get('is_unmatched')]
        print('ACTIVE PLAYERS before MATCHING =', active_players)

        all_g_copy = all_g.copy()
        for g in all_g_copy:
            if not all(p in active_players for p in g):
                i = all_g.index(g)
                all_g.pop(i)

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

        to_remove = list()
        for g in all_g:
            all_pairs = list(combinations(g, 2))
            for mg in new_matrix:
                if any(all(p in mg for p in pair) for pair in all_pairs):
                    to_remove.append(g)
                    break
        all_g = [g for g in all_g if g not in to_remove]

        self.session.vars['all_pay_all_g'] = all_g

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

            if all(k in self.session.config for k in ('bid_step', 'num_bidders')):
                bid_step = self.session.config['bid_step']
                num_bidders = self.session.config['num_bidders']
                # Sanity check
                if num_bidders == 5 and bid_step != 1:
                    raise ValueError(f'If number of bidders is {num_bidders}, bid step should be 1.')
            elif any(k in self.session.config for k in ('bid_step', 'num_bidders')):
                raise KeyError(
                    'Number of bidders and bid steps should always be set together in the session configuration.'
                )
            else:
                raise KeyError('Number of bidders and bid steps should always be set in the session configuration.')

        for p in self.get_players():
            if self.round_number == 1:
                if not p.participant.vars.get('tokens_so_far'):
                    p.participant.vars['tokens_so_far'] = Constants.endowment
                p.participant.vars['values_all_pay'] = []
            values = sample(range(Constants.max_value), Constants.num_bids)
            values.sort(reverse=True)
            p.participant.vars['values_all_pay'].append(values)
            for n, v in enumerate(values):
                setattr(p, f'v{n+1}', v)
            p.value = choice(values)


class Group(BaseGroup):

    def set_payoffs(self):
        players = [p for p in self.get_players() if not p.participant.vars.get('is_dropout')]
        players.sort(key=lambda x:x.bid, reverse=True)
        tie = False
        if len(players) > 1:
            tie = players[0].bid == players[1].bid
        for n, p in enumerate(players):
            if n == 0 and not tie:
                p.payoff = p.value - p.bid
                p.is_winner = True
            else:
                p.payoff = - p.bid
                p.is_winner = False


class Player(BasePlayer):
    for n in range(Constants.num_bids):
        locals()[f'b{n+1}'] = models.CurrencyField(label='', min=0, max=Constants.max_value)
        locals()[f'v{n+1}'] = models.IntegerField()
    del n

    value = models.CurrencyField()
    bid = models.CurrencyField()
    is_winner = models.BooleanField()

    answer1 = models.LongStringField(label="")
    answer2 = models.LongStringField(label="")

    def set_bid(self):
        values = self.participant.vars['values_all_pay'][self.round_number-1]
        i = values.index(self.value)
        self.bid = getattr(self, f'b{i+1}')
