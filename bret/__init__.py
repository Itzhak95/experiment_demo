from otree.api import *

import random

from .config import Constants

author = 'Felix Holzmeister & Armin Pfurtscheller'

doc = """
Bomb Risk Elicitation Task (BRET) à la Crosetto/Filippin (2013), Journal of Risk and Uncertainty (47): 31-65.
"""


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bomb = models.IntegerField()
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()
    boxes_collected = models.IntegerField()
    pay_this_round = models.BooleanField()
    round_result = models.CurrencyField()


# FUNCTIONS
def set_payoff(player: Player):

    # determine round_result as (potential) payoff per round
    if player.bomb:
        player.round_result = cu(0)
    else:
        player.round_result = player.boxes_collected * Constants.box_value

    # set payoffs if <random_payoff = True> to round_result of randomly chosen round
    # randomly determine round to pay on player level
    if player.round_number == 1:
        player.participant.vars['round_to_pay'] = random.randint(1, Constants.num_rounds)

    if Constants.random_payoff:
        if player.round_number == player.participant.vars['round_to_pay']:
            player.pay_this_round = True
            player.payoff = player.round_result
        else:
            player.pay_this_round = False
            player.payoff = cu(0)

    # set payoffs to round_result if <random_payoff = False>
    else:
        player.payoff = player.round_result


# PAGES
class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'num_rows':             Constants.num_rows,
            'num_cols':             Constants.num_cols,
            'num_boxes':            Constants.num_rows * Constants.num_cols,
            'num_nobomb':           Constants.num_rows * Constants.num_cols - 1,
            'box_value':            Constants.box_value,
            'time_interval':        Constants.time_interval,
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]

    # BRET settings for Javascript application
    @staticmethod
    def vars_for_template(player: Player):
        reset = player.participant.vars.get('reset', False)
        if reset:
            del player.participant.vars['reset']

        input = not Constants.devils_game if not Constants.dynamic else False

        otree_vars = {
            'reset':            reset,
            'input':            input,
            'random':           Constants.random,
            'dynamic':          Constants.dynamic,
            'num_rows':         Constants.num_rows,
            'num_cols':         Constants.num_cols,
            'num_boxes':        Constants.num_rows * Constants.num_cols,
            'feedback':         Constants.feedback,
            'undoable':         Constants.undoable,
            'box_width':        Constants.box_width,
            'box_height':       Constants.box_height,
            'time_interval':    Constants.time_interval,
        }

        return {
            'otree_vars':       otree_vars
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['reset'] = True
        set_payoff(player)


# ******************************************************************************************************************** #
# *** CLASS RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # only display results after all rounds have been played
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        total_payoff = sum([p.payoff for p in player.in_all_rounds()])
        player.participant.vars['bret_payoff'] = total_payoff

        print(player.participant.vars['bret_payoff'])

        return {
            'player_in_all_rounds':   player.in_all_rounds(),
            'box_value':              Constants.box_value,
            'boxes_total':            Constants.num_rows * Constants.num_cols,
            'boxes_collected':        player.boxes_collected,
            'bomb':                   player.bomb,
            'bomb_row':               player.bomb_row,
            'bomb_col':               player.bomb_col,
            'round_result':           player.round_result,
            'round_to_pay':           player.participant.vars['round_to_pay'],
            'payoff':                 player.payoff,
            'total_payoff':           player.participant.vars['bret_payoff'],
        }


page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)

