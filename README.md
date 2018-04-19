# bing-scraper
Scrape bing search engine for info about each town/city in England.

# Repos needed to run this project:
beautifulsoup4==4.6.0
requests==2.18.4

# How it works?
>> RUN START.PY
1. It takes list of all towns/cities in England from: https://en.wikipedia.org/wiki/List_of_towns_in_England
2. Whole list will be sorted by county and the base dict will be created: dict[county][list ow towns for each county]
3. Dirs will be created: Logs (with succesful and unsuccesful queries sorted by files), Data (with raw HTML from each succesful query).
4. For each town from the list up to 3 bing queries will be created:
if list == 1:
        url = BASE_URL + URL
        example: https://www.bing.com/search?q=Watford
    elif list > 1:
        url = BASE_URL + PREVIOUS_KEYWORD + NEXT_KEYWORD
        example: https://www.bing.com/search?q=Watford+Hertfordshire
    else:
        url = BASE_URL + PREVIOUS_KEYWORD + NEXT_KEYWORD + United Kingdom
        example: https://www.bing.com/search?q=Watford+Hertfordshire+United+Kingdom

This is neccessary due to different search results (HTML structure) served by bing. If content not found querying first URL, second URL will be used.
5. Save successful urls in 'Logs\query_found.txt' and unsuccessful urls in 'Logs\query_not_found.txt'. 
6. Save HTML content of each successful url in 'Data' directory. Each file name is built of town name + current time + .html
7. Start extracting the data from all saved HTML files:
data-extractor.py will loop over all files found in the 'Data' directory. It will grab:
- Title of each location,
- Description of each location,
- Image of each location,
- map coordinates of each location,
- Population of each location if found.
8. New file will be created, result.json:
{
    "Bedfordshire": {
        "Ampthill": {
            "HEAD": {
                "subtitle": "Civil Parish",
                "title": "Ampthill"
            },
            "description": "Ampthill is a town and civil parish in Bedfordshire, England, between Bedford and Luton, with a population of about 14,000. It is administered by Central Bedfordshire Council. A regular market has taken place on Thursdays for centuries.",
            "img": {
                "url": "https://tse1.mm.bing.net/th?id=A0e3135c092a44d853c3bfe8cba89ac99&w=118&h=149&c=8&rs=1&qlt=90&pid=3.1&rm=2"
            },
            "map": {
                "coordinates": {
                    "centerLatitude": "52.0169105529785",
                    "centerLongitude": "-0.506489992141724",
                    "zoom": ""
                }
            },
            "population": null
        },
        "Arlesey": {
            "HEAD": {
                "subtitle": null,
                "title": "Arlesey"
            },
            "description": "Arlesey is a town and Civil Parish in Bedfordshire. It is near the border with Hertfordshire, about three miles north-west of Letchworth Garden City, four miles north of Hitchin and six miles south of Biggleswade. Arlesey railway station provides services to London, Stevenage and Peterborough. The Domesday Book mentions Arlesey.",
            "img": {
                "url": "http://www.bing.com/th?id=A48eb8ccbbebcc8a526f98deace00c596&w=110&h=110&c=7&rs=1&qlt=80&pcl=f9f9f9&cdv=1&pid=16.1"
            },
            "map": {
                "coordinates": {
                    "centerLatitude": "51.9719200134277",
                    "centerLongitude": "-0.299589991569519",
                    "zoom": ""
                }
            },
            "population": "5,584 (2011)"
        },
        "Bedford": {
            "HEAD": {
                "subtitle": null,
                "title": "Bedford"
            },
            "description": "Bedford is the county town of Bedfordshire, England. The town has a population of around 80,000, whereas the Borough of Bedford had a population of 166,252 in 2015 together with Kempston. Bedford was founded at a ford on the River Great Ouse, and is thought to have been the burial place of Offa of Mercia. Bedford Castle was built by Henry I, although it was destroyed in 1224. Bedford was granted borough status in 1165 and has been represented in Parliament since 1265. It is well known for its large population of Italian descent.",
            "img": {
                "url": "https://tse1.mm.bing.net/th?id=OIP.q_hW4uLBcidfzyo-1UV6TgHaE8&w=151&h=105&c=8&rs=1&qlt=90&pid=3.1&rm=2"
            },
            "map": {
                "coordinates": {
                    "centerLatitude": "52.1137809753418",
                    "centerLongitude": "-0.500009536743164",
                    "zoom": ""
                }
            },
            "population": "92,410 (2016)"
        },
