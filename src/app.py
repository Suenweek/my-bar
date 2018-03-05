from . import errors
from .db import DataBase, with_session
from .models import Bar, Ingredient, Cocktail
from .helpers import Resources


class App(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(self.config.DATABASE_URL)
        self.resources = Resources(self.config.RESOURCES_DIR)

    @with_session
    def ensure_bar_exists(self, name, session):
        Bar.get_one_or_create(session, name=name)
        session.commit()

    @with_session
    def load_iba_ingredients(self, session):
        ingredients = [
            Ingredient.get_one_or_create(session, name=name)
            for name in self.resources["ingredients"]
        ]
        session.add_all(ingredients)
        session.commit()

    @with_session
    def load_iba_cocktails(self, session):
        for recipe in self.resources["recipes"]:
            name = recipe["name"]
            ingredients = {
                Ingredient.get_one_or_create(session, name=ingr["ingredient"])
                for ingr in recipe["ingredients"]
                if ingr.get("ingredient") is not None
            }
            cocktail = Cocktail.get_one_or_create(session, name=name)
            cocktail.ingredients = ingredients
            session.add(cocktail)
        session.commit()

    @with_session
    def add_bar_ingredient(self, bar_name, ingredient_name, session):
        bar = Bar.get_one_or_create(session, name=bar_name)
        ingredient = session.query(Ingredient)\
                            .filter_by(name=ingredient_name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient not in bar.ingredients:
            bar.ingredients.add(ingredient)
        else:
            raise errors.AlreadyInBarError

        session.commit()

    @with_session
    def list_bar_ingredients(self, bar_name, session):
        bar = Bar.get_one_or_create(session, name=bar_name)
        return bar.ingredients

    @with_session
    def remove_bar_ingredient(self, bar_name, ingredient_name, session):
        bar = Bar.get_one_or_create(session, name=bar_name)
        ingredient = session.query(Ingredient)\
                            .filter_by(name=ingredient_name)\
                            .one_or_none()

        if ingredient is None:
            raise errors.DoesNotExistError

        if ingredient in bar.ingredients:
            bar.ingredients.remove(ingredient)
        else:
            raise errors.NotInBarError

        session.commit()

    @with_session
    def list_available_cocktails(self, bar_name, session):
        bar = Bar.get_one_or_create(session, name=bar_name)
        return [
            cocktail for cocktail
            in session.query(Cocktail).all()
            if bar.can_make(cocktail)
        ]

    @with_session
    def list_most_wanted_ingredients(self, bar_name, limit=None, session=None):
        bar = Bar.get_one_or_create(session, name=bar_name)
        all_ingredients = session.query(Ingredient)
        missing_ingredients = set(all_ingredients) - bar.ingredients
        return sorted(missing_ingredients,
                      key=lambda i: len(i.cocktails),
                      reverse=True)[:limit]
