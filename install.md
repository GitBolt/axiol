# Install (for devs)

*Makes sure to have the right python > 3.7 and mongodb 4.0 first!*

1 - download the files from the repository 
```git
git clone https://github.com/GitBolt/Axiol
```

2 - Setup your python environment:
- Create a python venv
- **Or** a pipenv
- **Or** build the docker image.

**Only if you are using a venv** - Install the required packages in your python intepreter or venv
```py
python -m pip install requirements.txt
```

3 - Fill the secrets:
- Adds the `TOKEN` and `MONGO_DB_URL` to your environment variables
- **Or** cope the `.env.example` to `.env` and and complte it.

4 - Runs `db_setup.py` (in `axiol/functions`)
```py
python -m db_setup.py
```

5 - Runs the `run.py` module.
```py
python -m main.py
```
