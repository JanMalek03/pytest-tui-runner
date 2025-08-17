import click


@click.group()
def cli():
    """CLI pro pytest-gui plugin."""


@cli.command()
def run():
    """Spustí TUI."""
    print("Spouštím TUI...")
