from . import errors
from .db import DataBase, get_or_create, with_session
from .models import Bar, Ingredient, Cocktail
from .helpers import get_config, Resources


class App(object):

    def __init__(self, env):
        self.config = get_config(env)
        self.db = DataBase(self.config.DATABASE_URL)
        self.resources = Resources(self.config.RESOURCES_DIR)

    @with_session
    def create_bar(self, session, id):
        bar = get_or_create(session, Bar, id=id)
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
            ingredients = {
                get_or_create(
                    session, Ingredient,
                    name=ingr["ingredient"]
                )
                for ingr in recipe["ingredients"]
                if ingr.get("ingredient") is not None
            }
            cocktail = get_or_create(
                session, Cocktail,
                name=name
            )
            cocktail.ingredients = ingredients
            session.add(cocktail)
        session.commit()

    @with_session
    def add_ingredient(self, session, bar_id, ingredient_name):
        bar = session.query(Bar).get(bar_id)
        ingredient = session.query(Ingredient)\
                            .filter(Ingredient.name == ingredient_name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient not in bar.ingredients:
            bar.ingredients.add(ingredient)
        else:
            raise errors.AlreadyInBarError

        session.commit()

    @with_session
    def list_ingredients(self, session, bar_id):
        return session.query(Bar).get(bar_id).ingredients

    @with_session
    def remove_ingredient(self, session, bar_id, ingredient_name):
        bar = session.query(Bar).get(bar_id)
        ingredient = session.query(Ingredient)\
                            .filter(Ingredient.name == ingredient_name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient in bar.ingredients:
            bar.ingredients.remove(ingredient)
        else:
            raise errors.NotInBarError

        session.commit()

    @with_session
    def list_available_cocktails(self, session, bar_id):
        bar = session.query(Bar).get(bar_id)
        return [
            cocktail for cocktail
            in session.query(Cocktail).all()
            if cocktail.ingredients.issubset(bar.ingredients)
        ]

    @with_session
    def list_most_wanted_ingredients(self, session, bar_id):
        raise NotImplementedError
