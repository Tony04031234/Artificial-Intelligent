import sys
import copy

def write_to_file(file, state, utility):
  
	# open the output file for writing. This will delete any existing data
	outfile = open(file, 'a')

	# save the names into the file
	outfile.write(state  + ' ' + str(utility) + '\n')

	# close the file
	outfile.close()

# convert string to board 
def string_to_board(my_input):
	board = [ ['-', '-', '-'],
			  ['-', '-', '-'],
			  ['-', '-', '-'] ]
	count = 0
	for i in range(3):
		for j in range(3):
			board [i][j] = my_input[count]
			count = count + 1

	return copy.deepcopy(board)

#1 PLAYER(s): Defines which player has the move in a state.
def player(state):
	count_X = 0
	count_O = 0
	for i in range(3):
		for j in range(3):
			if state[i][j] == 'x':
				count_X = count_X + 1
			elif state[i][j] == 'o':
				count_O = count_O + 1
	if count_X == count_O:
		return 'x'
	elif count_X > count_O:
		return 'o'
	else:
		return 'x'

#2 find out -> list of legal moves. ex:[(1,0) (2,0) (2,2)] 
def action(state):
	# return list of legal moves which are the empty space 
	legal_move = []
	for i in range(3):
		for j in range(3):
			if state[i][j] == '-':
				legal_move.append([i,j])
			else:
				continue 
	
	return copy.deepcopy(legal_move)


#3 RESULT(s,a): The transition model, which defines the result of a move.
def result(state, action):

	my_action = action
	turn = player(state)
	
	my_copy_state = copy.deepcopy(state)
	# action is an array including [x , y] which is the index
	i, j=  my_action[0], my_action[1]

	my_copy_state[i][j] = turn

	return my_copy_state # the board with a new move made


#4TERMINAL-TEST(s): A terminal test, which is true when the game is over and false
#otherwise. States where the game has ended are called terminal states.
def terminal_test(state):

	#the winner in row
	for row in range(3):
		if state[row][0]==state[row][1]==state[row][2] and state[row][0] != '-':
			return True 


	#the winner in column
	for col in range(3):
		if state[0][col]==state[1][col]==state[2][col] and state[0][col] != '-':
			return True 


	#winner in one diagonal
	if state[0][0]==state[1][1]==state[2][2] and state[0][0] != '-':
		return True 

	#check winner in another diagonal
	if state[0][2]==state[1][1]==state[2][0] and state[0][2]!= '-':
		return True

	# game is not finished keep going asd
	for i in range(3):
		for j in range(3):
			if state[i][j] == '-':
				return False

	# draw
	return True


def terminal_test_winner(state):
	# the winner in row
	for row in range(3):
		if state[row][0] == state[row][1] == state[row][2] and state[row][0] != '-':
			if state[row][0] == 'x':
				return 'x'
			else:
				return 'o'

	# the winner in column
	for col in range(3):
		if state[0][col] == state[1][col] == state[2][col] and state[0][col] != '-':
			if state[0][col] == 'x':
				return 'x'
			else:
				return 'o'

	# winner in one diagonal
	if state[0][0] == state[1][1] == state[2][2] and state[0][0] != '-':
		if state[0][0] == 'x':
			return 'x'
		else:
			return 'o'

	# check winner in another diagonal
	if state[0][2] == state[1][1] == state[2][0] and state[0][2] != '-':
		if state[0][2] == 'x':
			return 'x'
		else:
			return 'o'
	else:
		return False


#5 UTILITY(s, p): A utility function x(also called an objective function or payoff function), 
#defines the final numeric value for a game that ends in terminal state s for a player p
def utility(state):

	if terminal_test(state) == True:
		player = terminal_test_winner(state)
		if player == 'x':
			return 1
		elif player == 'o':
			return -1
		else: 
			return 0
	elif terminal_test(state) == False:
		return 0
	else:
		return 'error'

#6 write function MIN-VALUE(state) returns a (utility value, action)
# minmax algorithm here 
def max_value(file, state, best_action, alpha, beta ):
	my_file = file 
	if terminal_test(state):
		return utility(state), best_action

	value = -10000000
	best_action_return = None
	my_alpha = alpha
	my_beta = beta

	for move in action(state):
		resultant_state = result(state, move) # store the board with a current move here
		max_value = min_value(my_file, resultant_state, move, my_alpha, my_beta) #run max_value function with current state

		if value < max_value[0]:
			value = max_value[0]
			best_action_return = move

		if value > my_beta or value == my_beta:
			best_action_return = move
			return value, best_action_return

		my_alpha = max(my_alpha, value)

		write_to_file(my_file, board_to_string(resultant_state), value)

	return value, best_action_return


# function MIN-VALUE(state) returns a (utility value, action)
def min_value(file, state, best_action, alpha, beta):
	my_file = file 
	if terminal_test(state):
		return utility(state), best_action

	value = 10000000
	best_action_return = None
	my_alpha = alpha
	my_beta = beta

	for move in action(state):

		resultant_state = result(state, move) # store the board with a current move here
		min_value = max_value(my_file, resultant_state, move, my_alpha, my_beta ) #run max_value function with current state
		# find min( value, min_value )
		
		# value = min(value, min_value[0]) # find smaller number
		# best_action_return = min_value[1]
		if value > min_value[0]:
			value = min_value[0]
			best_action_return = move

		if value < my_alpha or value == my_alpha: 
			best_action_return = move
			return value, best_action_return
		
		my_beta = min(my_beta, value)

		write_to_file(my_file, board_to_string(resultant_state), value)

	return value, best_action_return

def max_min_decision(file, state):
	
	my_file = file

	#if it's max's (x's) turn -> first call max_value()
	if player(state) == 'x':
		return max_value(my_file, state, None, -10000000, 100000000)
	#if it's min's (o's) turn -> first call min_value()
	else:
		return min_value(my_file, state, None, -100000000, 100000000)


#7 print to web sub, convert matrix back to string using rastor scan xxo---
def board_to_string(state):
	output = []
	my_str = ''
	for i in range(3):
		for j in range(3):
			output.append(state[i][j])
	my_str = my_str.join(output)
	return my_str

# Main game
def main(): 
	BEST_ACTION = None
	# S0: The initial state, which specifies how the game is set up at the start. xxo-----
	my_input = sys.argv[1]

	# write to the file 
	my_file = sys.argv[2]

	# my prune 
	#my_prune = sys.argv[3]

	# output the state in 2D matrix 
	my_state = string_to_board(my_input)
	#print(state)

	my_value = max_min_decision(my_file, my_state) # utility value and current state 
	#print(my_value[0])

	# Convert matrix to reaster scan - string
	my_final_state = board_to_string(result(string_to_board(my_input), my_value[1]) )
	print(my_final_state)

	# test write to file 
	# write_to_file(file , resultant_state, value)


if __name__ == '__main__':
	main()
