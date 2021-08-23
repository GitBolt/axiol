from core.bot import Bot


def main() -> None:
    """Main entry point."""
    client = Bot('>>')   # Avoid conflit with Axiol Beta, will be change to `,`.
    client.run()


if __name__ == '__main__':
    main()
