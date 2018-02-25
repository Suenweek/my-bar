import click
import config
from . import errors
from .app import App


pass_app = click.make_pass_decorator(App)


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = App(config=config)


@main.command("add")
@pass_app
@click.argument("ingredient")
def add_ingredient(app, ingredient):
    """Add new ingredient to bar."""
    try:
        app.add_ingredient(name=ingredient)
    except errors.DoesNotExistError:
        click.echo("Ingredient '{}' does not exist.".format(ingredient))
    except errors.AlreadyInBarError:
        click.echo("Ingredient '{}' is already in bar.".format(ingredient))


@main.command("list")
@pass_app
def list_ingredients(app):
    """List ingredients in bar."""
    for i in app.list_ingredients():
        click.echo(i)


@main.command("rm")
@pass_app
@click.argument("ingredient")
def remove_ingredient(app, ingredient):
    """Remove ingredient from bar."""
    try:
        app.remove_ingredient(name=ingredient)
    except errors.DoesNotExistError:
        click.echo("Ingredient '{}' does not exist.".format(ingredient))
    except errors.NotInBarError:
        click.echo("Ingredient '{}' is not in bar.".format(ingredient))


@main.group()
def db():
    """Bar database management."""


@db.command()
@pass_app
@click.option("--iba/--no-iba", default=True)
def init(app, iba):
    """Create all tables, bar instance and load IBA cocktails."""
    app.db.create_all()
    app.create_bar()
    if iba:
        app.load_iba_ingredients()
        app.load_iba_cocktails()


@db.command()
@pass_app
@click.pass_context
def reset(ctx, app):
    """Drop all tables and init again."""
    app.db.drop_all()
    ctx.invoke(init)
