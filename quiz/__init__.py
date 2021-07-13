from otree.api import *
from random import choice, randrange

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1

    max_value = 100
    seconds_for_timed_page = 60 * 5

    bid_step = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(label="")
    q2a = models.BooleanField(
        label="Do you win the auction?",
        choices=[(True, "Yes"), (False, "No")],
        widget=widgets.RadioSelect
    )
    q2b = models.IntegerField(label="How many tokens do you win (you may enter 0)?")
    q2c = models.IntegerField(label="How many tokens does your opponent win (you may enter 0)?")
    q3a = models.BooleanField(
        label="Do you win the auction?",
        choices=[(True, "Yes"), (False, "No")],
        widget=widgets.RadioSelect
    )
    q3b = models.IntegerField(label="How many tokens do you win (you may enter 0)?")
    q3c = models.IntegerField(label="How many tokens does your opponent win (you may enter 0)?")


# FUNCTIONS
def live_quiz(player: Player, data):
    is_next_q = data['is_next_q']
    print('is_next_q =', is_next_q)
    alter_bid_cancelled = data['alter_bid_cancelled']
    if is_next_q:
        player.participant.vars['q'] = set_quiz_q(player, alter_bid_cancelled)
        errors = dict()
        is_next_q = False
    else:
        errors = quiz_error_message(player, data['values'], alter_bid_cancelled)
        print('errors =', errors)
        is_next_q = True
    return {player.id_in_group: dict(question=player.participant.vars['q'], errors=errors, is_next_q=is_next_q)}


def set_quiz_q(player: Player, alter_bid_cancelled):
    bid_step = player.session.config['bid_step']
    ego_v = choice(list(range(bid_step * 2, Constants.max_value + 1)))
    alter_v = choice(list(range(bid_step * 1, Constants.max_value + 1)))
    if alter_bid_cancelled:
        alter_b = choice(list(range(bid_step * 1, alter_v, bid_step)))
        ego_b = choice(list(range(0, min(alter_b, ego_v), bid_step)))
    else:
        ego_b = choice(list(range(bid_step * 1, ego_v, bid_step)))
        alter_b = choice(list(range(0, min(ego_b, alter_v), bid_step)))
    return dict(ego_v=ego_v, ego_b=ego_b, alter_v=alter_v, alter_b=alter_b)


def quiz_error_message(player: Player, values, alter_bid_cancelled):
    q = player.participant.vars['q']
    fields = list(values.keys())
    a = [True, q['ego_v'] - q['ego_b'], 0]
    if not alter_bid_cancelled:
        if q['ego_b'] < q['alter_b']:
            a = [False, 0, q['alter_v'] - q['alter_b']]
    corrects = {k: v for k, v in zip(fields, a)}
    if alter_bid_cancelled:
        msg = {fields[0]: f"Since your opponent’s bid was cancelled but yours was not, you win the auction.",
               fields[1]: f"Since you win the auction, you receive your valuation of {q['ego_v']} minus "
                          f"your bid of {q['ego_b']} tokens, or {q['ego_v'] - q['ego_b']} tokens.",
               fields[2]: 'Since your opponent loses the auction, they don’t gain any tokens (so the answer is 0).'}
    else:
        msg = {fields[0]: f"Since you bid {q['ego_b']} and your opponent only bid {q['alter_b']}, "
                          f"you win the auction.",
               fields[1]: f"Since you win the auction, you receive your valuation of {q['ego_v']} minus your bid "
                          f"of {q['ego_b']} tokens, or {q['ego_v'] - q['ego_b']} tokens.",
               fields[2]: 'Since your opponent loses the auction, they don’t gain any tokens (so the answer is 0).'}
    errors = dict()
    for k in values.keys():
        if values[k] != corrects[k]:
                errors[k] = msg[k]
    return errors


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


class QuestionN(TimedPage):
    template_name = 'quiz/QuestionN.html'
    form_model = 'player'

    live_method = live_quiz


class Page1(TimedPage):
    pass


class Page2(TimedPage):
    pass


class Page3(TimedPage):
    @staticmethod
    def vars_for_template(player: Player):
        bid_step = player.session.config['bid_step']
        return dict(bid_step=bid_step)


class Page4(TimedPage):
    pass


class Page5(TimedPage):
    @staticmethod
    def vars_for_template(player: Player):
        value = randrange(player.session.config['bid_step'], 100, 1)
        bid = randrange(0, value, player.session.config['bid_step'])
        net = value - bid
        return dict(value=value, bid=bid, net=net)


class Page6(TimedPage):
    @staticmethod
    def vars_for_template(player: Player):
        bid_step = player.session.config['bid_step']
        return dict(bid_step=bid_step)


class Page7(TimedPage):
    pass


class Question1(TimedPage):
    form_model = 'player'
    form_fields = ['q1']


class Answer1(TimedPage):
    pass


class Question2(QuestionN):
    form_fields = ['q2a', 'q2b', 'q2c']

    @staticmethod
    def vars_for_template(player: Player):
        alter_bid_cancelled = False
        player.participant.vars['q'] = set_quiz_q(player, alter_bid_cancelled)
        return dict(q=player.participant.vars['q'], alter_bid_cancelled=alter_bid_cancelled)


class Correct(Page):
    pass


class Question3(QuestionN):
    form_fields = ['q3a', 'q3b', 'q3c']

    @staticmethod
    def vars_for_template(player: Player):
        alter_bid_cancelled = True
        player.participant.vars['q'] = set_quiz_q(player, alter_bid_cancelled)
        return dict(q=player.participant.vars['q'], alter_bid_cancelled=alter_bid_cancelled)


class FinalPage(TimedPage):
    @staticmethod
    def vars_for_template(player: Player):
        value = randrange(player.session.config['bid_step'], 100, 1)
        bid = randrange(0, value, player.session.config['bid_step'])
        return dict(value=value, bid=bid)


page_sequence = [
    Page1, Page2, Page3, Page4, Page5, Page6, Page7,
    Question1, Answer1,
    Question2, Correct, Question3, Correct, FinalPage
]
