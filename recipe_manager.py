#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlencode, urlunparse
from PyInquirer import prompt


def create_url(path, query=''):
    return urlunparse(ParseResult(scheme='https', netloc='www.recetario.es', path=path,
                                  params='', query=urlencode(query), fragment=''))


def get_recipes_for(food):
    """
    Return the set of recipe links containing ``food`` by scrapping a certain web page.
    """
    get_recipes_for.description = f'search recipes with {food}'
    query = {
        'rec_all': '0',
        'search': food
    }
    # url_parsed = create_url('/encontrar', query)
    url_parsed = urlunparse(ParseResult(scheme='https', netloc='www.recetario.es', path='/encontrar',
                                        params='', query=urlencode(query), fragment=''))

    html = urlopen(url_parsed)
    soup = BeautifulSoup(html, 'lxml')
    recipes_links = soup.select('a[class="item-link item-title"]')

    return set(recipes_links)


def get_recipe_ingredients(recipe_link):
    url = create_url(recipe_link)
    print(recipe_link)
    html = urlopen(url)
    scraper = BeautifulSoup(html, 'lxml')
    ingredients_scraped = scraper.select('li[itemprop="recipeIngredient"]')
    ingredients_list = [ingredient.text.replace('\n', '').replace('\t', '').strip()
                        for ingredient in ingredients_scraped]

    print(ingredients_list)


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
    get_recipe_ingredients(url_selected_recipe)
    # print(url_selected_recipe)


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
                'value': recipe_link,
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
