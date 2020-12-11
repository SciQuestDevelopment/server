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
            p=100,
            api_key=api_key
        )
        resp = requests.get(url=self.base, params=payload)
        print(resp.url)
        res = resp.json()['records']
        return res


if __name__ == '__main__':
    s = springer("openaccess")
    params = dict(
        keyword='cnn'
    )
    pprint(s.query(params))
