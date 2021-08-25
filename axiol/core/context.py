from axiol.utils.chronometer import Chronometer
from discord.ext.commands import Context


class TimedContext(Context):

    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.time: Chronometer = Chronometer()
