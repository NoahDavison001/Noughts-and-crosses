Noughts and Crosses app with various game modes (o_x.py):

vs Human allows user to play against someone else at the same computer

vs Algorithm allows user to play against a perfect strategic algorithm; prepare for a lot of draws

vs AI allows user to play against a Q-learning AI. after one training session, AI knows a lot of strategy, enough to block lines and even set up forced wins,
however still makes mistakes and is definately able to be beaten. more training sessions would perfect the gaps in its logic and raise it to the same level as
the algorithm play, and probably tweaked training variables would speed up training and result in a better AI.

"updated_training.py" is the training algorithm that can be run to generate and train the q-tables, one each for starting first or second. as default, tables are 
being trained against an opponent playing purely random moves for 5000 episodes on each table, before being moved onto playing an algorithm that wins or blocks 
lines where possible, else plays randomly, for another 10,000 episodes each. in my instance of the training data, ai quickly rose to a 75% and 55% win rate, playing 
as O and X respectively, against the random opponent, which dropped significantly when transitioning to the tougher opponent before rising to the same levels as 
previously. currently epsilon is set to decay over the course of training to begin to exploit its knowledge after gaining some strategy, althought this could be 
changed by just setting epsilon to the desired value and setting the decay to 1. i briefly experimented with a decaying learning rate, though this proved ineffective
in the end and i removed it. user should bear in mind there are different sets of training variables for stage 1 and stage 2 of training, if they intend to alter them.

after the training algorithm runs, it will load a graph showing the rolling average win rate and draw rate for each q-table, over the coarse of training. the default
window size is set to 500, although if the number of episodes is increased it is advised that this window size be altered similarly to make the graph readable.

potential future improvements include a stage 3 of AI training, where it plays against itself.
