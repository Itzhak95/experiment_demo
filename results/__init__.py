from otree.api import *

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'results'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback = models.LongStringField(
        label='Are there any ways in which the experiment could be improved? For example, '
              'were any of the instructions unclear?'
    )


# PAGES
class Dropout(Page):
    @staticmethod
    def is_displayed(player: Player):
        return True if player.participant.vars.get('is_dropout') else False


class Results(Page):
    def vars_for_template(player: Player):
        previous_tokens = player.participant.vars.get('tokens_so_far', 0)
        tokens_so_far = previous_tokens + player.payoff
        earnings_so_far = tokens_so_far
        return dict(
            tokens_so_far=tokens_so_far,
            earnings_so_far=earnings_so_far.to_real_world_currency(player.session),
            previous_tokens=previous_tokens
        )


page_sequence = [Dropout, Results]
