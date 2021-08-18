import random


def greeting(member):
    greetinglist = [

        f'{member} We hope you brought some milk 🥛',
        f'{member} Hopped into the server!',
        f'{member} Glad to have you here today!',
        f'We hope you brought some sweets 🍩 {member}',
        f'Have a pizza slice 🍕 {member}',
        f'{member} Woooohooo! '
        f'We are excited to have you here <a:hyper_cat:809781548210978828>',
        f'{member} just joined, hide your cookies!🍪',
        f'Swooooooosh! {member} just landed ✈',
        f'{member} joined the party <a:party_parrot:810545477668962315>',
        'Roses are red, violets are blue,'
        f' {member} hopped into the server, are they a kangaroo 🦘? ',

    ]

    greeting = random.choice(greetinglist)
    return greeting
