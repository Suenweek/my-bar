from src.models import Glass, Ingredient, Cocktail, CocktailIngredient


def test_create_ingredient(db):
    ingredient_name = "Dark rum"
    ingredient_abv = 40

    with db.session as session:
        dark_rum = Ingredient(name=ingredient_name, abv=ingredient_abv)
        session.add(dark_rum)
        session.commit()

    with db.session as session:
        ingredient = session.query(Ingredient).one()
        assert ingredient.name == ingredient_name
        assert ingredient.abv == ingredient_abv


def test_create_glass(db):
    glass_name = "martini"

    with db.session as session:
        martini_glass = Glass(name=glass_name)
        session.add(martini_glass)
        session.commit()

    with db.session as session:
        glass = session.query(Glass).one()
        assert glass.name == glass_name


def test_create_cocktail(db):
    with db.session as session:
        highball = Glass(name="highball")
        vodka = Ingredient(name="Vodka", abv=40)
        orange_juice = Ingredient(name="Orange juice", abv=0)
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
                             .order_by(Ingredient.abv.desc())\
                             .all()
        assert len(ingredients) == 2
        vodka, orange_juice = ingredients
        assert vodka.name == "Vodka"
        assert vodka.abv == 40
        assert orange_juice.name == "Orange juice"
        assert orange_juice.abv == 0

        cocktail = session.query(Cocktail).one()
        assert cocktail.name == "Screwdriver"
        assert cocktail.glass == highball
        assert len(cocktail.ingredients) == 2
        assert vodka in cocktail.ingredients
        assert orange_juice in cocktail.ingredients

        assert cocktail in highball.cocktails
        assert cocktail in vodka.cocktails
        assert cocktail in orange_juice.cocktails
