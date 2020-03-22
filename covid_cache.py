import json
from time import time, sleep
from pylev import damerau_levenshtein
import requests
from covid_service import parse_html
from covid_log import log

# thanks to these guys !!!
end_point = "https://www.worldometers.info/coronavirus/"

"""
In case the user writes the bad country name (pt-br)
we do some help here to find the right name
"""
sinonimos = {
    "brasil": "brazil",
    "italia": "italy",
    "espanha": "spain",
    "alemanha": "germany",
    "franca": "france",
    "frança": "france",
    "eua": "usa",
    "u.s.a": "usa",
    "estados unidos": "usa",
    "korea": "s. korea",
    "coreia": "s. korea",
    "suiça": "switzerland",
    "suica": "switzerland",
    "inglaterra": "uk",
    "reino unido": "uk",
    "holanda": "Netherlands",
    "noruega": "Norway",
    "belgica": "Belgium",
    "suécia": "Sweden",
    "suecia": "Sweden",
    "dinamarca": "Denmark",
    "japao": "Japan",
    "japão": "Japan",
    "malasia": "Malaysia",
    "grecia": "Greece",
    "irlanda": "Ireland",
    "bosnia": "Bosnia and Herzegovina"
}


def _load_data():
    try:
        resp = requests.get(end_point)
        if resp.status_code == 200:
            payload = parse_html(resp.text)
            for n1, n2 in sinonimos.items():
                payload[n1.lower()] = payload[n2.lower()]
            log("Cache miss")
            return True, payload
        return False, None
    except Exception as e:
        log("ERROR - cache_covid:_load_data - {}".format(e))
        return False, None


class Covid:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = None
        self.time = time() + ttl
        rc, payload = _load_data()
        if rc:
            self.cache = payload
        else:
            self.cache = None

    def get_data(self, country_name):
        if self.time < time():
            rc, payload = _load_data()
            if rc:
                self.cache = payload
            self.time = time() + self.ttl
        if self.cache is None:
            return None
        c = country_name.lower()
        if c in self.cache:
            return self.cache[c]
        best = ""
        score = 999999999
        for name in self.cache.keys():
            s = damerau_levenshtein(name, c)
            if s < score:
                score = s
                best = name
        if best in self.cache:
            return self.cache[best]
        return None


if __name__ == '__main__':
    covid = Covid(ttl=3)
    while True:
        now = time()
        country = covid.get_data("italiano")
        elapsed = round(time() - now, 3)
        payload = json.dumps(country, indent=4)
        log("Reply time {} seconds\n{}".format(elapsed, payload))
        sleep(1)
