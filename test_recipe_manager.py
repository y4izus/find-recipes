import unittest
from bs4 import BeautifulSoup
from recipe_manager import _has


class TestRecipeManagerMethods(unittest.TestCase):

    def test_get_recipes(self):
        '''should show the first 12 recipe <a> links for berenjenas'''
        food = 'berenjenas'
        recipes_anchors = _has(food)
        recipes_anchors_bs4 = list(map(lambda a: BeautifulSoup(a).a, [
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/1t4dgkn5-885b2-476309-cfcd2-b65gwfkr">BERENJENAS RELLENAS</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-ibericas/qfscdbe1-410a0-374809-cfcd2-quwvtebm">Berenjenas ibéricas.</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-confitadas/7lq5l513-eddeb-290173-cfcd2-y0ab5c7b">BERENJENAS CONFITADAS</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/jt8njca4-731d0-725093-cfcd2-ypp6v0f8">Berenjenas Rellenas</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/lcg9y27p-25311-946237-88c8b-hhp34ycj">BERENJENAS RELLENAS</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-estofadas/2x3jz8my-e4a93-514368-cfcd2-t05p5a0e">BERENJENAS ESTOFADAS</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjena-rellena/4glantqd-e3d11-451326-cfcd2-i1dmr9fu">Berenjena rellena</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/3gnkc93i-129e4-356941-cfcd2-f57ghumz">BERENJENAS RELLENAS </a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/gxwiyssl-e449b-234109-cfcd2-z1wi29lv">Berenjenas rellenas</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/simplemente-berenjenas/1knqn7dq-27302-305429-cfcd2-rb41hkae">SIMPLEMENTE BERENJENAS</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-sencillas/vmn1gmci-6fad7-189053-cfcd2-1r4nqa4u">Berenjenas sencillas</a>',
            '<a class="item-link item-title" href="/verduras-y-hortalizas-recetas/berenjenas-rellenas/iki514l6-e449b-129568-cfcd2-qkyy224q">Berenjenas rellenas</a>'
        ]))
        self.assertEqual(len(recipes_anchors), 12)
        self.assertEqual(recipes_anchors, recipes_anchors_bs4)


if __name__ == '__main__':
    unittest.main()
