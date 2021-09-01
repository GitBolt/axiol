from axiol.core.bot import Bot
from axiol.cogs import cogs


def main() -> None:
    """Main entry point."""
    bot = Bot(';')   # Avoid conflit with Axiol Beta, will be change to `,`.
    bot.load_extensions(cogs)
    bot.run()


if __name__ == '__main__':
    main()
