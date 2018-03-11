import pytest
from mybar import errors
from mybar.bl import Bartender, CookBook
from mybar.models import Bar, Ingredient, Cocktail


class TestBartender(object):

    def test_ensure_non_existent_bar_exists(self, app):
        with app.db.session_scope() as session:
            assert session.query(Bar).count() == 0

        bartender = Bartender(app=app)
        bartender.ensure_bar_exists("test")

        with app.db.session_scope() as session:
            assert session.query(Bar).one().name == "test"

    def test_ensure_existent_bar_exists(self, app):
        with app.db.session_scope() as session:
            assert session.query(Bar).count() == 0
            session.add(Bar(name="test"))
            session.commit()

        bartender = Bartender(app=app)
        bartender.ensure_bar_exists("test")

        with app.db.session_scope() as session:
            assert session.query(Bar).one().name == "test"

    def test_add_existent_missing_ingredient(self, app):
        with app.db.session_scope() as session:
            session.add(Bar(name="test"))
            session.add(Ingredient(name="Vodka"))
            session.commit()

        bartender = Bartender(app=app)
        bartender.add_ingredient(bar_name="test", ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            vodka = session.query(Ingredient).one()
            assert vodka in bar.ingredients

    def test_add_existent_present_ingredient(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            bar.ingredients.add(Ingredient(name="Vodka"))
            session.add(bar)
            session.commit()

        bartender = Bartender(app=app)
        with pytest.raises(errors.AlreadyInBarError):
            bartender.add_ingredient(bar_name="test", ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            vodka = session.query(Ingredient).one()
            assert vodka in bar.ingredients

    def test_add_non_existent_ingredient(self, app):
        with app.db.session_scope() as session:
            session.add(Bar(name="test"))
            session.commit()

        bartender = Bartender(app=app)
        with pytest.raises(errors.DoesNotExistError):
            bartender.add_ingredient(bar_name="test", ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            assert not bar.ingredients

    def test_list_zero_ingredients(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            session.add(bar)
            session.commit()

        bartender = Bartender(app=app)
        bar_ingredients = bartender.list_ingredients(bar_name="test")

        assert not bar_ingredients

    def test_list_one_ingredient(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            bar.ingredients.add(Ingredient(name="Vodka"))
            session.add(bar)
            session.commit()

        bartender = Bartender(app=app)
        bar_ingredients = bartender.list_ingredients(bar_name="test")

        assert len(bar_ingredients) == 1
        vodka = next(iter(bar_ingredients))
        assert vodka.name == "Vodka"

    def test_remove_existent_present_ingredient(self, app):
        pass

    def test_remove_existent_missing_ingredient(self, app):
        pass

    def test_remove_non_existent_ingredient(self, app):
        pass

    def test_list_wanted_ingredients(self, app):
        pass

    def test_list_cocktails(self, app):
        pass


class TestCookBook(object):
    pass
