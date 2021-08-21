from axiol.bot import Bot


def main() -> None:
    """Main entry point."""
    client = Bot()
    client.run('>>')  # Avoid conflit with Axiol Beta, will be change to `,`.


if __name__ == '__main__':
    main()
