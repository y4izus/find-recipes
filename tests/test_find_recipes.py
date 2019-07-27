import unittest
from bs4 import BeautifulSoup
from find_recipes import get_recipes_with, get_recipes_info


class TestFindRecipesMethods(unittest.TestCase):

    def test_get_recipes_with_food(self):
        '''should show the first 10 recipe <a> links for berenjenas'''
        food = 'berenjenas'
        recipes_anchors = get_recipes_with(food)
        recipes_anchors_bs4 = set(map(lambda a: BeautifulSoup(a).a, [
            '<a href="/robot-cocina/recetas/verduras/berenjenas-la-crema-con-gambas-y-jamon">Berenjenas a la crema con gambas y jamón</a>',
            '<a href="/robot-cocina/recetas/verduras/berenjenas-rellenas">Berenjenas rellenas</a>',
            '<a href="/robot-cocina/recetas/verduras/berenjenas-rellenas-la-mallorquina">Berenjenas rellenas a la mallorquina</a>',
            '<a href="/robot-cocina/recetas/sopas-y-cremas/crema-de-berenjenas-y-puerro">Crema de berenjenas y puerro</a>',
            '<a href="/robot-cocina/recetas/pates/pate-de-berenjenas">Paté de berenjenas</a>',
            '<a href="/robot-cocina/recetas/huevos/tortilla-de-berenjenas">Tortilla de berenjenas</a>',
        ]))
        self.assertEqual(recipes_anchors, recipes_anchors_bs4)

    def test_get_recipes_info(self):
        '''should get the nutritial information of the recipes'''
        recipe_tag_str = '<a href="/robot-cocina/recetas/huevos/tortilla-de-berenjenas">Tortilla de berenjenas</a>'
        recipe_tag = BeautifulSoup(recipe_tag_str, "html.parser")
        recipes_info = get_recipes_info(recipe_tag)
        self.assertEqual(
            recipes_info,
            [
                {'title': 'Tortilla de berenjenas',
                 'url': '/robot-cocina/recetas/huevos/tortilla-de-berenjenas',
                 'kcal': '293.00',
                 'fats': '25.50',
                 'proteins': '8.63',
                 'carbohydrates': '5.20',
                 'fiber': '3.80'}
            ]
        )


if __name__ == '__main__':
    unittest.main()
