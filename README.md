# (Interactive) Tic Tac Toe

This tic tac toe project contains two main parts. First, it takes in the
tictactoe-data.csv file, which contains moves for 200+ games of tic tac toe
between 10 different players. This data is summarized in the results.txt file
by the records, win percentage, and moves made by the players both as X and O.
Using the data, I modeled the playing tendencies of the 10 players using 
Decision Trees, which are used in the second part. The second part is a 
playable version of the game, where there are three options. You can:
1. Simulate matches between any two of the ten models of
   the players.
2. Play one of the models head-to-head
3. Play head-to-head with a friend on your local machine

To play the game, execute the following in the proper directory:

	python3 tic_tac_toe.py (py -3 on Windows)
