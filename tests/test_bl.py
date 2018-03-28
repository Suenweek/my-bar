import pytest
from mybar import errors
from mybar.models import Bar, Ingredient, Cocktail


class TestBartender(object):

    def test_ensure_non_existent_bar_exists(self, app):
        with app.db.session_scope() as session:
            assert not session.query(Bar).count()

        app.bartender.ensure_bar_exists("test")

        with app.db.session_scope() as session:
            assert session.query(Bar).one().name == "test"

    def test_ensure_existent_bar_exists(self, app):
        with app.db.session_scope() as session:
            session.add(Bar(name="test"))

        app.bartender.ensure_bar_exists("test")

        with app.db.session_scope() as session:
            assert session.query(Bar).one().name == "test"

    def test_add_existent_missing_ingredient(self, app):
        with app.db.session_scope() as session:
            session.add(Bar(name="test"))
            session.add(Ingredient(name="Vodka"))

        app.bartender.add_ingredient(bar_name="test",
                                     ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            vodka = session.query(Ingredient).one()
            assert vodka in bar.ingredients

    def test_add_existent_present_ingredient(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            bar.ingredients.add(Ingredient(name="Vodka"))
            session.add(bar)

        with pytest.raises(errors.AlreadyInBarError):
            app.bartender.add_ingredient(bar_name="test",
                                         ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            vodka = session.query(Ingredient).one()
            assert vodka in bar.ingredients

    def test_add_non_existent_ingredient(self, app):
        with app.db.session_scope() as session:
            session.add(Bar(name="test"))

        with pytest.raises(errors.DoesNotExistError):
            app.bartender.add_ingredient(bar_name="test",
                                         ingredient_name="Vodka")

        with app.db.session_scope() as session:
            bar = session.query(Bar).one()
            assert not bar.ingredients

    def test_list_zero_ingredients(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            session.add(bar)

        bar_ingredients = app.bartender.list_ingredients(bar_name="test")

        with pytest.raises(StopIteration):
            next(bar_ingredients)

    def test_list_one_ingredient(self, app):
        with app.db.session_scope() as session:
            bar = Bar(name="test")
            bar.ingredients.add(Ingredient(name="Vodka"))
            session.add(bar)

        bar_ingredients = app.bartender.list_ingredients(bar_name="test")

        vodka = next(bar_ingredients)
        assert vodka.name == "Vodka"
        with pytest.raises(StopIteration):
            next(bar_ingredients)

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
