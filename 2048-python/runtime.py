import argparse
from greedy_AI import GreedyAI
from neural_AI import NeuralAI

""" Command-line argument intake for runtime options """
parser = argparse.ArgumentParser(description="2048-python frontend",
                                 epilog="")

parser.add_argument('-a', '--ai', help="enable AI run mode",
                    action='store_true', default=False)

parser.add_argument('-g', '--greedy', help="sets AI to be greedy",
                    action='store_true', default=False)

parser.add_argument('-d', help="set AI search iterations",
                    metavar="ITER", type=int, dest='searchdepth')

parser.add_argument('-s', '--seed', help="custom seed for 2048 placement RNG",
                    type=int)

parser.add_argument('-l', '--log', help="outputs the AI run to a file",
                    metavar="FILE", default="outlog")

parser.add_argument('-v', '--verbosity', help="verbosity of log file",
                    type=int, choices=[1, 2], default=1)

# parser.add_argument('--ui', help="Run the game in a terminal UI")

# List of parsed variables
args = parser.parse_args()

ai_enabled = args.ai
ai_greedy = args.greedy
depth = args.searchdepth
seed = args.seed


log = args.log
verb = args.verbosity

trained_matrix = [] # training matrix here!

def main():
    """ Main runtime """

    if ai_enabled:
        if ai_greedy:
            ai = GreedyAI(iter=depth)

        else:
            ai = NeuralAI(trained_matrix)

        if log:
            out = open(log + '.log', 'w')

        while not(ai.board.game_over()):
            if args.log is not None:
                log_to_file(ai, out, verb, None)
            print(ai.board)
            ai.move()

        print("TURN: " + str(ai.board.num_steps) + " | SCORE: " +
              str(ai.board.score) + "\n")

    # Runs the UI version
    else:
        import UI.py     # runs manual UI (play using user input)


def log_to_file(ai, file, verbosity, delimiter=None):
    """ Logs an AI's game run to a text file """

    # Print turn and score information
    if verbosity > 1:
        file.write("TURN: " + str(ai.board.num_steps) + " | SCORE: " +
                   str(ai.board.score) + "\n")

    # Print runtime board states
    if verbosity > 0:
        file.write(str(ai.board))
        if delimiter:
            file.write(delimiter)
        else:
            file.write("--------------------\n\n")

main()
