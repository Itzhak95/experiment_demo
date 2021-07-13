from otree.api import *



author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1

    seconds_for_timed_page = 60 * 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


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


class ConsentForm(TimedPage):
    pass


page_sequence = [ConsentForm]
