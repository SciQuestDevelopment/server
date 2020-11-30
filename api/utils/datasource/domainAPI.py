import json
from pprint import pprint


# class for searching universities in diff countries
# use query($country) to find the result
class domainAPI:
    def __init__(self):
        # Load the source
        self.src = None
        with open('./world_universities_and_domains.json') as src_file:
            self.src = json.load(src_file)

    # it returns a list including names of all universities in that country
    def query(self, country):
        if self.src is None:
            return []

        if country == "global":
            return [entry['name'] for entry in self.src]

        def filter(entry, item):
            matching = entry['country']

            if item == matching or \
                    item == matching.lower() or \
                    item == matching.upper():
                return True

            else:
                return False

        return [entry['name'] for entry in self.src if filter(entry, country)]


if __name__ == '__main__':
    d = domainAPI()
    pprint(d.query("global"))
