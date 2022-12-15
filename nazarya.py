# from _curses import raw
#
# import numpy as np
#
# #a = np.array([[1,3,5],[6,56,9]])
# #a = np.array(range(1,37,2)).reshape(3,6)     #باید دقت کرد که اون که شکلمون رو رسم میکنه چندتا استیت میخوره و بزاش اونقدر استیت رسم کرد
# #print(a)
# #dfa = {a:{'0':a,'1':b}
# #       ,b:{'0':b,'1':c}
# #       ,c:{'0':c,'1':d}
# #       ,d:{'0':d,'1':f}
# #       ,f:{'0':d,'1':f}}
#
# # dfa = {0:{'0':0, '1':1},
# #        1:{'0':2, '1':0},
# #        2:{'0':1, '1':2}}
# #
# # def accepts(transitions,initial,accepting,s):
# #     state = initial
# #     for c in s:
# #         state = transitions[state][c]
# #     return state in accepting
# #
# # accepts(dfa,0,{0},'1011101')
#
# #nfa simulation for (a|b)*abb
# #state 4 is a trap state
#
#
# import sys
#
#
#
# def main():
#     transition = [[[0,1],[0]], [[4],[2]], [[4],[3]], [[4],[4]]]
#     input = raw_input("enter the string: ")
#     input = list(input) #copy the input in list because python strings are immutable and thus can't be changed directly
#     for index in range(len(input)): #parse the string of a,b in 0,1 for simplicity
#         if input[index]=='a':
#             input[index]='0'
#         else:
#             input[index]='1'
#
#     final = "3" #set of final states = {3}
#     start = 0
#     i=0  #counter to remember the number of symbols read
#
#     trans(transition, input, final, start, i)
#     print("rejected")
#
#
#
# def trans(transition, input, final, state, i):
#     for j in range (len(input)):
#         for each in transition[state][int(input[j])]: #check for each possibility
#             if each < 4:                              #move further only if you are at non-hypothetical state
#                 state = each
#                 if j == len(input)-1 and (str(state) in final): #last symbol is read and current state lies in the set of final states
#                     print("accepted")
#                     sys.exit()
#                 trans(transition, input[i+1:], final, state, i) #input string for next transition is input[i+1:]
#         i = i+1 #increment the counter
#
#
# main()

class NFA:
    def __init__(self):
        self.num_states = 0
        self.states = []
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []



    def construct_nfa_from_file(self, lines):
        self.num_states = int(lines[0])
        self.init_states()
        self.symbols = list(lines[1].strip())

        accepting_states_line = lines[2].split(" ")
        for index in range(len(accepting_states_line)):
            self.accepting_states.append(int(accepting_states_line[index]))

            # if index == 0:
            #     self.num_accepting_states = int(accepting_states_line[index])
            # else:
            #     self.accepting_states.append(int(accepting_states_line[index]))
        self.num_accepting_states = int(len(accepting_states_line))
        self.startState = int(lines[3])

        for index in range(4, len(lines)):
            transition_func_line = lines[index].split(" ")

            starting_state = int(transition_func_line[0])
            transition_symbol = transition_func_line[1]
            ending_state = int(transition_func_line[2])

            transition_function = (starting_state, transition_symbol, ending_state);
            self.transition_functions.append(transition_function)


    def init_states(self):
        self.states = list(range(self.num_states))


    def print_nfa(self):
        print(self.num_states)
        print(self.states)
        print(self.symbols)
        print(self.num_accepting_states)
        print(self.accepting_states)
        print(self.start_state)
        print(self.transition_functions)



class DFA:
    def __init__(self):
        self.num_states = 0
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []
        self.q = []

    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols
        self.start_state = nfa.start_state

        nfa_transition_dict = {}
        dfa_transition_dict = {}

 # Combine NFA transitions
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]

            if (starting_state, transition_symbol) in nfa_transition_dict:
                nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)        #0 -a->0,1
            else:
                nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]             #0 -a-> 0   0 -b->0   1 -b-> 2

        self.q.append((0,))
 # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            for symbol in nfa.symbols:
                if  (dfa_state, symbol) in nfa_transition_dict:                     #dfa_dtate[0]              len(dfa_state) == 1 and
                    dfa_transition_dict[(dfa_state, symbol)] = nfa_transition_dict[(dfa_state, symbol)]    #dfa_dtate[0]

                    if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))

                else:
                    destinations = []
                    final_destination = []

                    for nfa_state in dfa_state:                                                                                                                                      # start of 0 to dfa_state
                        if (nfa_state, symbol) in nfa_transition_dict and nfa_transition_dict[(nfa_state, symbol)] not in destinations:                                                                                            #
                            destinations.append(nfa_transition_dict[(nfa_state, symbol)])                                                                                            #enter the value of index 2 in destinations

                    if not destinations:
                        final_destination.append(None)
                    else:                                                                                                                                                            #قرار دادن استیت پایانی final
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)

                    dfa_transition_dict[(dfa_state, symbol)] = final_destination

                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))                                                                                                                      #complet all state

        # Convert NFA states to DFA states
        for key in dfa_transition_dict:
            self.transition_functions.append(
                (self.q.index(key[0]), key[1], self.q.index(tuple(dfa_transition_dict[key]))))

        for q_state in self.q:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.q.index(q_state))
                    self.num_accepting_states += 1

    def print_dfa(self):
        print(len(self.q))
        print("".join(self.symbols))
        print(str(self.num_accepting_states) + " " + " ".join(
            str(accepting_state) for accepting_state in self.accepting_states))
        print(self.start_state)

        for transition in sorted(self.transition_functions):
            print(" ".join(str(value) for value in transition))
