# chess_tournaments

This code allow to manage a chess tournament.
The user can create a tournament with adding players, the first round is automatically created with the match corresponding.
The user can consult the result of the tournament at each time.

### Prerequisites

This project is developped in Python, if you did not get a python environnement you can download it from : https://www.python.org/downloads/
You can also download IDE (Integrated Development Environment) like sypder, pycharm, Jupyter Notebook... It usually provides features such as build automation, code linting, testing and debugging.<br />
On my side, I developped this project with spyder.


### Installing

The first step is to retreive the files from github. You can install Git on your computer with the following link : https://git-scm.com/downloads
Move to the folder where you wish to saved this project using the command cd C:/Users/XXXX/XXXX/XXXX<br />
We will then clone the file located in the Github platform using the following command in Git prompt : <br />
>git init<br />
>git remote add Name_given https://github.com/amelie2107/chess_tournaments.git <br />
>git clone https://github.com/amelie2107/chess_tournaments.git <br />

The second step is to work on the same environnement, I mean with the same package versions to be sure the project will be run in the same condition as me. 
For that, you can run the "requirement.txt" file using the following lines in your command prompt :<br />
>Python -m venv env #to create the new virtual environnement<br />
>env\\Scripts\\Activate.ps1 #to activate the environnement<br />
>pip install -r requirements.txt #to download the package in the required version<br />


### Running the tests

You can then lauch the python file using the following line :<br />
>python main.py<br />

The programm is running.<br />
The menu appear :<br />
>************************** menu ***************************
>|                                                         |
>| 0 - add new player                                      |
>| 1 - create tournament                                   |
>| 2 - show all players list                               |
>| 3 - show players list of a tournament                   |
>| 4 - show tournaments list                               |
>| 5 - show round list                                     |
>| 6 - show match list                                     |
>| 7 - launch/continue tournament                          |
>| 8 - input match result                                  |
>| 9 - update player ranking                               |
>| 10 - show tournament's results                          |
>| 11 - exit                                               |
>|                                                         |
>***********************************************************
>please enter your choice (index) : 

You can choose what you plan to do, the program will lead you to run a tournament.

### Flake8

You can check if the code observe the PEP8 using Flake8 with a maximum of 119 caracteres by line.
From you consol, Windows Powershell in my case, you can use the following code :
> python -m pip install flake8
> flake8 --format=html --htmldir=flake8-rapport --max-line-length=119

### Deployment

To improve this programm, it could be nice to retreive the players's emails and informed them of the tournaments in progress of to plan.
In addition, the tournaments results can be available from anywhere, by anybody.

### Author

* **Amélie Noury** 

### Acknowledgments

* This project has been requested by the openclassroom training


