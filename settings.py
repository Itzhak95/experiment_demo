from os import environ

SESSION_CONFIGS = [
    dict(
        name='study_one_step',
        display_name="Main treatment (integer bids)",
        num_demo_participants=4,
        app_sequence=['survey', 'quiz', 'first_price', 'quiz_3', 'all_pay', 'quiz_2', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='study_five_step',
        display_name="Alternate treatment (multiples)",
        num_demo_participants=4,
        app_sequence=['survey', 'quiz', 'first_price', 'quiz_3', 'all_pay', 'quiz_2', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=5
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.05, participation_fee=2.00, doc="", OTREE_PRODUCTION=1,
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
        name='virtual_lab_1',
        display_name='Virtual Lab 1',
        participant_label_file='_rooms/virtual_lab_1.txt'
    ),
    dict(
        name='virtual_lab_2',
        display_name='Virtual Lab 2',
        participant_label_file='_rooms/virtual_lab_2.txt'
    ),
]


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = ')my6dfz_+dj3uql9xb*2s-bfuuga6s5#w9fden#^7@s^j_p*fa'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
