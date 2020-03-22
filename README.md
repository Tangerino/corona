# corona
## COVID-19 Web Service

A simple web service, written in Python.
Basically it reads this web page (https://www.worldometers.info/coronavirus/) parse it and shares the information as a web service.

This software is free, do whatever you want with it. I'm not responsable for anything :)

No further documentation is planned, sorry.

The project is somehow tiny.

An active service will run until the crisis ends at:

```url
http://covid.tangerino.me:26666/[country_name]
```

Example:
```bash
curl http://robot.tangerino.me:26666/covid/france/
```

The service will return a JSON payload like this

```json
{
  "status": "ok",
  "covid": {
    "country": "france",
    "total_cases": 14459,
    "new_cases": 0,
    "total_deaths": 562,
    "new_deaths": 0,
    "total_recovered": 1587,
    "active_cases": 12310,
    "serious_critical": 1525
  }
}
```

## Enjoy 
