"""
    A simple consoled based logging utility.

    Example usage:
        >>> from logging import log

        >>> log.success("Connected to the cookie generator.")
        >>> log.inform("Sigmanificient took generated a cookie.")
        >>> log.warn("No more cookies can be generated due to empty Stack.")
        >>> log.error("Missing cookie generator key.")
        >>> log.db(
        >>> ...     "Attempting `select cookie from user where user_name = ?"
        >>> ...     "with args ?= `Sigmanificient`"
        >>> ... )

"""

from datetime import datetime

import colorama
from termcolor import colored

COMMON_LOG_FORMAT: str = "%d/%b/%Y-%Hh:%Mm:%Ss"

colorama.init()


class Logger:
    """The utility class for easy and beautiful logging.

    This class should not be instantiated.
    Instead use the log instance given in the module.
    """

    @staticmethod
    def __log(color, log_type, message) -> None:
        date: str = datetime.now().strftime(COMMON_LOG_FORMAT)

        print(
            f"[{colored(date, 'magenta')}] [{colored(log_type, color=color)}]",
            message, flush=True
        )

    def success(self, message: str) -> None:
        """Log a successful operation.

        :param message: str
            details of the operation.
        """
        self.__log('green', 'Success', message)

    def inform(self, message: str) -> None:
        """Log a informative or debug message.

        :param message: str
            details of the message.
        """
        self.__log('blue', 'Info', message)

    def warn(self, message: str) -> None:
        """Log a unexpected behavior that isn't fatal.

        :param message:
            Failure details or error __cause__.
        """
        self.__log('yellow', 'Warning', message)

    def error(self, message: str, fatal: bool = True) -> None:
        """Log a operation fail or missing core element
            causing instabilities to run or reducing available features.

        :param fatal:
            Whether the program can continue to run or not.

        :param message:
            Failure details, error __cause__ and/or solve hint.
        """
        self.__log('red', 'Error', message)

        if fatal:
            quit()

    def db(self, message: str) -> None:
        """Log a db call.

        :param message:
            Query string or result.
        """
        self.__log('white', 'DB', message)


log = Logger()
