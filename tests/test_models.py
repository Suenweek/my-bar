from src.db import session_scope
from src.models import Ingredient, Cocktail, Bar


def test_create_ingredient(db):
    with session_scope() as session:
        dark_rum = Ingredient(name="Dark rum")
        session.add(dark_rum)
        session.commit()

    with session_scope() as session:
        ingredient = session.query(Ingredient).one()
        assert ingredient.name == "Dark rum"


def test_create_cocktail(db):
    with session_scope() as session:
        vodka = Ingredient(name="Vodka")
        orange_juice = Ingredient(name="Orange juice")
        screwdriver = Cocktail(
            name="Screwdriver",
            ingredients={vodka, orange_juice}
        )
        session.add(screwdriver)
        session.commit()

    with session_scope() as session:
        ingredients = session.query(Ingredient)\
                             .order_by(Ingredient.name.desc())\
                             .all()
        assert len(ingredients) == 2
        vodka, orange_juice = ingredients
        assert vodka.name == "Vodka"
        assert orange_juice.name == "Orange juice"

        cocktail = session.query(Cocktail).one()
        assert cocktail.name == "Screwdriver"
        assert len(cocktail.ingredients) == 2
        assert vodka in cocktail.ingredients
        assert orange_juice in cocktail.ingredients

        assert cocktail in vodka.cocktails
        assert cocktail in orange_juice.cocktails


def test_create_bar(db):
    with session_scope() as session:
        bar = Bar(name="Home-bar")
        session.add(bar)
        session.commit()

    with session_scope() as session:
        bar = session.query(Bar).one()
        assert bar.name == "Home-bar"
