import click
from . import errors
from .app import App
from .context import pass_context
from .helpers import get_config


@click.group(context_settings={
    "auto_envvar_prefix": "MYBAR"
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
    ctx.app.db.create_all()
    ctx.app.bartender.ensure_bar_exists(ctx.bar_name)


@main.command("add")
@click.argument(
    "ingredient-names",
    nargs=-1
)
@pass_context
def bar_add_ingredients(ctx, ingredient_names):
    """Add ingredient(s)."""
    for ingredient_name in ingredient_names:
        try:
            ctx.app.bartender.add_ingredient(ctx.bar_name, ingredient_name)
        except errors.DoesNotExistError:
            ctx.log("Ingredient '{}' does not exist.", ingredient_name)
        except errors.AlreadyInBarError:
            ctx.log("Ingredient '{}' is already in bar.", ingredient_name)


@main.command("ls")
@click.option(
    "-l", "--limit",
    type=click.INT,
    default=5,
    help="Most wanted ingredients limit.",
    show_default=True
)
@pass_context
def list_bar(ctx, limit):
    """List ingredients, available cocktails and most wanted ingredients."""
    bar_ingredients = ctx.app.bartender.list_ingredients(ctx.bar_name)
    if bar_ingredients:
        click.echo("Bar ingredients:")
    for ingredient in bar_ingredients:
        click.secho(ingredient.name, fg="green")

    available_cocktails = ctx.app.bartender.list_cocktails(ctx.bar_name)
    if available_cocktails:
        click.echo("Available cocktails:")
    for cocktail in available_cocktails:
        click.secho(cocktail.name, fg="green")

    most_wanted = ctx.app.bartender.list_wanted_ingredients(
        ctx.bar_name,
        limit=limit
    )
    if most_wanted:
        click.echo("Most wanted ingredients:")
    for ingredient in most_wanted:
        click.secho(ingredient.name, fg="red")


@main.command("rm")
@click.argument(
    "ingredients-names",
    nargs=-1
)
@pass_context
def bar_rm_ingredients(ctx, ingredients_names):
    """Remove ingredient(s)."""
    for ingredient_name in ingredients_names:
        try:
            ctx.app.bartender.remove_ingredient(ctx.bar_name, ingredient_name)
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
    ctx.app.cookbook.load_iba_ingredients()
    ctx.app.cookbook.load_iba_cocktails()


@db.command("reset")
@pass_context
def db_reset(ctx):
    """Drop all tables."""
    ctx.app.db.drop_all()
    ctx.app.db.create_all()
