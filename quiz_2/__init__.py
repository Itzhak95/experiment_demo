from otree.api import *
from random import randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz_2'
    players_per_group = None
    num_rounds = 1

    seconds_for_timed_page = 60 * 5
    qa_label = "How many tokens do you receive?"
    qb_label = "How many tokens does your opponent receive?"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1a = models.IntegerField(label=Constants.qa_label)
    q1b = models.IntegerField(label=Constants.qb_label)
    q2a = models.IntegerField(label=Constants.qa_label)
    q2b = models.IntegerField(label=Constants.qb_label)


# FUNCTIONS
def live_quiz(player: Player, data):
    is_next_q = data['is_next_q']
    if is_next_q:
        player.participant.vars['q'] = set_quiz_q(data['question_n'])
        errors = dict()
        is_next_q = False
    else:
        errors = quiz_error_message(player, data['values'], data['question_n'])
        is_next_q = True
    return {player.id_in_group: dict(question=player.participant.vars['q'], errors=errors, is_next_q=is_next_q)}


def set_quiz_q(question_n):
    if question_n == 1:
        alter_c = randint(13, 20)
        ego_c = alter_c - 2
    elif question_n == 2:
        alter_c = randint(13, 20)
        ego_c = alter_c - 1
    return dict(ego_c=ego_c, alter_c=alter_c)


def quiz_error_message(player: Player, values, question_n):
    q = player.participant.vars['q']
    fields = list(values.keys())
    if question_n == 1:
        corrects = dict(q1a=10 * q['ego_c'], q1b=10 * q['alter_c'])
    elif question_n == 2:
        corrects = dict(q2a=10 * q['ego_c'] + 200, q2b=10 * q['alter_c'])
    msg_1 = {
        fields[0]: f"In this case, you simply receive the number that you chose multiplied by 10. "
                   f"So you receive {10*q['ego_c']} tokens.",
        fields[1]: f"In this case, your opponent simply receives the number that they chose "
                   f"multiplied by 10. So they receive {10*q['alter_c']} tokens."}
    msg_2 = {
        fields[0]: f'As always, you receive the number that you chose multiplied by 10. '
                   f'However, since the number you chose is exactly one less than the number '
                   f'chosen by your opponent, you receive a bonus of 200 tokens. '
                   f'So you receive {10 * q["ego_c"]} + 200 = {10 * q["ego_c"] + 200} tokens in total.',
        fields[1]: f'Once again, your opponent simply receives the number that you '
                   f'chose multiplied by 10. So they receive {10*q["alter_c"]} tokens.'}
    msg = msg_1 if fields[0] == 'q1a' else msg_2
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


class Intro(TimedPage):
    pass


class Page1(TimedPage):
    def vars_for_template(self):
        x = randint(11, 20)
        return dict(x=x, y=10*x)


class Page2(TimedPage):
    pass


class Question1(TimedPage):
    form_model = 'player'
    form_fields = ['q1a', 'q1b']

    live_method = live_quiz

    @staticmethod
    def vars_for_template(player: Player):
        question_n = 1
        player.participant.vars['q'] = set_quiz_q(question_n)
        return dict(q=player.participant.vars['q'], question_n=question_n, alter_bid_cancelled=False)


class Correct(TimedPage):
    pass


class Question2(TimedPage):
    form_model = 'player'
    form_fields = ['q2a', 'q2b']

    live_method = 'live_quiz'

    @staticmethod
    def vars_for_template(player: Player):
        question_n = 2
        player.participant.vars['q'] = set_quiz_q(question_n)
        return dict(q=player.participant.vars['q'], question_n=question_n, alter_bid_cancelled=False)


page_sequence = [Intro, Page1, Page2, Question1, Correct, Question2, Correct]
