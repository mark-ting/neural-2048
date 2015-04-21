import argparse
from greedy_AI import GreedyAI

""" Command-line argument intake for runtime options """
parser = argparse.ArgumentParser(description="2048-python frontend",
                                 epilog="")

parser.add_argument('-a', '--ai', help="enable AI run mode",
                    action='store_true', default=False)

parser.add_argument('-d', help="set AI search iterations",
                    metavar="ITER", type=int, dest='searchdepth')

parser.add_argument('-s', '--seed', help="custom seed for 2048 RNG placement",
                    type=int)

parser.add_argument('-l', '--log', help="outputs the AI run to a file",
                    metavar="FILE", default="outlog")

parser.add_argument('-v', '--verbosity', help="verbosity of log file",
                    type=int, choices=[1, 2], default=1)

# parser.add_argument('--ui', help="Run the game in a terminal UI")

""" List parsed variables """
args = parser.parse_args()

ai_enabled = args.ai
depth = args.searchdepth
seed = args.seed


log = args.log
verb = args.verbosity


""" Main runtime """
def main():

    if ai_enabled:
        ai = GreedyAI(iter=depth, s=seed)

        if log:
            out = open(log + '.log', 'w')

        while not(ai.board.game_over()):
            if args.log:
                log_to_file(ai, out, verb, None)
            print(ai.board)
            ai.move()
    else:
        """ FIXME: make UI call a method; else python gonna cry """
        import UI.py     # runs manual UI (play using user input)


""" Logs an AI's game run to a text file """
def log_to_file(ai, file, verbosity, delimiter=None):

    """ Output Turn and Score information """
    if verbosity > 1:
        file.write("TURN: " + str(ai.board.num_steps) + " | SCORE: " +
                   str(ai.board.score) + "\n")

    """ Output runtime board states """
    if verbosity > 0:
        file.write(str(ai.board))
        if delimiter:
            file.write(delimiter)
        else:
            file.write("--------------------\n\n")


main()
# class NoviceRuntime:
