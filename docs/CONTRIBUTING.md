# Contributing to this repository

## Getting started

Before you begin:

- Makes sure to have the right python version and the project dependencies
  installed. You also need to have a mongodb server.

### Top priorities

- any kind of bug fixes and optimizations.
- implementing `master` features in the `pkg-rewrite` branch.

### Project Structure

<!-- Not jsonpath, but man the colors! -->
```jsonpath
$
├── .idea
├── .githus
├── assets/                       'img & fonts'
├── docs/                         'Github documentation'
│   ├── AUTHORS.md
│   ├── CONTRIBUTING.md
│   ├── INSTALL.md
│   └── README.md
├── axiol/
│   ├── cogs/
│   │   ├── custom/               'all custom-based/privates cogs'
│   │   ├── handlers/             'main non-user togglabe cogs.'
│   │   │   ├── errors.py
│   │   │   ├── extras.py
│   │   │   ├── help.py
│   │   │   ├── permissions.py
│   │   │   └── settings.py
│   │   └── plugins/              'bot taggable cogs'
│   │       ├── (...)
│   │       └── __init__.py
│   ├── core/                     'base classes that derive the discord.py package'                
│   ├── database/                 'everything related to pymongo db'
│   │   ├── db_setup.py
│   │   └── wrapper.py
│   ├── utils/                    'groups of utilities functions'
│   └── __init__.py
├── tests/                        'python unittest files'
├── .editorconfig
├── (.env)                        'python unittest files'
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── run.py                        'main python script to start the bot'
├── tokei.toml
└── VERSION
```

### Don't see your issue? Open one

If you spot something new, open an issue using the template. We'll use the issue
to have a conversation about the problem you found.

### Make your update

Make your changes to the file(s) you'd like to update to solve an issue or

### Open a pull request

When you're done making changes, and you'd like to propose them for review, use
the pull request template to open your PR (pull request).

- I might take up to 24 hours to get your code reviewed, testing and merged.
- If you remove any feature, or don't pass the basic tests and code style your
  pull request might not get approved and will be asked for modifications.
