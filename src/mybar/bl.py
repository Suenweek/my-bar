from . import errors
from .models import Bar, Ingredient, Cocktail


class BlBase(object):

    def __init__(self, app):
        self.app = app


class Bartender(BlBase):

    def ensure_bar_exists(self, bar_name):
        with self.app.db.session_scope() as session:
            Bar.get_one_or_create(session, name=bar_name)
            session.commit()

    def add_ingredient(self, bar_name, ingredient_name):
        with self.app.db.session_scope() as session:
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

    def list_ingredients(self, bar_name):
        with self.app.db.session_scope() as session:
            bar = Bar.get_one_or_create(session, name=bar_name)
            return bar.ingredients

    def remove_ingredient(self, bar_name, ingredient_name):
        with self.app.db.session_scope() as session:
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

    def list_wanted_ingredients(self, bar_name, limit=None):
        with self.app.db.session_scope() as session:
            bar = Bar.get_one_or_create(session, name=bar_name)
            all_ingredients = session.query(Ingredient)
            missing_ingredients = set(all_ingredients) - bar.ingredients
            return sorted(missing_ingredients,
                          key=lambda i: len(i.cocktails),
                          reverse=True)[:limit]

    def list_cocktails(self, bar_name):
        with self.app.db.session_scope() as session:
            bar = Bar.get_one_or_create(session, name=bar_name)
            return [cocktail for cocktail
                    in session.query(Cocktail).all()
                    if bar.can_make(cocktail)]


class CookBook(BlBase):

    def load_iba_ingredients(self):
        with self.app.db.session_scope() as session:
            ingredients = [
                Ingredient.get_one_or_create(session, name=name)
                for name in self.app.resources["ingredients"]
            ]
            session.add_all(ingredients)
            session.commit()

    def load_iba_cocktails(self):
        with self.app.db.session_scope() as session:
            for recipe in self.app.resources["recipes"]:
                name = recipe["name"]
                ingredients = {
                    Ingredient.get_one_or_create(session,
                                                 name=ingr["ingredient"])
                    for ingr in recipe["ingredients"]
                    if ingr.get("ingredient") is not None
                }
                cocktail = Cocktail.get_one_or_create(session, name=name)
                cocktail.ingredients = ingredients
                session.add(cocktail)
            session.commit()
