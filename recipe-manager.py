#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup


def _has(food):
    _has.description = 'search recipes with {}'.format(food)
    url = f'https://www.recetario.es/encontrar?rec_all=0&search={food}'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    recipes_links = soup.select('a[class="item-link item-title"]')

    return recipes_links


def _build_parser():
    parser = argparse.ArgumentParser(
        description='Get recipes information.')
    
    # options
    parser.add_argument(
        '-has',
        action='store_true',
        help='indicates the foods that the recipes must contain')
    parser.add_argument('food')
    
    return parser


if __name__ == '__main__':
    parser = _build_parser()
    args = parser.parse_args()

    if args.has:
        recipes = _has(args.food)

        for recipe in recipes:
            recipe_title = recipe.text.capitalize()
            recipe_link = recipe.attrs['href']
            print(f'{recipe_title} en https://www.recetario.es{recipe_link}')
