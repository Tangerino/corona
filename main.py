from flask import Flask, request
from covid_cache import Covid
import json
from covid_log import log

app = Flask(__name__)
covid_cache = Covid(ttl=900)        # fetch new data every 15 minutes only


@app.before_request
def just_log():
    try:
        headers = ""
        for h in request.headers:
            headers += "{} - ".format(h)
        print("WEB_REQUEST - {} {} {}".format(request.remote_addr, request.url, headers))
    except Exception as e:
        print("@app.before_request - {}".format(e))


@app.route("/covid/<country_name>/", methods=['GET'])
def covid(country_name):
    headers = ""
    for h in request.headers:
        headers += "{},".format(h)
    log("country_name, {}, {}, {}".format(country_name, request.remote_addr, headers))
    if country_name == "":
        r = {'status': 'error', 'description': "empty country name"}
        return json.dumps(r), 304

    country = covid_cache.get_data(country_name)
    if country is None:
        r = {'status': 'error', 'description': "country name not found - {}".format(country_name)}
        return json.dumps(r), 404
    r = {'status': 'ok', 'covid': country}
    return json.dumps(r), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=26666)

