from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


CocktailIngredient = Table(
    "cocktail_ingredient", Base.metadata,
    Column("cocktail_id", Integer, ForeignKey("cocktail.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"))
)


BarIngredient = Table(
    "ingredient_bar", Base.metadata,
    Column("bar_id", Integer, ForeignKey("bar.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"))
)


class Ingredient(Base):

    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    cocktails = relationship(
        "Cocktail",
        secondary=CocktailIngredient,
        back_populates="ingredients"
    )

    bars = relationship(
        "Bar",
        secondary=BarIngredient,
        back_populates="ingredients"
    )


class Glass(Base):

    __tablename__ = "glass"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    cocktails = relationship("Cocktail", back_populates="glass")


class Cocktail(Base):

    __tablename__ = "cocktail"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    glass_id = Column(Integer, ForeignKey("glass.id"))
    glass = relationship("Glass", back_populates="cocktails")

    ingredients = relationship(
        "Ingredient",
        secondary=CocktailIngredient,
        back_populates="cocktails"
    )


class Bar(Base):

    __tablename__ = "bar"

    id = Column(Integer, primary_key=True)

    ingredients = relationship(
        "Ingredient",
        secondary=BarIngredient,
        back_populates="bars"
    )
