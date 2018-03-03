import click
from . import errors
from .app import App
from .context import pass_context


@click.group(context_settings={
    "auto_envvar_prefix": "MY_BAR"
})
@click.option(
    "-e", "--env",
    type=click.Choice(["test", "prod"]),
    default="prod",
    help="Environment to use."
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose mode."
)
@click.option(
    "--bar-id",
    type=click.INT,
    default=1,
    show_default=True,
    help="Id of a bar to operate on."
)
@pass_context
def main(ctx, env, verbose, bar_id):
    """
    Helps to manage your bar.
    """
    ctx.env = env
    ctx.verbose = verbose
    ctx.app = App(env)
    ctx.bar_id = bar_id


@main.command("add")
@pass_context
@click.argument("ingredient-name")
def add_ingredient(ctx, ingredient_name):
    """Add new ingredient to bar."""
    try:
        ctx.app.add_ingredient(ctx.bar_id, ingredient_name)
    except errors.DoesNotExistError:
        ctx.log("Ingredient '{}' does not exist in db.", ingredient_name)
    except errors.AlreadyInBarError:
        ctx.log("Ingredient '{}' is already in bar.", ingredient_name)


@main.command("ls")
@pass_context
@click.option(
    "-f", "--filter",
    type=click.Choice(["ingredients", "cocktails"]),
    default=["ingredients", "cocktails"],
    multiple=True
)
def list_ingredients(ctx, filter):
    """List bar ingredients and available cocktails."""
    for item in filter:
        if item == "ingredients":
            for ingredient in ctx.app.list_ingredients(ctx.bar_id):
                ctx.log(ingredient)
        elif item == "cocktails":
            for cocktail in ctx.app.list_available_cocktails(ctx.bar_id):
                ctx.log(cocktail)
        else:
            raise RuntimeError("Unreachable.")


@main.command("rm")
@pass_context
@click.argument("ingredient-name")
def remove_ingredient(ctx, ingredient_name):
    """Remove bar ingredient."""
    try:
        ctx.app.remove_ingredient(ctx.bar_id, ingredient_name)
    except errors.DoesNotExistError:
        ctx.log("Ingredient '{}' does not exist in db.", ingredient_name)
    except errors.NotInBarError:
        ctx.log("Ingredient '{}' is not in bar.", ingredient_name)


@main.group()
def db():
    """Bar database management."""


@db.command()
@pass_context
def init(ctx):
    """Create all tables, bar instance."""
    ctx.app.db.create_all()
    ctx.app.create_bar(id=ctx.bar_id)


@db.command()
@pass_context
def iba(ctx):
    """Load IBA cocktails and ingredients."""
    ctx.app.load_iba_ingredients()
    ctx.app.load_iba_cocktails()


@db.command()
@pass_context
def drop(ctx):
    """Drop all tables."""
    ctx.app.db.drop_all()
