from .db import DataBase, get_or_create
from .resources import Resources
from .models import Bar, Ingredient, Glass, Cocktail


class App(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(config.DATABASE_URL)
        self.resources = Resources(config.RESOURCES_DIR)

    def create_bar(self):
        with self.db.session as session:
            bar = get_or_create(session, Bar, id=1)
            session.add(bar)
            session.commit()

    def load_iba_ingredients(self):
        with self.db.session as session:
            ingredients = [
                get_or_create(
                    session, Ingredient,
                    name=name,
                    abv=info["abv"]
                )
                for name, info in self.resources["ingredients"].items()
            ]
            session.add_all(ingredients)
            session.commit()

    def load_iba_cocktails(self):
        with self.db.session as session:
            for recipe in self.resources["recipes"]:
                name = recipe["name"]
                glass = get_or_create(
                    session, Glass,
                    name=recipe["glass"]
                )
                ingredients = [
                    get_or_create(
                        session, Ingredient,
                        name=ingr["ingredient"]
                    )
                    for ingr in recipe["ingredients"]
                    if ingr.get("ingredient") is not None
                ]
                cocktail = get_or_create(
                    session, Cocktail,
                    name=name
                )
                cocktail.glass = glass
                cocktail.ingredients = ingredients
                session.add(cocktail)
            session.commit()
