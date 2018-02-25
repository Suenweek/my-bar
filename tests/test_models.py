from src.models import Glass, Ingredient, Cocktail


def test_create_ingredient(db):
    with db.session as session:
        dark_rum = Ingredient(name="Dark rum")
        session.add(dark_rum)
        session.commit()

    with db.session as session:
        ingredient = session.query(Ingredient).one()
        assert ingredient.name == "Dark rum"


def test_create_glass(db):
    with db.session as session:
        martini_glass = Glass(name="martini")
        session.add(martini_glass)
        session.commit()

    with db.session as session:
        glass = session.query(Glass).one()
        assert glass.name == "martini"


def test_create_cocktail(db):
    with db.session as session:
        highball = Glass(name="highball")
        vodka = Ingredient(name="Vodka")
        orange_juice = Ingredient(name="Orange juice")
        screwdriver = Cocktail(
            name="Screwdriver",
            glass=highball,
            ingredients=[vodka, orange_juice]
        )
        session.add(screwdriver)
        session.commit()

    with db.session as session:
        highball = session.query(Glass).one()
        assert highball.name == "highball"

        ingredients = session.query(Ingredient)\
                             .order_by(Ingredient.name.desc())\
                             .all()
        assert len(ingredients) == 2
        vodka, orange_juice = ingredients
        assert vodka.name == "Vodka"
        assert orange_juice.name == "Orange juice"

        cocktail = session.query(Cocktail).one()
        assert cocktail.name == "Screwdriver"
        assert cocktail.glass == highball
        assert len(cocktail.ingredients) == 2
        assert vodka in cocktail.ingredients
        assert orange_juice in cocktail.ingredients

        assert cocktail in highball.cocktails
        assert cocktail in vodka.cocktails
        assert cocktail in orange_juice.cocktails
