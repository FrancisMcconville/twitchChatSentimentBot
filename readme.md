# Twitch Chat Sentiment Analyzer
Analyzes twitch chat messages for their sentiment and hype. \
Written for python 3.5, using Vaders sentiment analysis \
\
Django project must be run with --noreload flag: `manage.py runserver --noreload`\
Vader Sentiment Analysis Lexicon can be updated in settings.py by updating TWITCH_LEXICON\
\
Basic Lexicon contains following values:

    '<3': 0.4,
    '4head': 1,
    'babyrage': -0.7,
    'biblethump': -0.7,
    'blessrng': 0.3,
    'bloodtrail': 0.7,
    'coolstorybob': -1,
    'residentsleeper': -1,
    'kappa': -0.3,
    'lul': -0.3,
    'pogchamp': 1.5,
    'heyguys': 1,
    'wutface': -1.5,
    'kreygasm': 1,
    'seemsgood': 0.7,
    'kappapride': 0.7,
    'feelsgoodman': 1,
    'notlikethis': -1
    
Chat messages are logged to chat_log.log, along with a sentiment rating for each message in the format "#channel [sentiment] user: message" eg:\
`[DEBUG] twitch: #beyondthesummit: [-0.6037] hayashidayuki: RIGGED GAME BibleThump` 