from my_bar.db import session_scope
from my_bar.models import Ingredient, Cocktail, Bar


def test_create_ingredient(db):
    with session_scope() as session:
        # Create ingredient
        dark_rum = Ingredient(name="Dark rum")
        session.add(dark_rum)

        session.commit()

    with session_scope() as session:
        # Check if ingredient was created
        ingredient = session.query(Ingredient).one()
        assert ingredient.name == "Dark rum"


def test_create_cocktail(db):
    with session_scope() as session:
        # Create Screwdriver ingredients
        vodka = Ingredient(name="Vodka")
        orange_juice = Ingredient(name="Orange juice")

        # Create Screwdriver cocktail
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
        # Check if ingredients were added
        assert len(ingredients) == 2
        vodka, orange_juice = ingredients
        assert vodka.name == "Vodka"
        assert orange_juice.name == "Orange juice"

        # Check if cocktail contains added ingredients
        cocktail = session.query(Cocktail).one()
        assert cocktail.name == "Screwdriver"
        assert len(cocktail.ingredients) == 2
        assert vodka in cocktail.ingredients
        assert orange_juice in cocktail.ingredients

        # Check if cocktail in ingredients' cocktails
        assert cocktail in vodka.cocktails
        assert cocktail in orange_juice.cocktails


def test_create_bar(db):
    with session_scope() as session:
        # Create bar
        bar = Bar(name="my-bar")
        session.add(bar)

        session.commit()

    with session_scope() as session:
        # Check if it can be found
        bar = session.query(Bar).one()
        assert bar.name == "my-bar"


def test_bar_can_make_cocktail(db):
    with session_scope() as session:
        # Create bar
        bar = Bar(name="my-bar")
        session.add(bar)

        # Create all ingredients
        vodka = Ingredient(name="Vodka")
        orange_juice = Ingredient(name="Orange juice")
        champagne = Ingredient(name="Champagne")

        # Add Screwdriver cocktail ingredients to bar
        bar.ingredients |= {vodka, orange_juice}

        # Create all cocktails
        screwdriver = Cocktail(
            name="Screwdriver",
            ingredients={vodka, orange_juice}
        )
        mimosa = Cocktail(
            name="Mimosa",
            ingredients={champagne, orange_juice}
        )
        session.add_all({screwdriver, mimosa})

        session.commit()

    with session_scope() as session:
        bar = session.query(Bar).one()
        screwdriver = session.query(Cocktail)\
                             .filter_by(name="Screwdriver")\
                             .one()
        mimosa = session.query(Cocktail)\
                        .filter_by(name="Mimosa")\
                        .one()

        # Check if bar can make Screwdriver but not Mimosa
        assert bar.can_make(screwdriver)
        assert not bar.can_make(mimosa)
