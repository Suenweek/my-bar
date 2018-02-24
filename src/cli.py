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


@db.command("create-all")
@pass_app
def create_all(app):
    """Create all tables."""
    app.db.create_all()


@db.command("drop-all")
@pass_app
def drop_all(app):
    """Drop all tables."""
    app.db.drop_all()


@db.command("load-iba")
@pass_app
def load_iba(app):
    """Load ingredients and cocktails from IBA list."""
    app.load_iba_ingredients()
    app.load_iba_cocktails()
