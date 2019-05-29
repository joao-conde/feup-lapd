# FEUP LAPD
Structring The UNStructured project for FRAUHNOFER AICOS project.

More information available in:

* [STUNS](stuns/)
* [flask API](api/)

Authors:
 * [João Conde](https://github.com/joao-conde/)
 * [João Damas](https://github.com/cyrilico)
 * [Miguel Ramalho](https://github.com/msramalho)


## Docker
To start the database and API services, you must first guarantee that you have loaded the API image (demdata-api-docker-images). To do so, simply run `docker load --input demdata-api-docker-images` (AICOS team should have this image). After that, simply run `docker-compose up` from the repository root folder.