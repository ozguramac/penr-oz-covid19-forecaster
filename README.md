# Penr-oz Covid-19 Forecaster

### Reference Documentation
For further reference, please consider the following sections:

* [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
* [Docker Compose Overview](https://docs.docker.com/compose/overview/) 
* [Python - Pandas](https://pandas.pydata.org/)
* [Python - Matplotlib](https://matplotlib.org/)
* [Data Science - ARIMA model](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)

### Additional Links
These additional references should also help you:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [Python - Time Series Forecasting](https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/)

## Download and Installation
* [Fork, Clone, or Download on GitHub](https://github.com/ozguramac/penr-oz-covid19-forecaster)

### Run
```
$ docker-compose up penr-oz-covid19-forecaster
```

Launch your favorite browser and goto [localhost:5000](http://localhost:5000)

### Stop
```
$ docker-compose stop
```

### Clean
```
$ docker-compose down
```

### Check/Health
```
docker-compose ps
```

### Testing
[docker-compose.override.yml](https://docs.docker.com/compose/extends/):
```
version: "3.7"
services:
  penr-oz-covid19-forecaster:
    command: app_test.py
```
then:
```
$ docker-compose up penr-oz-covid19-forecaster
```

### Who do I talk to? ###
* Repo owner or [admin](mailto:info@derinworksllc.com) 

## Copyright and License
&copy; Copyright 2020 [Derin Works LLC](http://www.derinworksllc.com)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)