"""
COMP SCI 7059 || Assignment 01 || Problem 1 Tic-tac-toe
Submitted by: Arpit Gole || a1814270

Below program demonstrates the game play of tic-tac-toe
in 3 different settings to make computation less expensive
step by step.
1. Minimax algorithm.
2. Alpha-beta pruning in minimax algorithm.
3. Early termination with Alpha-beta pruning in minimax algorithm.
"""

import sys
import copy


class Tic_tac_toe():
    def __init__(self, state, path, prune=None, ply=None):
        # Game's starting set up.
        # Convert rastor string into matrix form
        self.initial_state = \
            [list(state)[steps:steps + 3] for steps in range(0, len(state), 3)]
        self.path = path
        self.prune = prune
        self.ply = int(ply)
        # Record of visited nodes with the minimax value
        self.visited_node = []

    def convert_matrix_rastor(self, state_matrix):
        """
        Converts state represented in matrix form back to rastor string
        Parameters
        ----------
        state_matrix: A 3 X 3 matrix of board state.

        Returns
        -------
        Rastor string of the supplied board state.
        """
        result_rastor = ''

        for i in range(3):
            for j in range(3):
                result_rastor += state_matrix[i][j]

        return result_rastor

    def player(self, state):
        """
        Which player has the move in the state.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        Either Max's(x) or Min's(o) based on game play logic
        """
        no_of_moves_by_player_1 = 0
        no_of_moves_by_player_2 = 0

        # Just count the number of 'x' and 'o' to find out whose
        # turn is next
        for row_values in state:
            no_of_moves_by_player_1 += row_values.count('x')
            no_of_moves_by_player_2 += row_values.count('o')

        if no_of_moves_by_player_1 == no_of_moves_by_player_2:
            return 'x'

        elif no_of_moves_by_player_1 > no_of_moves_by_player_2:
            return 'o'

        elif no_of_moves_by_player_2 > no_of_moves_by_player_1:
            return 'x'

    def terminal_test(self, state):
        """
        To check if the game has ended or not.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A tuple specifying game over or not and the respective winner.
        """
        # Anyone won already?
        ended, winner = self.anyone_won(state)

        if ended:
            return ended, winner
        else:
            # Checking if still game play is left
            for row_value in state:
                for column_value in row_value:
                    if column_value == '-':
                        return False, None

        # It's a draw
        return True, None

    def anyone_won(self, state):
        """
        To find the winner for the given state of the board.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A tuple specifying game over or not and the respective winner.
        """
        # Checking all the rows
        for row_values in state:
            if row_values.count('x') == 3:
                return True, 'x'
            if row_values.count('o') == 3:
                return True, 'o'

        # Checking all the columns
        for i in range(3):
            if state[0][i] == 'x' and state[1][i] == 'x' and state[2][i] == 'x':
                return True, 'x'
            if state[0][i] == 'o' and state[1][i] == 'o' and state[2][i] == 'o':
                return True, 'o'

        # Checking all the diagonals
        if (state[0][0] == 'x' and state[1][1] == 'x' and state[2][2] == 'x') \
                or (state[0][2] == 'x' and state[1][1] == 'x' and state[2][0] == 'x'):
            return True, 'x'

        if (state[0][0] == 'o' and state[1][1] == 'o' and state[2][2] == 'o') \
                or (state[0][2] == 'o' and state[1][1] == 'o' and state[2][0] == 'o'):
            return True, 'o'

        return False, None

    def utility(self, state):
        """
        Defines the final numeric value for a game that ends in
        terminal state s for a player p.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A payoff value.
        """

        ended, winner = self.terminal_test(state)

        if ended and winner == 'x':
            return 1
        if ended and winner == 'o':
            return -1
        else:
            return 0

    def actions(self, state):
        """
        To fetch all of legal moves.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A set of legal moves in a given state.
        """
        valid_actions = []

        for i in range(3):
            for j in range(3):
                if state[i][j] == '-':
                    valid_actions.append((i, j))

        return copy.deepcopy(valid_actions)

    def result(self, state, action):
        """
        To fetch the resultant board state when current player plays
        at the specified location.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        action: index value

        Returns
        -------
        A transition board state resultant of the action performed.
        """
        current_player = self.player(state)

        i, j = action
        sc = copy.deepcopy(state)

        if current_player:
            sc[i][j] = current_player
            return sc
        else:
            raise Exception('Unable to identify the current player')

    def visited_nodes_to_file(self):
        """
        Writes the visited nodes with the corresponding minimax values to
        the specified path.
        """
        with open('{}'.format(self.path), mode='w') as f:
            # Writing line by line to the file
            for node, val in self.visited_node:
                f.write('{} {}\n'.format(self.convert_matrix_rastor(node), val))

    def depth_check(self, depth):
        """
        To check if the specified depth of the game tree is reached.
        Parameters
        ----------
        depth: Current depth of the game tree

        Returns
        -------
        True if the limit is reached and further computation needs to stop
        otherwise False.
        """
        if depth >= self.ply:
            return True
        return False

    def terminal_check(self, state, depth):
        """
        Determine if further computation needs to stop or not
        based on the depth and the state of the board.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        depth: Current depth of the game tree

        Returns
        -------
        True if computation needs to stop otherwise False.
        """
        early_terminated = self.depth_check(depth)
        ended, winner = self.terminal_test(state)

        if early_terminated or ended:
            return True

        return False

    def utility_et(self, state):
        """
        Defines the final numeric value for a game that ends in
        terminal state s for a player p or by early termination logic.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A payoff value.
        """

        # Here ms and os are respectively the number of possible winning
        # lines for Max and Min after state s.
        # es is the chosen evaluation function.
        es, ms, os = 0, 0, 0

        # Check all the rows
        for row_values in state:
            if row_values.count('x') + row_values.count('-') == 3:
                ms += 1
            if row_values.count('o') + row_values.count('-') == 3:
                os += 1

        # Check all the columns
        for i in range(3):
            if ((state[0][i] == 'x' or state[0][i] == '-')
                    and (state[1][i] == 'x' or state[1][i] == '-')
                    and (state[2][i] == 'x' or state[2][i] == '-')):
                ms += 1
            if ((state[0][i] == 'o' or state[0][i] == '-')
                    and (state[1][i] == 'o' or state[1][i] == '-')
                    and (state[2][i] == 'o' or state[2][i] == '-')):
                os += 1

        # Check diagonal 1 by 1
        if ((state[0][0] == 'x' or state[0][0] == '-')
                and (state[1][1] == 'x' or state[1][1] == '-')
                and (state[2][2] == 'x' or state[2][2] == '-')):
            ms += 1

        if ((state[0][2] == 'x' or state[0][2] == '-')
                and (state[1][1] == 'x' or state[1][1] == '-')
                and (state[2][0] == 'x' or state[2][0] == '-')):
            ms += 1

        if ((state[0][0] == 'o' or state[0][0] == '-')
                and (state[1][1] == 'o' or state[1][1] == '-')
                and (state[2][2] == 'o' or state[2][2] == '-')):
            os += 1

        if ((state[0][2] == 'o' or state[0][2] == '-')
                and (state[1][1] == 'o' or state[1][1] == '-')
                and (state[2][0] == 'o' or state[2][0] == '-')):
            os += 1

        # Evaluation function
        es = ms - os
        return es

    def minimax_decision(self, state):
        """
        An algorithm for calculating minimax decisions.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        A tuple of best action based on minimax algorithm with the corresponding value.
        """

        # Here implementing custom version of arg max, keeping all the problem
        # criterion in mind.
        # Implementing MIN-VALUE and MAX-VALUE separate for each variant.
        all_actions_from_root = self.actions(state)
        player_current = self.player(state)
        best_action = ()

        # Early terminated alpha-beta pruned minimax algorithm
        if self.ply and self.prune:
            if player_current == 'x':
                best_action = self.max_value_prune_et(state, all_actions_from_root[0], -999, 999, 0)
            else:
                best_action = self.min_value_prune_et(state, all_actions_from_root[0], -999, 999, 0)
        # alpha-beta pruned minimax algorithm
        elif self.prune:
            if player_current == 'x':
                best_action = self.max_value_prune(state, all_actions_from_root[0], -999, 999)
            else:
                best_action = self.min_value_prune(state, all_actions_from_root[0], -999, 999)
        # minimax algorithm
        else:
            if player_current == 'x':
                best_action = self.max_value(state, all_actions_from_root[0])
            else:
                best_action = self.min_value(state, all_actions_from_root[0])

        # Tuple of best action (best action value, best action)
        return best_action

    def min_value(self, state, l_action):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by minimising the value.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended, winner = self.terminal_test(state)

        if ended:
            # Calculate the utility value
            return self.utility(state), l_action

        # Variables to check against
        v = 999
        g_action = (5, 5)

        for action in self.actions(state):
            # resultant state after taking action on the state
            rd = self.result(state, action)
            vv = self.max_value(rd, action)

            # Minimising the value
            if v > vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rd), vv[0]))

        # (best action value, best action)
        return v, g_action

    def max_value(self, state, l_action):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by maximising the value.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended, winner = self.terminal_test(state)

        if ended:
            # Calculate the utility value
            return self.utility(state), l_action

        # Variables to check against
        v = -999
        g_action = (6, 6)

        for action in self.actions(state):
            # resultant state after taking action on the state
            rs = self.result(state, action)
            vv = self.min_value(rs, action)

            # Maximising the value
            if v < vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rs), vv[0]))

        return v, g_action

    def min_value_prune(self, state, l_action, alpha, beta):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by minimising the value, but
        prunes away branches that cannot possibly influence the final decision.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.
        alpha: The value of the best (i.e., highest-value) choice we have found so far at any choice point
                along the path for MAX.
        beta: = The value of the best (i.e., lowest-value) choice we have found so far at any choice point
                along the path for MIN.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended, winner = self.terminal_test(state)

        if ended:
            # Calculate the utility value
            return self.utility(state), l_action

        # Variables to check against
        v = 999
        g_action = (5, 5)

        for action in self.actions(state):
            rd = self.result(state, action)
            vv = self.max_value_prune(rd, action, alpha, beta)

            # Minimising the value
            if v > vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rd), vv[0]))

            # Update beta and prune the search
            if v <= alpha:
                return v, action
            beta = min(beta, v)

        return v, g_action

    def max_value_prune(self, state, l_action, alpha, beta):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by maximising the value, but
        prunes away branches that cannot possibly influence the final decision.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.
        alpha: The value of the best (i.e., highest-value) choice we have found so far at any choice point
                along the path for MAX.
        beta: = The value of the best (i.e., lowest-value) choice we have found so far at any choice point
                along the path for MIN.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended, winner = self.terminal_test(state)

        if ended:
            # Calculate the utility value
            return self.utility(state), l_action

        v = -999
        g_action = (6, 6)

        for action in self.actions(state):
            rs = self.result(state, action)
            vv = self.min_value_prune(rs, action, alpha, beta)

            # Maximising the value
            if v < vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rs), vv[0]))

            # Update alpha and prune the search
            if v >= beta:
                return v, action
            alpha = max(alpha, v)

        return v, g_action

    def min_value_prune_et(self, state, l_action, alpha, beta, d):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by minimising the value, but
        prunes away branches that cannot possibly influence the final decision.
        It will call the heuristic function when it is appropriate to cut off the search.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.
        alpha: The value of the best (i.e., highest-value) choice we have found so far at any choice point
                along the path for MAX.
        beta: = The value of the best (i.e., lowest-value) choice we have found so far at any choice point
                along the path for MIN.
        d: Current depth of the game tree.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended = self.terminal_check(state, d)

        if ended:
            # Calculate the utility value based on heuristic function
            return self.utility_et(state), l_action

        v = 999
        g_action = (5, 5)

        for action in self.actions(state):
            rd = self.result(state, action)
            vv = self.max_value_prune_et(rd, action, alpha, beta, d + 1)

            if v > vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rd), vv[0]))

            # Update beta and prune the search
            if v <= alpha:
                return v, action
            beta = min(beta, v)

        return v, g_action

    def max_value_prune_et(self, state, l_action, alpha, beta, d):
        """
        To go through the whole game tree, all the way to the leaves,
        to determine the backed-up value of a state by maximising the value, but
        prunes away branches that cannot possibly influence the final decision.
        It will call the heuristic function when it is appropriate to cut off the search.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        l_action: Last action taken according to minimax algorithm.
        alpha: The value of the best (i.e., highest-value) choice we have found so far at any choice point
                along the path for MAX.
        beta: = The value of the best (i.e., lowest-value) choice we have found so far at any choice point
                along the path for MIN.
        d: Current depth of the game tree.

        Returns
        -------
        A tuple of best action (best action value, best action)
        """
        ended = self.terminal_check(state, d)

        if ended:
            # Calculate the utility value based on heuristic function
            return self.utility_et(state), l_action

        v = -999
        g_action = (6, 6)

        for action in self.actions(state):
            rs = self.result(state, action)
            vv = self.min_value_prune_et(rs, action, alpha, beta, d + 1)

            if v < vv[0]:
                v = vv[0]
                g_action = action

            # Updating the record of visited state and the corresponding minimax value
            self.visited_node.append((copy.deepcopy(rs), vv[0]))

            # Update alpha and prune the search
            if v >= beta:
                return v, action
            alpha = max(alpha, v)

        return v, g_action

    def play(self):
        """
        Simulates a tic-tac-toe gameplay
        """
        state = copy.deepcopy(self.initial_state)
        # calculating the best move value and action for the given state
        best_action = self.minimax_decision(state)

        # Making the best move corresponding to the initial state
        state = copy.deepcopy(self.initial_state)
        expected_state = self.result(state, best_action[1])

        # Printing the board state resulting from the best move.
        print '{}'.format(self.convert_matrix_rastor(expected_state))


if __name__ == '__main__':

    # Capturing the command line arguments
    state_1 = sys.argv[1]
    path_1 = sys.argv[2]

    try:
        prune_1 = sys.argv[3]
        prune_1 = True
    except IndexError as e:
        prune_1 = False

    try:
        ply_1 = sys.argv[4]
    except IndexError as e:
        ply_1 = False

    # Initialising the tic-tac-toe game class
    game = Tic_tac_toe(state_1, path_1, prune_1, ply_1)

    # Play the game
    game.play()

    # Print all the nodes visited to the specified output file
    game.visited_nodes_to_file()
