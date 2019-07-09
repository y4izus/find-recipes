#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlencode, urlunparse
from PyInquirer import prompt


def get_recipes_for(food):
    """
    Return the set of recipe links containing ``food`` by scrapping a certain web page.
    """
    get_recipes_for.description = f'search recipes with {food}'
    query = {
        'rec_all': '0',
        'search': food
    }
    url_parsed = urlunparse(ParseResult(scheme='https', netloc='www.recetario.es', path='/encontrar',
                                        params='', query=urlencode(query), fragment=''))

    html = urlopen(url_parsed)
    soup = BeautifulSoup(html, 'lxml')
    recipes_links = soup.select('a[class="item-link item-title"]')

    return set(recipes_links)


def _build_parser():
    parser = argparse.ArgumentParser(
        description='Get recipes information.')

    # options
    parser.add_argument(
        '-has',
        dest='food',
        help='indicates the foods that the recipes must contain')

    return parser


def show_recipes_list_on_console(recipes_list):
    questions = [
        {
            'type': 'list',
            'message': 'Select a recipe',
            'name': 'selected_recipe',
            'choices': recipes_list
        }
    ]
    answers = prompt(questions)
    url_selected_recipe = answers['selected_recipe']
    print(url_selected_recipe)


def format_recipes_to_show_in_console(recipes):
    """
    Create a PyInquirer list of options from the list of recipes.
    """
    recipes_formatted_to_console = []

    for recipe in recipes:
        recipe_title = recipe.text.capitalize()
        recipe_link = recipe.attrs['href']
        recipes_formatted_to_console.append(
            {
                'value': f'https://www.recetario.es{recipe_link}',
                'name': recipe_title
            })
    return recipes_formatted_to_console


if __name__ == '__main__':
    parser = _build_parser()
    args = parser.parse_args()

    if args.food:
        recipes = get_recipes_for(args.food)
        recipes_formatted_to_console = format_recipes_to_show_in_console(
            recipes)
        show_recipes_list_on_console(recipes_formatted_to_console)
