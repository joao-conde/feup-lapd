# STUNS
> Structring The UNStructured

### Python Virtual Environment Setup
* `cd stuns/` change to the dir that will hold the virtual environment
* `python -m venv env/` creates a virtual environment for the tool
* Windows: 
	* `.\env\Scripts\activate` to activate
	*  `where python` should give `.../env/bin/python.exe` 
* Linux:
	* `source env/bin/activate` to activate
	* `which python` should give `.../env/bin/python`
* `deactivate` to exit virtual environment
* `pip freeze > requirements.txt` to export all the installed modules (the file `requirements.txt` should always be committed)
* Other users can enter then activate the virtual environment and install the modules with `pip install -r requirements.txt`

