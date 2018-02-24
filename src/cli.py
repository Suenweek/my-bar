import click
import config
from .app import App


pass_app = click.make_pass_decorator(App)


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = App(config=config)


@main.group()
def db():
    """Bar database management."""


@db.command()
@pass_app
def init(app):
    """Create all tables and bar instance."""
    app.db.create_all()
    app.create_bar()


@db.command()
@pass_app
def drop(app):
    """Drop all tables."""
    app.db.drop_all()


@db.command()
@pass_app
def iba(app):
    """Load ingredients and cocktails from IBA list."""
    app.load_iba_ingredients()
    app.load_iba_cocktails()
