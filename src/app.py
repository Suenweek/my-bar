from . import errors
from .db import DataBase, get_or_create, with_session
from .resources import Resources
from .models import Bar, Ingredient, Cocktail


# TODO: Make possible to work on multiple bars
BAR_ID = 1


class App(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(config.DATABASE_URL)
        self.resources = Resources(config.RESOURCES_DIR)

    @with_session
    def create_bar(self, session):
        bar = get_or_create(session, Bar, id=BAR_ID)
        session.add(bar)
        session.commit()

    @with_session
    def load_iba_ingredients(self, session):
        ingredients = [
            get_or_create(
                session, Ingredient,
                name=name
            )
            for name in self.resources["ingredients"]
        ]
        session.add_all(ingredients)
        session.commit()

    @with_session
    def load_iba_cocktails(self, session):
        for recipe in self.resources["recipes"]:
            name = recipe["name"]
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
            cocktail.ingredients = ingredients
            session.add(cocktail)
        session.commit()

    @with_session
    def add_ingredient(self, session, name):
        bar = session.query(Bar).get(BAR_ID)
        ingredient = session.query(Ingredient)\
                            .filter(Ingredient.name == name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient not in bar.ingredients:
            bar.ingredients.append(ingredient)
        else:
            raise errors.AlreadyInBarError

        session.commit()

    @with_session
    def list_ingredients(self, session):
        return session.query(Bar).get(BAR_ID).ingredients

    @with_session
    def remove_ingredient(self, session, name):
        bar = session.query(Bar).get(BAR_ID)
        ingredient = session.query(Ingredient)\
                            .filter(Ingredient.name == name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient in bar.ingredients:
            bar.ingredients.remove(ingredient)
        else:
            raise errors.NotInBarError

        session.commit()
