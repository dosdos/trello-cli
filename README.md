# Trello interactive CLI #


### What is this repository for? ###
This tool is a Python wrapper around Trello REST API able to interact with Trello boards from the command line.

The current version '1.0' allows to:

* Get the list of your Trello boards
* Get the list of the columns in a given Trello board
* Create a new card in a given column of a board

### How do I get set up locally? ###
First, clone the project:

```
$ git git clone git@bitbucket.org:Dosdos/trello-cli.git
```

Second, you need to get an API key from [Trello Developer API Keys page](https://trello.com/app-key).
Make sure to paste them in the `.env` file, that you need to create in the `trellocli` folder.
Look at the [.env.template](trellocli/.env.template) file to get an example.

The tool is depending on [Typer](https://typer.tiangolo.com/), then you need to install it.
A requirement file is included, so you can easily setup a virtualenv and install it.

For example, if you use *virtualenvwrapper*, you can create a new env
```
$ mkvirtualenv -p python3 trellocli
```

or execute an existing one:
```
$ workon trellocli
```

Move to the root folder of the `trellocli` project and use pip to update dependencies from the requirements file:
```
$ cd trellocli
$ pip3 install -r requirements-local.txt
```

Now you can run the script using `python -m`; the `-m` option helps to run the library module as a script.

Try it out:

```
$ python -m trellocli --help
```

### How does it work? ###
You can use the tool to:

* Get the list of your Trello boards:

```
$ python -m trellocli list-boards
```

* Pick a *Board ID* from the previous response and get the list of the columns in that Trello board:

```
$ python -m trellocli list-columns <board-id>
```

* Pick a *Column ID* from the previous response and create a new card (follow the instruction to add a comment and labels):

```
$ python -m trellocli create-card -c <column-id>
```


### Run tests ###

To run unit tests simply type:

```
$ python -m unittest
```

### Contribution guidelines ###

Feel free to:

* Writing more tests
* Doing code review
* Add comments

### Who do I talk to? ###

* Repo owner or admin: dosdos
* Contact: dav.santucci@gmail.com

### What's next? ###

Further readings (and some links where I got inspiration from):

* [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-post): the official Trello API documentation
* [py-trello](https://github.com/sarumont/py-trello): a nice Python wrapper for Trello API
* [Typer-Todo-CLI](https://github.com/Sachin-chaurasiya/Typer-Todo-CLI/tree/main/todo): a simple example to start with Typer
* [unittest](https://docs.python.org/3/library/unittest.html): the official docs about unittest

Next developments:

* Increase unit tests coverage (e.g. cli commands and exceptions cases)
* Add integration tests for Trello API (need a Trello board for testing purposes)
* Give a better structure to trello utils (atm objects, exceptions and functions live together)
* Clean constants all around the code
* Implement more functions (e.g. create columns, move cards, ...)
