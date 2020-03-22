import json
import requests
from covid_log import log

html_path = "/tmp/virus.html"


def extract_value_2(line):
    s = None
    line2 = line.replace("</a>", "")
    line2 = line2.replace("</td>", "")
    line2 = line2.replace("\n", "")
    line2 = line2.strip()
    sc = line2.rfind(">")
    if sc >= 0:
        s = line2[sc + 1:]
    return s


def extract_value(d, line, line_id):
    if line_id == 0:
        return
    s = extract_value_2(line)
    n = "0" + s.replace(",", "").replace("+", "")
    if line_id == 1:
        d["country"] = s.lower()
    elif line_id == 2:
        d["total_cases"] = int(n)
    elif line_id == 3:
        d["new_cases"] = int(n)
    elif line_id == 4:
        d["total_deaths"] = int(n)
    elif line_id == 5:
        d["new_deaths"] = int(n)
    elif line_id == 6:
        d["total_recovered"] = int(n)
    elif line_id == 7:
        d["active_cases"] = int(n)
    elif line_id == 8:
        d["serious_critical"] = int(n)


def parse_html(payload):
    try:
        html = payload
        s = "<div class=\"tab-content\" id=\"nav-tabContent\">"
        p = html.split(s)
        if len(p) > 1:
            html = p[1]
            s = "<div class=\"tab-pane \" id=\"nav-yesterday\" role=\"tabpanel\" aria-labelledby=\"nav-yesterday-tab\">"
            p = html.split(s)
            html = p[0]
            s = "<tr style=\"\">"
            p = html.split(s)
            groups = p[1:]
            d = {}
            for group in groups:
                lines = group.split("<td style=")
                item = {}
                for line_id in range(len(lines)):
                    extract_value(item, lines[line_id], line_id)
                d[item["country"]] = item
            return d
        return None     # what ?
    except Exception as e:
        log("parse_html error - {}".format(e))
        return None


