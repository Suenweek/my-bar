from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .db import Base


CocktailIngredient = Table(
    "cocktail_ingredient", Base.metadata,
    Column("cocktail_id", Integer, ForeignKey("cocktail.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"))
)


BarIngredient = Table(
    "bar_ingredient", Base.metadata,
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
        back_populates="ingredients",
        collection_class=set
    )

    bars = relationship(
        "Bar",
        secondary=BarIngredient,
        back_populates="ingredients",
        collection_class=set
    )

    def __repr__(self):
        return "<Ingredient(name='{}')>".format(self.name)


class Cocktail(Base):

    __tablename__ = "cocktail"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    ingredients = relationship(
        "Ingredient",
        secondary=CocktailIngredient,
        back_populates="cocktails",
        collection_class=set
    )

    def __repr__(self):
        return "<Cocktail(name='{}')>".format(self.name)


class Bar(Base):

    __tablename__ = "bar"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    ingredients = relationship(
        "Ingredient",
        secondary=BarIngredient,
        back_populates="bars",
        collection_class=set
    )

    def __repr__(self):
        return "<Bar(name='{}')>".format(self.name)

    def can_make(self, cocktail):
        return cocktail.ingredients.issubset(self.ingredients)
