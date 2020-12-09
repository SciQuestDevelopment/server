import json
from pprint import pprint

import requests

api_key = "d8052a59b5b11e8deb269ce1805fcbae"


class springer:
    def __init__(self, api_type):
        self.base = "http://api.springernature.com"
        if api_type == "metadata":  # Springer Nature Metadata API
            self.base += "/metadata/"
        elif api_type == "meta":  # Springer Nature Meta API
            self.base += "/meta/v2/"
        elif api_type == "openaccess":  # Springer Nature openaccess API
            self.base += "/openaccess/"

        self.base += "json"  # can be changed for returning xml

    '''
        query_type: doi
                    type
                    subject
                    keyword
                    ...
                    more on  https://dev.springernature.com/adding-constraints
    '''

    def query(self, params):
        payload = dict(
            q=" ".join([f"{constraint}:{value}" for (constraint, value) in params.items()]),
            api_key=api_key
        )
        resp = requests.get(url=self.base, params=payload)
        print(resp.url)
        resp_json = resp.json()['records'][0]
        res = dict(abstract = resp_json['abstract'],
                    creators = resp_json['creators'],
                    doi = resp_json['doi'],
                    isbn = resp_json['isbn'],
                    date = resp_json['publicationDate'],
                    title = resp_json['title'],
                    publisher = resp_json['publisher'])
        return json.dumps(res)


if __name__ == '__main__':
    s = springer("meta")
    params = dict(
        doi='10.1007/978-3-319-07410-8_4'
    )
    pprint(s.query(params))
