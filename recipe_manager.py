#!/usr/bin/env python3

import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlencode, urlunparse
from PyInquirer import prompt
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


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def _get_soup_obj(path, query=''):
    '''Open a webpage with the indicated url and return its BeautifulSoup object'''
    url_parsed = urlunparse(ParseResult(scheme='http', netloc='www.chefplus.es', path=path,
                                        params='', query=query, fragment=''))

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url_parsed)

    return BeautifulSoup(html, 'lxml')


async def _get_recipe_info(recipe_tag):
    recipe = {}
    recipe['title'] = recipe_tag.text.capitalize()
    recipe['url'] = recipe_tag.attrs['href']

    soup = await _get_soup_obj(recipe['url'])
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

    return recipe


async def get_recipes_info(recipes_tags):
    recipes_info_co_list = [(_get_recipe_info(
        recipe_tag)) for recipe_tag in recipes_tags]
    recipes_info = await asyncio.gather(*recipes_info_co_list)

    return recipes_info


async def get_recipes_with(food):
    """
    Return the set of recipe tags containing ``food`` by scrapping a certain web page.
    """
    query = {
        'title': food
    }
    soup = await _get_soup_obj('/robot-cocina/recetas-resultados', urlencode(query))
    recipes_tags = soup.select('p[class="tit"]>a')

    return set(recipes_tags)


async def show_recipe_instructions(url_selected_recipe):
    soup = await _get_soup_obj(url_selected_recipe)

    print('\n=== INGREDIENTES ===')
    for recipe_ingredient_tag in soup.select('li[class="ingrediente"]'):
        print(recipe_ingredient_tag.text.replace('\n', ' '))

    print('\n=== PREPARACIÓN ===')
    for recipe_step_tag in soup.select('div[class*="field-name-field-receta-modo-express"]'):
        print(recipe_step_tag.text)


async def show_recipes_list_on_console(recipes_list):
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
    await show_recipe_instructions(url_selected_recipe)


def format_recipes_to_show_in_console(recipes):
    """
    Create a PyInquirer list of options from the list of recipes.
    """
    recipes_formatted_to_console = []

    for recipe in recipes:
        text_to_show = f'{recipe["title"]}' \
            f'\nCalorías(Kcal): {recipe["kcal"]}' \
            f'\nGrasas(g): {recipe["fats"]}' \
            f'\nProteínas(g): {recipe["proteins"]}' \
            f'\nHidratos de carbono(g): {recipe["carbohydrates"]}' \
            f'\nFibra(g): {recipe["fiber"]}\n'

        recipes_formatted_to_console.append(
            {
                'value': recipe['url'],
                'name': text_to_show
            })
    return recipes_formatted_to_console


async def recipe_management(food):
    recipes_tags = await get_recipes_with(food)
    start = datetime.now()
    recipes_infos = await get_recipes_info(recipes_tags)
    print('Elapsed time:', datetime.now() - start)
    recipes_formatted_to_console = format_recipes_to_show_in_console(
        recipes_infos)
    await show_recipes_list_on_console(recipes_formatted_to_console)


if __name__ == '__main__':
    parser = _build_parser()
    args = parser.parse_args()

    if args.food:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(recipe_management(args.food))
