# STUNS
> Structring The UNStructured command line tool

Requires: python3-tk:  `sudo apt-get install python3-tk`

## Execution
Simply call `python stuns/stuns.py -p <DATA_DIR>` where `<DATA_DIR>` is the path to a folder containing "user" folders.

There are many arguments you can invoke, simply do `python stuns/stuns.py --help` to see them. 

## Python Virtual Environment Setup
* `cd stuns/` change to the dir that will hold the virtual environment
* `python -m venv env/` creates a virtual environment for the tool (make sure it is python3)
* Windows: 
	* `.\env\Scripts\activate` to activate
	*  `where python` should give `.../env/bin/python.exe` 
* Linux:
	* `source env/bin/activate` to activate
	* `which python` should give `.../env/bin/python`
* Install the modules with `pip install -r requirements.txt`
* `deactivate` to exit virtual environment
* `pip freeze > requirements.txt` to export all the installed modules (the file `requirements.txt` should always be committed), in case new requirements are added.


## Docs
To generate the documentation, **activate** virtual environment, `cd stuns/docs` and:
 * Windows: `make.bat html`
 * Linux: `make html`
