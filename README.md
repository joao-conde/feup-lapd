# FEUP LAPD
Repository to host the LAPD project

 * [D1 report on overleaf](https://www.overleaf.com/project/5c6e7f6dbc4fc01eaea98c5d)
 * [D1 slides on google slides](https://docs.google.com/presentation/d/1NvJW_P9WwHBwbEacZ1J-pC1pkdlGDi9zphYnHp0PHlc/edit)
 * [frauhnofer drive with some initial files](https://foldr.fraunhofer.pt/public/KREZM/browse)

## Setup
* `sudo apt-get install python3-tk`

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
accessed by our Data Scientists to apply Machine Learning (ML) techniques and develop physical
activity and indoor location algorithms. AICOS developed a platform developed that consists of
a Spring Boot [1](https://spring.io/projects/spring-boot) enabled back-end server, providing a RESTful API; the data is stored on a
MongoDB [2](https://www.mongodb.com) database and Keycloak [3](https://www.keycloak.org) is adopted for authentication.
The objective of this application to migrate the datasets available in ASCII files to a NoSQL
databased through the provided API. We will deliver the datasets, a public instance of the
AICOS platform, and the API documentation


## Docker
To start the database and API services, you must first guarantee that you have loaded the API image (demdata-api-docker-images). To do so, simply run `docker load --input demdata-api-docker-images`. After that, simply run `docker-compose up` from the repository root folder.

## Loading sample data provided
After downloading the compressed binary dump file (.gz) and having the database service up and running, navigate to the directory where the file is and run `mongorestore --port 9090 --gzip --archive=dump_2019-04-01.gz`. If everythings goes well, you should see a few messages stating that 'x' documents were imported for each collection, and a _done_ message in the end is displayed.

## Querying data

In order to query the data, fire a mongo shell or, for a prettier solution, download [Robo3T](https://download.robomongo.org/1.2.1/linux/robo3t-1.2.1-linux-x86_64-3e50a65.tar.gz). Setting up a connection should be pretty straightfoward (just leave default settings, other than port, which should be 9090). To view all documents in a collection, simply navigate in the GUI and double click on it (equivalent to, in a mongo shell, doing `use demdata_db`, `db.<collection_name>.find()`).

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

# Possible features of the parser suggested at the meeting in Fraunhofer AICOS

## Data Verification

1. Timestamps
   * Ensure ascending order
   * Consistent sampling frequency
   * Negative timestamps
   * Too short samples (begin and end timestamp too close, possibility of defining minimum time for a sample)
2. De-calibration of the magnetometer
3. Column completness


## Data Visualization

1. Drag & drop ASCII files to parser
2. Make plots of the different sensors data
