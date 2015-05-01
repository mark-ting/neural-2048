from neural_network import *
from parse_game import *
from neural_AI import *


""" Trains the neural network AI over a given dataset """
def train_AI(network, filename, epoch=2000, starting_weights=None):
    data = parse_arr(load_datafile(filename))
    print(data)
    return network.train(data, epoch, starting_weights)

ai = NeuralAI()

w1 = train_AI(ai.network, "data/Output_1.txt", 1)
ai.network.load_weights(w1)
w2 = train_AI(ai.network, "data/Output_2.txt", 1)
ai.network.load_weights(w2)
w3 = train_AI(ai.network, "data/Output_3.txt", 1)
ai.network.load_weights(w3)
w4 = train_AI(ai.network, "data/Output_4.txt", 1)
ai.network.load_weights(w4)
w5 = train_AI(ai.network, "data/Output_5.txt", 1)
ai.network.load_weights(w5)
w6 = train_AI(ai.network, "data/Output_6.txt", 1)
ai.network.load_weights(w6)
w7 = train_AI(ai.network, "data/Output_7.txt", 1)
ai.network.load_weights(w7)
w8 = train_AI(ai.network, "data/Output_8.txt", 1)
ai.network.load_weights(w8)
w9 = train_AI(ai.network, "data/Output_9.txt", 1)
ai.network.load_weights(w9)
w10 = train_AI(ai.network, "data/Output_10.txt", 1)
ai.network.load_weights(w10)


# Run the AI, see what happened
while not(ai.board.game_over()):
    ai.move()

ai.board.print_game_over_message()