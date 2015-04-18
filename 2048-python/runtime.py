import argparse
from greedy_AI import GreedyAI

# command line argument intake for runtime options
parser = argparse.ArgumentParser(description="2048-python frontend",
                                 epilog="")

parser.add_argument('-a', '--ai', help="enable AI run mode",
                    action='store_true', default=False)

parser.add_argument('-s', '--searchdepth', help="set AI search depth",
                    type=int, choices=[1, 2, 3])

parser.add_argument('-l', '--log', help="outputs the AI run to a file",
                    metavar="FILENAME", default="outlog")

parser.add_argument('-v', '--verbosity', help="verbosity of log file",
                    type=int, choices=[1, 2], default=1)

# parser.add_argument('--ui', help="Run the game in a terminal UI")

args = parser.parse_args()

# parsed variables
log = args.log
verb = args.verbosity
depth = args.searchdepth


# main runtime
def main():

    if args.ai:
        ai = GreedyAI(iter=depth)

        if args.log:
            out = open(log + '.log', 'w')

        while not(ai.board.game_over()):
            if args.log:
                log_to_file(ai, out, verb, None)
            print(ai.board)
            ai.move()
    else:
        # FIXME: make UI have a method that is called; else python is gonna cry
        # runs manual UI (play using user input)
        import UI.py


# logs an AI's game data to a text file
def log_to_file(ai, file, verbosity=1, delimiter=None):

    if verbosity > 0:
        file.write(str(ai.board))
        if delimiter:
            file.write(delimiter)
        else:
            file.write("--------------------\n\n")

    # turn and score log
    if verbosity > 1:
        file.write("TURN: " + "###" + " | SCORE: " +
                   str(ai.board.score) + "\n")


main()
# class NoviceRuntime:
