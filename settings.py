from os import environ

SESSION_CONFIGS = [
    dict(
        name='study_all_pay_first_price_one_step',
        display_name="Study (All Pay then First Price / 1 Bid Step)",
        num_demo_participants=4,
        app_sequence=['consent', 'survey', 'quiz', 'all_pay', 'quiz_2', 'first_price', 'quiz_3', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='study_all_pay_first_price_five_step',
        display_name="Study (All Pay then First Price / 5 Bid Step)",
        num_demo_participants=4,
        app_sequence=['consent', 'survey', 'quiz', 'all_pay', 'quiz_2', 'first_price', 'quiz_3', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='auction_all_pay',
        display_name="Auction All Pay (for testing)",
        num_demo_participants=4,
        app_sequence=['all_pay', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='auction_first_price',
        display_name="Auction First Price (for testing)",
        num_demo_participants=4,
        app_sequence=['first_price', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='quiz',
        display_name="Quiz 1",
        num_demo_participants=1,
        app_sequence=['quiz', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='quiz_2',
        display_name="Quiz 2",
        num_demo_participants=1,
        app_sequence=['quiz_2', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='quiz_3',
        display_name="Quiz 3",
        num_demo_participants=1,
        app_sequence=['quiz_3', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='bret',
        display_name="BRET",
        num_demo_participants=1,
        app_sequence=['bret'],
        num_bidders=2,
        bid_step=1
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.03, participation_fee=3.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'

ROOMS = [
    dict(
        name='virtual_lab',
        display_name='Virtual Lab',
        participant_label_file='_rooms/virtual_lab.txt'
    )
]


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = ')my6dfz_+dj3uql9xb*2s-bfuuga6s5#w9fden#^7@s^j_p*fa'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
