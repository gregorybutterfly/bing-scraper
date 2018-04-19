import os
from config import DATA_PATH, FILE_LIST, BASE_PATH
from bs4 import BeautifulSoup
from collections import defaultdict
import json

final_dict = defaultdict(dict)


def location_title(content):
    """Grabs title and subtitle from bing search results pages.
    """

    if content.find('h2', {'class':' b_entityTitle'}):

        title = content.find('h2', {'class':' b_entityTitle'}).text.strip()

        if content.find('div', {'class': 'b_entitySubTitle'}):
            subtitle = content.find('div', {'class': 'b_entitySubTitle'}).text.strip()
            return {'title': title, 'subtitle': subtitle}
        else:
            return {'title': title, 'subtitle': None}


def location_description(content):
    """Grabs the description from given content.
    Bing does not serve same results for the same query every time. Some page results are built differently.

    Text can be found wrapped in:
    - span.text
    - span.span.text

    If span tag contains '…' symbol it is shortened description and will not be used as description.

    """

    description_block = content.find('div', {'class': 'b_lBottom b_snippet'})

    description_block_span = description_block.find_all('span')

    description = ''

    for i in range(len(description_block_span)):
        if len(description_block_span[i].text) > len(description) and '…' not in description_block_span[i].text:
            description = description_block_span[i].text.strip()

    return description


def location_map(content):
    """Grabs map coordinates from given content.
    """

    if content.find('a', {'title':'Map'}):

        coordinates = content.find('a', {'title':'Map'}).div['data-src'].split('&')

        for element in coordinates:
            if 'ma=' in element:
                return {"coordinates": {"centerLatitude": element.split('ma=')[1].split(',')[0], "centerLongitude": element.split('ma=')[1].split(',')[1],
                         "zoom": ''}, }

    elif content.find('div', {'class':'dynMap'}):

        if content.find('div', {'class':'bm_details_overlay'}):

            coordinates = eval(
                content.find('div', {'class': 'bm_details_overlay'})['data-detailsoverlay'].replace(':true', ":'true'"))

            return {"coordinates": {
                "centerLatitude": coordinates["centerLatitude"],
                "centerLongitude": coordinates["centerLongitude"], "zoom": coordinates['zoom']}
                , }

        elif content.find('div', {'class':'bm_results_overlay'}):

            coordinates = eval(
                content.find('div', {'class': 'bm_results_overlay'})['data-resultsoverlay'].replace(':true', ":'true'"))

            return {"map": {"centerLatitude": coordinates['mapBounds'][0],
                            "centerLongitude": coordinates['mapBounds'][1], "zoom": None}, }
    else:
        return {'map':None}


def location_img(content, keyword):
    """Grabs location img from bing search results.
    """

    try:
        if content.find('div', {'class':'irp'}):
            return {'url': content.find('div', {'class':'irp'}).a.img['data-src-hq']}
        elif content.find('div', {'class':'b_float_img'}):
            return {'url': 'http://www.bing.com' + content.find('div', {'class': 'b_float_img'}).div.a.div['data-src']}
    except:
        return {'url':None}


def location_population(content):
    """Grabs info about population of each place from bing search engine results.
    """

    population = content.find_all('span', {'class':'cbl b_lower'})

    if population:
        for element in population:
            if 'Population' in element.parent.text:
                return element.parent.text.split(':')[-1].strip()
            else:
                return None
    else:
        return None


def create_json_file(location_dictionary):
    """Create json file from collected data
    """

    os.chdir(BASE_PATH)
    with open('result.json', 'w') as fp:
        json.dump(location_dictionary, fp, sort_keys=True, indent=4, separators=(',', ': '))
    print('File result.json has been created')


def extract_data():

    for file in FILE_LIST:
        with open(os.path.join(DATA_PATH,file), 'r') as f:
            data = f.read()
            first_line = data.split('\n', 1)[0].split('=')

            soup = BeautifulSoup(data, 'html.parser')

            title = location_title(soup)
            print('Processing: {}, {}'.format(first_line[0], first_line[1]))
            description = location_description(soup)
            _map = location_map(soup)
            img = location_img(soup, first_line[0])
            population = location_population(soup)

            final_dict[first_line[0]][first_line[1]] = {
                'HEAD':title,
                'description':description,
                'map':_map,
                'img':img,
                'population':population,
                }

    # Create json file with all the data: result.json
    create_json_file(final_dict)


# Start data extraction

if __name__ == '__main__':
    extract_data()


