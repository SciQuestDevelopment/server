from pprint import pprint

import requests

class nature:
    def __init__(self):
        self.base = "https://www.nature.com/opensearch/request"

    def query(self, keyword):
        payload = dict(
            interface='sru',
            maximumRecords=25,
            startRecord=1,
            recordPacking='packed',
            sortKeys='Relevance',
            httpAccept='application/json',
            query="cql.keywords="+keyword
        )
        resp = requests.get(url=self.base, params=payload)
        print(resp.url)
        res = resp.json()
        return res['feed']['entry']


if __name__ == '__main__':
    s = nature()
    pprint(s.query('gene'))
