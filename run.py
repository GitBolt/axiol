from axiol.core.bot import Bot
from axiol.cogs import cogs


def main() -> None:
    """Main entry point."""
    client = Bot('>>')   # Avoid conflit with Axiol Beta, will be change to `,`.
    client.load_extensions(cogs)
    client.run()


if __name__ == '__main__':
    main()
