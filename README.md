  # Our problem statement is Knowledge Representation and Insight Generation from Structured Datasets(PS-12)
## About the Dataset
 
In this repository we have added two datasets named matches.csv and deliveries.csv - matches.csv contains the id, 
season, city, date, team1, team2, toss_winner, toss_decision, result, dl_applied, winner, win_by_runs, win_by_wickets, player_of_match, venue, umpire1, umpire2, umpire3 details,
whereas the deliveries.csv contains information about each ball delivered such as match_id, inning, batting_team, bowling_team, over, ball, batsman, non_striker, bowler, is_super_over, 
wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, player_dismissed, dismissal_kind, fielder.

## Jupyter Notebook and UI Components

Alongside the dataset we have the Jupyter notebook named PS12, all the knowledge that we could analyse from these datasets is shown, and we have generated meaningful statistical information
that helps one to understand and analyze the dataset better - up to 20 code snippets are available in the Jupyter Notebook. 
Adding to that our two inline models with UI integration, with the help of libraries that allow inline GUI for Jupyter Notebook.
(Although it is imported in the notebook, you may import the following for errorfree model implementation)
#### !pip install ipywidgets
#### !jupyter nbextension enable --py widgetsnbextension
#### !jupyter nbextension enable --py --sys-prefix ipywidgets

Apart from Inline UI, we have made three components using Tkinter, they are present in the repository by the name -
Pattern Identification UI, Player of the Match UI, Win Probability UI.

## Report and Documentation
The report is made according to the submission template with the info about the steps we took to come 
up with this final project. It is in PDF format and contains some snapshots of how the visualization is done in the notebook solution.
One needs to run the python files in the terminal to check out how the UI components look. The intent of each code snippet is in the markdown of the jupyter notebook. 

## Steps to run the project
Open the terminal and enter(make sure git is downloaded in your local system, if not check out this link - https://git-scm.com/downloads)
#### Clone the repository - git clone https://github.com/Rishita-Garg/ARP-INTEL-PS12-.git
Navigate to the repository and ensure Python and pip are installed by running (if not download from https://www.python.org/downloads/)
#### python --version
#### pip --version
Open the PS12 Jupyter notebook and run all to see the project and run the other Python files on the terminal to review the project.
Happy Coding
