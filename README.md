# FEUP LAPD
Repository to host the LAPD project

 * [D1 report on overleaf](https://www.overleaf.com/project/5c6e7f6dbc4fc01eaea98c5d)
 * [D1 slides on google slides](https://docs.google.com/presentation/d/1NvJW_P9WwHBwbEacZ1J-pC1pkdlGDi9zphYnHp0PHlc/edit)
 * [frauhnofer drive with some initial files](https://foldr.fraunhofer.pt/public/KREZM/browse)

## Entregas
1. 14.03.2019 Delivery and Presentation: Project proposal
2. 04.04.2019 Delivery and Presentation: Architecture and prototype
3. 23.05.2019 Guest presentation: Smart Services and IoT - challenges and opportunities.

## 15. Structuring the unstructured
Smartphones already include several sensors that can be used to improve the interaction with
the phone (e.g., answer calls), monitor the user’s physical activity, and locate the user in
indoor spaces. The accelerometer, gyroscope, and magnetometer are widely adopted to attain this goal. 
The sensory data is described as time series data since these data points are
captured in sequential time order. Over time, Fraunhofer AICOS collected several datasets and
saved a file for each sensor/user, which were stored in a network filesystem. These files are
accessed by our Data Scientists to apply Machine Learning (ML) technics and develop physical
activity and indoor location algorithms. AICOS developed a platform developed that consists of
a Spring Boot [1](https://spring.io/projects/spring-boot) enabled back-end server, providing a RESTful API; the data is stored on a
MongoDB [2](https://www.mongodb.com) database and Keycloak [3](https://www.keycloak.org) is adopted for authentication.
The objective of this application to migrate the datasets available in ASCII files to a NoSQL
databased through the provided API. We will deliver the datasets, a public instance of the
AICOS platform, and the API documentation


## Docker
To start the database and API services, you must first guarantee that you have loaded the API image (demdata-api-docker-images). To do so, simply run `docker load --input demdata-api-docker-images`. After that, simply run `docker-compose up` from the repository root folder.

## Tests
* Run tests: `python -m unittest discover`
* Run with [coverage](https://coverage.readthedocs.io/): `coverage run -m unittest discover`
* Generate (HTML) report: `coverage report` | `coverage html`

## Docs
To generate the docs again, `cd stuns/docs` and:
 * Windows: `make.bat html`
 * Linux: `make html`


## Pip problems
For some random pip related problems about "" you can use a proxy from [this list](https://free-proxy-list.net/) like so: `pip install MODULE --proxy="178.216.0.168:33364"`
