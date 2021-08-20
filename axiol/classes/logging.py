from datetime import datetime

import colorama
from termcolor import colored


COMMON_LOG_FORMAT: str = "%d/%b/%Y-%Hh:%Mm:%Ss"

colorama.init()


class Logger:

    @staticmethod
    def __log(color, log_type, message) -> None:
        date: str = datetime.now().strftime(COMMON_LOG_FORMAT)

        print(
            f"[{colored(date, 'magenta')}] [{colored(log_type, color=color)}]",
            message, flush=True
        )

    def success(self, message: str) -> None:
        self.__log('green', 'Success', message)

    def inform(self, message: str) -> None:
        self.__log('blue', 'Info', message)

    def warn(self, message: str) -> None:
        self.__log('yellow', 'Warning', message)

    def error(self, message: str) -> None:
        self.__log('red', 'Error', message)

    def db(self, message: str) -> None:
        self.__log('white', 'DB', message)


log = Logger()
