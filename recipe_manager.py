#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlencode, urlunparse
from PyInquirer import prompt
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


def _build_parser():
    parser = argparse.ArgumentParser(
        description='Get recipes information.')

    # options
    parser.add_argument(
        '-with',
        dest='food',
        help='indicates a food that the recipes must contain')

    return parser


def _get_soup_obj(path, query=''):
    '''Open a webpage with the indicated url and return its BeautifulSoup object'''
    url_parsed = urlunparse(ParseResult(scheme='http', netloc='www.chefplus.es', path=path,
                                        params='', query=query, fragment=''))
    html = urlopen(url_parsed)
    return BeautifulSoup(html, 'lxml')


def get_recipe_html(recipe_tag):
    recipe_url = recipe_tag.attrs['href']

    return _get_soup_obj(recipe_url)


def get_recipe_info(recipe_html):
    recipe = {}
    print(recipe_html.select('head'))
    recipe['title'] = recipe_html.select('h1')
    recipe['kcal'] = recipe_html.find(
        "div", text="Calorías(Kcal)").find_next_sibling("div").text
    recipe['fats'] = recipe_html.find(
        "div", text="Grasas(g)").find_next_sibling("div").text
    recipe['proteins'] = recipe_html.find(
        "div", text="Proteínas(g)").find_next_sibling("div").text
    recipe['carbohydrates'] = recipe_html.find(
        "div", text="Hidratos de carbono(g)").find_next_sibling("div").text
    recipe['fiber'] = recipe_html.find(
        "div", text="Fibra(g)").find_next_sibling("div").text
    return recipe


def get_recipes_info(recipes_tags):
    recipes_html = []
    recipes_info = []

    start = datetime.now()
    with ThreadPoolExecutor(max_workers=5) as executor:
        recipes_html = executor.map(get_recipe_html, recipes_tags)
    with ThreadPoolExecutor(max_workers=5) as executor:
        recipes_info = executor.map(get_recipe_info, recipes_html)
    print('Elapsed time:', datetime.now() - start)

    return recipes_info


def get_recipes_with(food):
    """
    Return the set of recipe tags containing ``food`` by scrapping a certain web page.
    """
    query = {
        'title': food
    }
    soup = _get_soup_obj('/robot-cocina/recetas-resultados', urlencode(query))
    recipes_tags = soup.select('p[class="tit"]>a')

    return set(recipes_tags)


def show_recipe_instructions(url_selected_recipe):
    soup = _get_soup_obj(url_selected_recipe)

    print('\n=== INGREDIENTES ===')
    for recipe_ingredient_tag in soup.select('li[class="ingrediente"]'):
        print(recipe_ingredient_tag.text.replace('\n', ' '))

    print('\n=== PREPARACIÓN ===')
    for recipe_step_tag in soup.select('div[class*="field-name-field-receta-modo-express"]'):
        print(recipe_step_tag.text)


def show_recipes_list_on_console(recipes_list):
    questions = [
        {
            'type': 'list',
            'message': 'Seleccione una receta: ',
            'name': 'selected_recipe',
            'choices': recipes_list
        }
    ]
    answers = prompt(questions)
    url_selected_recipe = answers['selected_recipe']
    show_recipe_instructions(url_selected_recipe)


def format_recipes_to_show_in_console(recipes):
    """
    Create a PyInquirer list of options from the list of recipes.
    """
    recipes_formatted_to_console = []

    for recipe in recipes:
        recipes_formatted_to_console.append(
            {
                'value': recipe['url'],
                'name': f"{recipe['title']}\nCalorías(Kcal): {recipe['kcal']}\nGrasas(g): {recipe['fats']}\nProteínas(g): {recipe['proteins']}\nHidratos de carbono(g): {recipe['carbohydrates']}\nFibra(g): {recipe['fiber']}\n"
            })
    return recipes_formatted_to_console


if __name__ == '__main__':
    parser = _build_parser()
    args = parser.parse_args()

    if args.food:
        recipes_tags = get_recipes_with(args.food)
        recipes_infos = get_recipes_info(recipes_tags)
        recipes_formatted_to_console = format_recipes_to_show_in_console(
            recipes_infos)
        show_recipes_list_on_console(recipes_formatted_to_console)
