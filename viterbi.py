class state:

    def __init__(self, name, symbols, probabilities, start_probability):
        self.name = name  # string
        self.symbols = symbols # list
        self.probabilities = probabilities # list
        self.start_probability = start_probability

    def __repr__(self):
        return "State " + self.name + " with symbols " +  ', '.join(self.symbols)

    def starting_probability(self):
        return self.start_probability

    def symbol_probability(self,letter):
        return self.probabilities[self.symbols.index(letter)]

class hmm:

    def __init__(self, states, transitions):
        self.states = states # list of states - all states in hmm
        self.transitions = transitions # list of lists - transitions between states

    def __repr__(self):
        rep = "HMM with states:\n"
        for s in self.states:
            rep += str(s) + "\n"
        return rep

    def number_of_states(self):
        return len(self.states)

    def transition(self,i,j):
        return self.transitions[i][j]

def viterbi(hmm, string):

    v = [[0 for s in string] for state in range(hmm.number_of_states())]
    pointers = [[0 for s in range(len(string)-1)] for state in range(hmm.number_of_states())]

    for i in range(len(string)):
        for j in range(hmm.number_of_states()):
            if i == 0: # probability of initial state
                v[j][i] = hmm.states[j].starting_probability() * hmm.states[j].symbol_probability(string[i])
            else:
                possible_paths = [v[j][i-1]*hmm.transition(j,j)]#the same state
                possible_paths_pointers = [j]
                for y in [x for x in range(hmm_example.number_of_states()) if x != j]:
                    possible_paths.append(v[y][i-1]*hmm.transition(y,j))
                    possible_paths_pointers.append(y)
                v[j][i] = hmm.states[j].symbol_probability(string[i]) * max(possible_paths)
                pointers[j][i-1] = possible_paths_pointers[possible_paths.index(max(possible_paths))]

    #states
    states = ""
    i = len(string) - 1
    last_column = [x[i] for x in v]
    s = last_column.index(max(last_column))# max value in last column
    i -= 1
    while i >= 0:
        states += hmm.states[s].name
        s = pointers[s][i]
        i -= 1
    states += hmm.states[s].name

    return v,max(last_column),states[::-1]

def forward_algorithm(hmm, string):
    #what is the probability that the string was generated by the hmm model

    v = [[0 for s in string] for state in range(hmm.number_of_states())]
    for i in range(len(string)):
        for j in range(hmm.number_of_states()):
            if i == 0:  # probability of initial state
                v[j][i] = hmm.states[j].starting_probability() * hmm.states[j].symbol_probability(string[i])
            else:
                paths_sum = v[j][i - 1] * hmm.transition(j, j) # the same state
                for y in [x for x in range(hmm_example.number_of_states()) if x != j]:
                    paths_sum += v[y][i - 1] * hmm.transition(y, j)
                v[j][i] = hmm.states[j].symbol_probability(string[i]) * paths_sum

    return sum([x[-1] for x in v])#sum of the elements in last column

def backward_algorithm(hmm, string):

    v = [[1 for s in string] for state in range(hmm.number_of_states())]
    for i in reversed(range(len(string)-1)):
        for j in range(hmm.number_of_states()):
            paths_sum = v[j][i + 1] * hmm.transition(j, j) * hmm.states[j].symbol_probability(string[i+1]) #the same state
            #other states
            for y in [x for x in range(hmm_example.number_of_states()) if x != j]:
                paths_sum += v[y][i + 1] * hmm.transition(j, y) * hmm.states[y].symbol_probability(string[i+1])
            v[j][i] = paths_sum

    return sum([x[0]*hmm.states[i].starting_probability()*hmm.states[i].symbol_probability(string[0]) for i,x in enumerate(v)])# first column * starting probability * emision of the first symbol


if __name__ == "__main__":

    H = state("H",["A","C","G","T"],[0.2,0.3,0.3,0.2],0.5)
    L = state("L",["A","C","G","T"],[0.3,0.2,0.2,0.3],0.5)
    hmm_example = hmm([H,L],[[0.5,0.5],[0.4,0.6]])
    print hmm_example
    v, prob, states = viterbi(hmm_example,"GGCA")
    print "The most probable path is: " + states
    print "Its probability is " + str(prob)
    
    print "Forward algorithm result " + str(forward_algorithm(hmm_example,"GGCA"))
    print "Backward algorithm result " + str(backward_algorithm(hmm_example,"GGCA"))
