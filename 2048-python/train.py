from neural_network import *
from parse_game import *
from neural_AI import *


""" Trains the neural network AI over a given dataset """
def train_AI(network, filename, epoch=2000, starting_weights=None):
    data = parse_arr(load_datafile(filename))
    print(data)
    return network.train(data, epoch, starting_weights)

ai = NeuralAI()
print(train_AI(ai.network, "data/Output_41.txt", 500))

# Run the AI, see what happened
while not(ai.board.game_over()):
    ai.move()

print(ai.board)
ai.board.print_game_over_message()