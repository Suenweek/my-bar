import click
from . import errors
from .app import App
from .context import pass_context
from .helpers import get_config


@click.group(context_settings={
    "auto_envvar_prefix": "MY_BAR"
})
@click.option(
    "--name",
    default="my-bar",
    show_default=True,
    help="Name of a bar to operate on."
)
@pass_context
def main(ctx, name):
    """
    Helps to manage your bar.
    """
    ctx.bar_name = name

    ctx.app = App(config=get_config())
    ctx.app.ensure_user_data_dir_exists()
    ctx.app.init_db()
    ctx.app.ensure_bar_exists(name=ctx.bar_name)


@main.command("add")
@pass_context
@click.argument("ingredient-names", nargs=-1)
def bar_add_ingredient(ctx, ingredient_names):
    """Add ingredient."""
    for ingredient_name in ingredient_names:
        try:
            ctx.app.add_bar_ingredient(ctx.bar_name, ingredient_name)
        except errors.DoesNotExistError:
            ctx.log("Ingredient '{}' does not exist in db.", ingredient_name)
        except errors.AlreadyInBarError:
            ctx.log("Ingredient '{}' is already in bar.", ingredient_name)


@main.command("ls")
@pass_context
def list_bar(ctx):
    """List ingredients and available cocktails."""
    bar_ingredients = ctx.app.list_bar_ingredients(ctx.bar_name)
    if bar_ingredients:
        click.echo("Bar ingredients:")
    for ingredient in bar_ingredients:
        click.secho(ingredient.name, fg="green")

    available_cocktails = ctx.app.list_available_cocktails(ctx.bar_name)
    if available_cocktails:
        click.echo("Available cocktails:")
    for cocktail in available_cocktails:
        click.secho(cocktail.name, fg="green")

    most_wanted = ctx.app.list_most_wanted_ingredients(
        ctx.bar_name,
        limit=5  # FIXME: Add CLI option instead of hard-coded value
    )
    if most_wanted:
        click.echo("Most wanted ingredients:")
    for ingredient in most_wanted:
        click.secho(ingredient.name, fg="red")


@main.command("rm")
@pass_context
@click.argument("ingredient-names", nargs=-1)
def bar_rm_ingredient(ctx, ingredient_names):
    """Remove ingredient."""
    for ingredient_name in ingredient_names:
        try:
            ctx.app.remove_bar_ingredient(ctx.bar_name, ingredient_name)
        except errors.DoesNotExistError:
            ctx.log("Ingredient '{}' does not exist in db.", ingredient_name)
        except errors.NotInBarError:
            ctx.log("Ingredient '{}' is not in bar.", ingredient_name)


@main.group()
def db():
    """Database management."""


@db.command("iba")
@pass_context
def db_load_iba(ctx):
    """Load IBA cocktails and ingredients."""
    ctx.app.load_iba_ingredients()
    ctx.app.load_iba_cocktails()


@db.command("reset")
@pass_context
def db_reset(ctx):
    """Drop all tables."""
    ctx.app.drop_db()
    ctx.app.init_db()
