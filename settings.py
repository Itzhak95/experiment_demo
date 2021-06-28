from os import environ

SESSION_CONFIGS = [
    dict(
        name='study_first_price_all_pay_two_bidders_five_step',
        display_name="Study (First Price - All Pay / 2 Bidders - 5 Bid Step)",
        num_demo_participants=8,
        app_sequence=['consent', 'survey', 'quiz', 'first_price', 'quiz_3', 'all_pay', 'quiz_2', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='study_all_pay_first_price_two_bidders_five_step',
        display_name="Study (All Pay - First Price / 2 Bidders - 5 Bid Step)",
        num_demo_participants=4,
        app_sequence=['consent', 'survey', 'quiz', 'all_pay', 'quiz_2', 'first_price', 'quiz_3', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='study_first_price_all_pay_four_bidders_one_step',
        display_name="Study (First Price - All Pay / 4 Bidders - 1 Bid Step)",
        num_demo_participants=16,
        app_sequence=['consent', 'survey', 'quiz', 'first_price', 'quiz_3', 'all_pay', 'quiz_2', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=4,
        bid_step=1
    ),
    dict(
        name='study_all_pay_first_price_four_bidders_one_step',
        display_name="Study (All Pay - First Price / 4 Bidders - 1 Bid Step)",
        num_demo_participants=16,
        app_sequence=['consent', 'survey', 'quiz', 'all_pay', 'quiz_2', 'first_price', 'quiz_3', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=4,
        bid_step=1
    ),
    dict(
        name='study_first_price_all_pay_two_bidders_one_step',
        display_name="Study (First Price - All Pay / 2 Bidders - 1 Bid Step)",
        num_demo_participants=8,
        app_sequence=['consent', 'survey', 'quiz', 'first_price', 'quiz_3', 'all_pay', 'quiz_2', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='study_all_pay_first_price_two_bidders_one_step',
        display_name="Study (All Pay - First Price / 2 Bidders - 1 Bid Step)",
        num_demo_participants=8,
        app_sequence=['consent', 'survey', 'quiz', 'all_pay', 'quiz_2', 'first_price', 'quiz_3', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=1
    ),
    dict(
        name='study_all_pay_first_price_two_bidders_five_step_testing',
        display_name="Study (All Pay - First Price / 2 Bidders - 5 Bid Step / for testing)",
        num_demo_participants=8,
        app_sequence=['consent', 'survey', 'all_pay', 'first_price', 'arad_rubinstein', 'bret', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='auction_all_pay',
        display_name="Auction All Pay (for testing)",
        num_demo_participants=4,
        app_sequence=['all_pay', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='auction_first_price',
        display_name="Auction First Price (for testing)",
        num_demo_participants=8,
        app_sequence=['first_price', 'results'],
        num_bidders=2,
        bid_step=5
    ),
    dict(
        name='all_auctions',
        display_name="All Auctions (for testing)",
        num_demo_participants=8,
        app_sequence=['first_price', 'all_pay', 'arad_rubinstein', 'results'],
        num_bidders=2,
        bid_step=5,
        use_browser_bots=True
    ),
    dict(
        name='quizzes',
        display_name="Quiz 1-3",
        num_demo_participants=1,
        app_sequence=['quiz', 'quiz_2', 'quiz_3', 'results'],
        num_bidders=4,
        bid_step=5
    ),
    dict(
        name='quiz_2',
        display_name="Quiz 2",
        num_demo_participants=1,
        app_sequence=['quiz_2', 'results'],
        num_bidders=4,
        bid_step=5
    ),
    dict(
        name='quiz_3',
        display_name="Quiz 3",
        num_demo_participants=1,
        app_sequence=['quiz_3', 'results'],
        num_bidders=4,
        bid_step=5
    ),
    dict(
        name='bret',
        display_name="BRET",
        num_demo_participants=1,
        app_sequence=['bret'],
        num_bidders=4,
        bid_step=5
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.2, participation_fee=3.00, doc=""
)

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
