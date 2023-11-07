# Table 4 Phase 3 Project


## Home

* [Dependencies](#dependencies)
* [Starting the Application](#starting-the-application)
* [Using the Application](#using-the-application)
* [Optional Features](#optional-features)
* [License](#license)
* [Attributions](#attributions)
* [What I Learned](#what-i-learned)


## Intro To Project

- This is a project where a user can play various games in their terminal.
- This project was made to complete the assignment `Phase 3 Project` for the `SE-West-091123` class for the [Flatiron](https://flatironschool.com/) Software Engineering Boot Camp.
- The project was completed using the following: `python`, `sqlite3`.


## Dependencies

- The following is needed to run this application: `pyenv`, `python`, `sqlite3`.

- You must have access to these dependencies in the directory that you are running this application in. If your environment does not have these requirements, you may install them in this order by going to these websites and following the installation instructions:

- [pyenv](https://realpython.com/intro-to-pyenv/#installing-pyenv)

- [python](https://www.python.org/)

- `sqlite3` should come standard on the `macOS`. You can check by typing `which sqlite3` in the terminal. If you do not see a response like `/usr/bin/sqlite3` then you probably need to install it. Go here to do so [codecademy - install sqlite on mac](https://www.codecademy.com/resources/videos/setting-up/how-to-install-sqlite-on-mac)

- To install `sqlite3` on a `windows` machine, go here [codecademy - install sqlite on windows](https://www.codecademy.com/resources/videos/setting-up/how-to-install-sqlite-on-windows)


## Starting the Application

- Open a terminal window in the main directory of where this project is located on your computer.
- Run `pipenv install`.
- Then run `./cli.py`
- It should take you to the main menu of this app that looks like this:
- ==============================================
    ![Login page of app.](./images/login.png "Login Page")
- ==============================================
- It should take you to the main menu of this app that looks like this:
- ==============================================
    ![Home page of app.](./images/menu.png "Home Page")
- ==============================================


## Using the Application

- The user can scroll through the list of cards the app sells. The user can display a card in the card section located on the right side of the page by clicking on the card desired.
- The user can also display a card by typing a card name in the search bar located in the top right area of the page. There is also functionality to bring up possible options for the user to choose from as the user types in names. The options are located in a dropdown right under the search bar that appears when the user starts typing.
- When the card is displayed, the user will be shown more detailed information about the card and be given the option to add the card to the user's cart, if the card is in stock. If the user adds a card to the cart, the quantity of that card will be updated on the page.
- The user can access their cart by clicking the cart icon located in the top right of the page. When the user does so, a modal pops up on the page that displays some information about the user and keeps a running total of the items the user clicked on.
- At the bottom of the modal is a submit button that will create a document of the order and store it in the database. When the user completes an order, the inventory in the database will be updated.


## Optional Features

- The user can adjust the order in which the cards are listed by selecting the different options located at the top of every column. For example, the user can click on the 'Name' option and sort the list alphabetically or the reverse.
- The user can switch the color theme of the app by clicking the moon located in the top right area of the page, to the right of the search bar.
- It should look like this:
- ==============================================
    <!-- ![Home page of app.](./assets/dark-index.png "Home Page") -->
- ==============================================


## License

- This project is is made in conjunction with the standard `MIT` license provided by `GitHub` upon creation of a new repository. A copy of the license is included with this project in a file named: `LICENSE`.


## Attributions

- The project was completed with collaboration from: `Danner Baumgartner`, `Isaac Song`, and `Brian Richie Sr.`
- This project was created with combination of skills learned from the `Flatiron` curriculum and our own individual research.
- The data used to seed the original data prior to being modified for the purposes of this project was supplied by [Dracos](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93) created by `M Somerville`. The data consisted of an expansive file of 5-letter words for our version of [Wordle](https://en.wikipedia.org/wiki/Wordle) created by `Josh Wardle`.
- We used [Array_This](https://arraythis.com/) created by `populu` to convert the data in an iterable list to easily store each word in our database.
- We used [Free Dictionary Api](https://dictionaryapi.dev/) created by [Suraj (github handle - meetDeveloper)](https://github.com/meetDeveloper) to check the validity of each word entered by the user in the `Anagrams` game.
- We used [Hangman](https://github.com/Xethron/Hangman/blob/master/words.txt) created by [Bernhard Breytenbach (github handle - Xethron)](https://github.com/Xethron) to seed the database with Hangman words and phrases
- And of course, thank you [Stack Overflow](https://stackoverflow.com/).

## What I Learned

- `Danner`: Lorem Ipsum
- `Isaac`: Lorem Ipsum
- `Brian`: I learned a lot more about the versatility of `Python` in its ability to interface with `SQL` databases and the terminal directly. I can see the potential of combining `Python` with a front-end langauge to make some incredible apps. The team was great. We collaborated well and were very supportive of each other's struggles with completing this project. We also inspired one another's creativity throughout this process. Thank you Danner, Isaac, and the `Flatiron` community.


* [Back To Top](#table-4-phase-3-project)