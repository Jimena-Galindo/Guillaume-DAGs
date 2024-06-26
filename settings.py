from os import environ


SESSION_CONFIGS = [
    dict(
        name='Part1_Part2',
        num_demo_participants=2,
        app_sequence=['Part1', 'Part2', 'Pay']
    ),

    dict(
        name='Extra6',
        num_demo_participants=2,
        app_sequence=['Part1', 'Part2ExtraGuesses', 'Pay']
    ),
]

ROOMS = [
    dict(
        name='econ_lab',
        display_name='Lab',
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = ['notes', 'cases_ordered', 'realized_cases', 'light_list', 'guesses', 'order_names', 'sound',
                      'current_case', 'original_color']

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '2516807391076'

INSTALLED_APPS = ['otree']
