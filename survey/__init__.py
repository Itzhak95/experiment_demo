from otree.api import *

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    # Payment parameters
    endowment = cu(200)
    exchange_rate = 0.01

    seconds_for_timed_page = 60 * 5


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['endowment'] = Constants.endowment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_dropout = models.BooleanField()
    age = models.IntegerField(label = "What is your age (in years)?", min=18, max=80)
    gender = models.StringField(
        label="What is your gender?",
        choices=["Male", "Female", "Other", "Prefer not to say"],
        widget=widgets.RadioSelect
    )
    subject = models.StringField(
        label="Into what division does your subject fall?",
        choices=["Humanities", "Social Sciences", "Medical Sciences", "Mathematical, Physical and Life Sciences"],
        widget=widgets.RadioSelect
    )


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


class Welcome(Page):
    pass


class Tokens(Page):
    pass


class Time(Page):
    pass


class Questions(TimedPage):
    form_model = "player"
    form_fields = ["age", "gender", "subject"]


page_sequence = [Welcome, Tokens, Time, Questions]
