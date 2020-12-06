import json
from pprint import pprint

import requests

api_key = "47423db69d6b0f939c002c98f08b46ad"


class elsevier:
    def __init__(self, search_type):
        self.base = "https://api.elsevier.com/content/search/"
        self.search_type = search_type


    '''
        :query_type author/scopus/affiliation...
        :param
            https://dev.elsevier.com/sc_search_tips.html
    '''

    def query(self, params):
        payload = dict(
            query=" ".join([f"{constraint}({value})" for (constraint, value) in params.items()]),
            apiKey=api_key
        )
        resp = requests.get(url=self.base + self.search_type, params=payload)
        print(resp.url, resp.status_code)
        return json.dumps(resp.json())


if __name__ == '__main__':
    s = elsevier('scopus')
    params = dict(
        # doi='10.1021/es052595+'
        all='gene'
    )
    pprint(s.query(params))
