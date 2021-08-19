import random
from typing import List

greeting_list: List[str] = [

    '{member} We hope you brought some milk 🥛',
    '{member} Hopped into the server!',
    '{member} Glad to have you here today!',
    'We hope you brought some sweets 🍩 {member}',
    'Have a pizza slice 🍕 {member}',
    '{member} Woooohooo! '
    'We are excited to have you here <a:hyper_cat:809781548210978828>',
    '{member} just joined, hide your cookies!🍪',
    'Swooooooosh! {member} just landed ✈',
    '{member} joined the party <a:party_parrot:810545477668962315>',
    'Roses are red, violets are blue,'
    ' {member} hopped into the server, are they a kangaroo 🦘? ',

]


def greeting(member) -> str:
    return random.choice(greeting_list).format(member)
