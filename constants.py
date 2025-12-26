from fractions import Fraction

RANK = [0, 16, 32, 48, 64, 80, 96, 112, 120, 128, 136, 152, 168, 176, 200, 203, 206, 208, 211, 214, 216, 222, 224, 224]
ACHV = [0, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 750000, 799999, 800000,
        900000, 940000, 969999, 970000, 980000, 989999, 990000, 995000, 999999, 1000000, 1004999, 1005000, 1010000]
DIFF_NAME_MAPPING = ['BASIC', 'ADVANCED', 'EXPERT', 'MASTER', 'Re:MASTER']
DIFF_EMOJI = [':green_square:', ':yellow_square:', ':red_square:', ':purple_square:',
             ':white_large_square:']
LEVEL_LIST = ['1', '2', '3', '4', '5', '6', '7', '7+',
                '8', '8+', '9', '9+', '10', '10+', '11', '11+',
              '12', '12+', '13', '13+', '14', '14+', '15']

DIFFICULTY_MAPPING = {
    'bas': 0,
    'basic': 0,
    'adv': 1,
    'advanced': 1,
    'exp': 2,
    'expert': 2,
    'mas': 3,
    'master': 3,
    'rem': 4,
    'remas': 4,
    'remaster': 4,
}

NOTE_NAMES = [
    'Tap',
    'Normal',
    'EX',
    'Hold',
    'Normal',
    'EX',
    'Touch Hold',
    'Slide',
    'Touch',
    'Break',
    'Tap',
    'EXTap',
    'Hold',
    'EXHold',
    'Slide'
]

NOTE_MULTIPLIER_BY_INDEX = {
    0: 1,
    3: 2,
    7: 3,
    8: 1,
    9: 5
}

KALEIDX_DIFF_SCALE = {
    '0': 'LIFE1/MASTER',
    '1': 'LIFE10/MASTER',
    '2': 'LIFE30/MASTER',
    '3': 'LIFE50/MASTER',
    '4': 'LIFE100/EXPERT',
    '5': 'LIFE999/BASIC',
}
KALEIDX_GATE_COLOR = {
    'blue': 1,
    'white': 2,
    'purple': 3,
    'violet': 3,
    'black': 4,
    'yellow': 5,
    'red': 6,
    'tower': 7,
    'prism_tower': 7,
    'prism': 7,
    '7sref': 7,
}
KALEIDX_EX_DIFF_SCALE = {
    '0': '- LIFE: 1/100\n'
         '- Damage: -1/-10/-20/-50\n'
         '- Difficulty: Re:MASTER',
    '1': '- LIFE: 1/**200**\n'
         '- Damage: -1/-10/-20/-50\n'
         '- Difficulty: Re:MASTER',
    '2': '- LIFE: **5**/**300**\n'
         '- Damage: -1/-10/-20/-50\n'
         '- Difficulty: Re:MASTER',
    '3': '- LIFE: 5/**400**\n'
         '- Damage: -1/-10/-20/-50\n'
         '- Difficulty: Re:MASTER',
    '4': '- LIFE: **10**/**500**\n'
         '- Damage: -1/-10/-20/-50\n'
         '- Difficulty: Re:MASTER',
    '5': '- LIFE: 10/500\n'
         '- Damage: -1/**-5**/**-10**/**-30**\n'
         '- Difficulty: Re:MASTER',
    '6': '- LIFE: **30**/500\n'
         '- Damage: -1/-5/-10/-30\n'
         '- Difficulty: Re:MASTER',
    '7': '- LIFE: 30/500\n'
         '- Damage: -1/-5/-10/-30\n'
         '- Difficulty: **MASTER**',
    '8': '- LIFE: 30/500\n'
         '- Damage: -1/-5/-10/**-20**\n'
         '- Difficulty: MASTER',
    '9': '- LIFE: **50**/**600**\n'
         '- Damage: -1/-5/-10/-20\n'
         '- Difficulty: MASTER',
    '10': '- LIFE: **100**/**700**\n'
         '- Damage: -1/**-3**/**-5**/**-10**\n'
         '- Difficulty: MASTER',
    '11': '- LIFE: 100/**999**\n'
         '- Damage: -1/-3/-5/-10\n'
         '- Difficulty: **EXPERT**',
    '12': '- LIFE: **999**/999\n'
         '- Damage: -1/-3/-5/-10\n'
         '- Difficulty: **BASIC**',
}

# Colors
PERFECT = "\u001b[0;33m"
GREAT = "\u001b[0;35m"
GOOD = "\u001b[0;36m"
MISS = "\u001b[0;0m"
NOTE_LABEL = "\u001b[0;34m"
DIFF_COLOR = [4571428, 16759297, 16737882, 10441180, 14396159]

# Emojis
STD_EMOJI = "<:std1:1339878288671244288><:std2:1339878300981526610><:std3:1339878312750874634>"
DX_EMOJI = "<:dx1:1339878735201042452><:dx2:1339878743224619090><:dx3:1339878753165381672>"

TITLE_RARITY_COLOR = {
    'Normal': 16777215,
    'Bronze': 13468978,
    'Silver': 12632256,
    'Gold': 16766720,
    'Rainbow': 32768
}

OTOMODACHI_RANK_MAPPING = {
    'S': '97.0000%',
    'S+': '98.0000%',
    'SS': '99.0000%',
    'SS+': '99.5000%',
    'SSS': '100.0000%',
    'SSS+': '100.5000%',
    'MAX': '101.0000%'
}

# For damage
REGULAR_NOTE_RATIO = [Fraction(1, 1), Fraction(1, 1), Fraction(4, 5), Fraction(1, 2), 0]
NOTE_TYPE_MULT = [1, 2, 3, 1]

BREAK_BASE_MULT = [0,
                   0, 0,
                   1, 2, Fraction(5, 2),
                   3,
                   5]

BREAK_BONUS_MULT = [0,
                    Fraction(1, 4), Fraction(1, 2),
                    Fraction(3, 5), Fraction(3, 5), Fraction(3, 5),
                    Fraction(7, 10),
                    1]
