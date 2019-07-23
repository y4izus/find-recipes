#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlencode, urlunparse
from PyInquirer import prompt


def _build_parser():
    parser = argparse.ArgumentParser(
        description='Get recipes information.')

    # options
    parser.add_argument(
        '-has',
        dest='food',
        help='indicates the foods that the recipes must contain')

    return parser


def get_recipes_info(recipes_tags):
    recipes_info = []
    for recipe_tag in recipes_tags:
        recipe = {}
        recipe['title'] = recipe_tag.text.capitalize()
        recipe['url'] = recipe_tag.attrs['href']
        url_parsed = urlunparse(ParseResult(scheme='http', netloc='www.chefplus.es', path=recipe['url'],
                                            params='', query='', fragment=''))
        html = urlopen(url_parsed)
        soup = BeautifulSoup(html, 'lxml')
        recipe['kcal'] = soup.find(
            "div", text="Calorías(Kcal)").find_next_sibling("div").text
        recipe['fats'] = soup.find(
            "div", text="Grasas(g)").find_next_sibling("div").text
        recipe['proteins'] = soup.find(
            "div", text="Proteínas(g)").find_next_sibling("div").text
        recipe['carbohydrates'] = soup.find(
            "div", text="Hidratos de carbono(g)").find_next_sibling("div").text
        recipe['fiber'] = soup.find(
            "div", text="Fibra(g)").find_next_sibling("div").text
        recipes_info.append(recipe)

    return recipes_info


def get_recipes_for(food):
    """
    Return the set of recipe links containing ``food`` by scrapping a certain web page.
    """
    get_recipes_for.description = f'search recipes with {food}'
    query = {
        'title': food
    }
    url_parsed = urlunparse(ParseResult(scheme='http', netloc='www.chefplus.es', path='/robot-cocina/recetas-resultados',
                                        params='', query=urlencode(query), fragment=''))

    html = urlopen(url_parsed)
    soup = BeautifulSoup(html, 'lxml')
    recipes_tags = soup.select('p[class="tit"]>a')

    return set(recipes_tags)


def show_recipe_instructions(url_selected_recipe):
    url_parsed = urlunparse(ParseResult(scheme='http', netloc='www.chefplus.es', path=url_selected_recipe,
                                        params='', query='', fragment=''))

    html = urlopen(url_parsed)
    soup = BeautifulSoup(html, 'lxml')

    print('\n=== INGREDIENTES ===')
    for recipe_ingredient_tag in soup.select('li[class="ingrediente"]'):
        print(recipe_ingredient_tag.text.replace('\n', ' '))

    print('\n=== PREPARACIÓN ===')
    for recipe_step_tag in soup.select('div[class*="field-name-field-receta-modo-express"]'):
        print(recipe_step_tag.text)

    # recipe['steps']


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
                'name': f"{recipe['title']}\nCalorías(Kcal): {recipe['kcal']}\nGrasas(g): {recipe['fats']}\nProteínas(g): {recipe['proteins']}\nHidratos de carbono(g): {recipe['carbohydrates']}\nFibra(g): {recipe['fiber']}"
            })
    return recipes_formatted_to_console


if __name__ == '__main__':
    parser = _build_parser()
    args = parser.parse_args()

    if args.food:
        recipes_tags = get_recipes_for(args.food)
        recipes_infos = get_recipes_info(recipes_tags)
        recipes_formatted_to_console = format_recipes_to_show_in_console(
            recipes_infos)
        show_recipes_list_on_console(recipes_formatted_to_console)
