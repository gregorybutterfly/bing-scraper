import requests
from bs4 import BeautifulSoup
from random import choice
import os
from time import strftime, gmtime
from config import DATA_PATH, LOGS_PATH, BASE_PATH
from data_extractor import extract_data

"""
- Scrap all english towns and counties from Wikipedia table.
- Create dict object with counties as keys and list of towns as values.
- Create 'Logs' and 'Data' directories.
- Create urls for bing search engine and download the content for each url.
- Save successful urls in 'Logs\query_found.txt' and unsuccessful urls in 'Logs\query_not_found.txt'. 
- Save HTML content of each successful url in 'Data' directory. Each file name is built of town name + current time + .html
"""


class FileHandler:

    def __init__(self, directory, filename, mode):
        self.filename = filename
        self.mode = mode

        if directory.lower() == 'logs':
            os.chdir(LOGS_PATH)
        elif directory.lower() == 'data':
            os.chdir(DATA_PATH)

    def __enter__(self):
        self.open_file = open(self.filename, self.mode)
        return self.open_file

    def __exit__(self, *args):
        self.open_file.close()
        return


class CreateBingUrl:
    """Create bing queries from given list of keywords.
    if list == 1
        url = BASE_URL + URL
        example: https://www.bing.com/search?q=Watford
    elif list > 1
        url = BASE_URL + PREVIOUS_KEYWORD + NEXT_KEYWORD
        example: https://www.bing.com/search?q=Watford+Hertfordshire
    """

    # First part of bing query
    BASE_URL = 'https://www.bing.com/search?q='

    def __init__(self, *keyword):
        self.KEYWORD_LIST = list(keyword)
        self.replace_spaces()

    def replace_spaces(self):
        """ensure that two word keywords are separated by '+' instead of empty space
        """

        for i, element in enumerate(list(self.KEYWORD_LIST)):
            self.KEYWORD_LIST[i] = element.replace(' ', '+')

    @property
    def url_list(self):
        """ Makes queries for bing search engine"""

        url_list = []

        for i in range(len(self.KEYWORD_LIST)):
            url = self.BASE_URL + str("+".join(self.KEYWORD_LIST[0:i+1]))
            url_list.append(url)

        return url_list


class QueryBing:
    """Accepts a list of links and grabs the data from Bing search results

    CREDITS:
    http://edmundmartin.com/random-user-agent-requests-python/
    """

    DESKTOP_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

    def __init__(self, urls, keywords):
        self.URL_LIST = urls
        self.KEYWORDS = keywords

    def random_headers(self):
        return {'User-Agent': choice(self.DESKTOP_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    @property
    def get_content(self):
        """Grab content of given url
        """

        for link in self.URL_LIST:
            # go by each link from the list
            r = requests.get(link, headers=self.random_headers())

            if 'class="b_lBottom b_snippet"' in r.text:

            # if present search result is valid
            #if 'CC-BY-SA' in r.text:
                # write the link to logs: query_found.txt
                with FileHandler('logs','query_found.txt', 'a') as f:
                    f.write(link + '\n')

                # Write html to file for future reference
                file_name = link.split('=')[1].replace('+','_')

                file_name = file_name + '_' + strftime("%H%M%S", gmtime()) + '.html'

                # Get rid of ugly pluses
                if '+' in file_name:
                    file_name.replace('+','_')
                if '/' in file_name:
                    file_name.replace('/','_')

                # save html to a file: query + current time
                with FileHandler('data', file_name, 'w') as f:
                    # write query keywords in first line for future use
                    f.write('='.join(self.KEYWORDS) + '\n')
                    f.write(BeautifulSoup(r.text, 'html.parser').prettify())

                break
            else:
                # continue with more specified query URL + PREVIOUS KEYWORD + NEXT KEYWORD
                continue

        else:
            # if nothing has been found log the url
            with FileHandler('logs','query_not_found.txt', 'a') as f:
                f.write(link + '\n')

        return


def wiki_locations_raw():
    """Grabs cities/towns and counties from wikitable
    https://en.wikipedia.org/wiki/List_of_towns_in_England
    """
    r = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_England').text, 'html.parser')

    locations_table = r.find_all('table', {'class':'wikitable sortable'})

    # list of lists of 3 elements each [[town],[county],[council]]
    rows = []

    for row in locations_table:
        element = row.find_all('tr')

        for cell in element:
            cell_text = cell.find_all('td')

            cells = []

            for item in cell_text:
                cells.append(item.text)

            if len(cells) > 0:
                rows.append(cells)

    # returns list of 3 elements (town, county, council)
    return rows


def sorted_locations(locations_to_sort):
    """Sorts wiki_locations and wraps them in dictionary
    """

    location_dict = {}

    for loc in locations_to_sort:
        if not location_dict.get(loc[1]):
            location_dict.update({loc[1]: [loc[0], ]})
        else:
            location_dict[loc[1]].append(loc[0], )

    return location_dict


def main():
    """
    progress_bar = 0
    for county, town_list in sorted_locations(wiki_locations_raw()).items():
        for town in town_list:
            # Create urls for each iteration
            query = CreateBingUrl(town, county, '"United+Kingdom"')
            # grab the content of each url
            search_results = QueryBing(query.url_list, (county, town))
            # save the html content in 'Data' directory and successful urls in 'Logs' directory
            search_results.get_content

            progress_bar += 1

            print('\r {0}%: {1}, {2}'.format(progress_bar / 10,
                                             county, town), end="")
    """
    # Extract the data and create json file: result.json
    extract_data()

if __name__ == '__main__':
    main()