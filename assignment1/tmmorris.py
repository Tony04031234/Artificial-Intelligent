"""
COMP SCI 7059 || Assignment 01 || Problem 2 Three Men's Morris
Submitted by: Arpit Gole || a1814270

Below program demonstrates the game play of three_men_morris
by Early termination with Alpha-beta pruning in minimax algorithm.

Various optional heuristic functions used for this game play are:

1. A utility function defines the final numeric value for a game
that ends in terminal state s for a player p. When the outcome
is a win for max, win for min, or draw, with values +1, -1, or 0.
CURRENTLY THIS UTILITY FUNCTION IS COMMENTED OUT.

2. A utility function which tries to come to the best possible
position in the game. Current player tries to increase it's number
of legal moves and decrease or limit the number of possible moves
for the other player. By doing so the current player is taking the
control of the board and tries to dominates.
CURRENTLY GAME PLAY USES THIS AS A DEFAULT UTILITY FUNCTION.
"""


import sys
import copy


class three_men_morris():
    def __init__(self, state, path, ply, turn):
        # Game's starting set up.
        # Convert rastor string into matrix form
        self.initial_state = \
            [list(state)[steps:steps + 3] for steps in range(0, len(state), 3)]
        self.path = path
        self.initial_turn = turn
        self.ply = int(ply)
        # Record of visited nodes with the minimax value
        self.visited_node = []
        # A look up table for legal moves from the given co-ordinate.
        self.valid_adjacent_positions = {
                (0, 0): [(0, 1), (1, 0)],
                (0, 1): [(0, 0), (0, 2), (1, 1)],
                (0, 2): [(0, 1), (1, 2)],
                (1, 0): [(0, 0), (1, 1), (2, 0)],
                (1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)],
                (1, 2): [(0, 2), (1, 1), (2, 2)],
                (2, 0): [(1, 0), (2, 1)],
                (2, 1): [(1, 1), (2, 0), (2, 2)],
                (2, 2): [(1, 2), (2, 1)]
            }

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

    def new_or_old_piece(self, state):
        """
        Defines whether to place a new piece in the game
        or move an existing piece. Since a game can have only
        6 pieces i.e. 3 x's and 3 o's.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.

        Returns
        -------
        If True, which new piece to introduce in the game.
        Otherwise None.
        """
        x_moves, o_moves = 0, 0

        for row_values in state:
            x_moves += row_values.count('x')
            o_moves += row_values.count('o')

        if x_moves + o_moves < 6:
            if x_moves > o_moves:
                return True, 'o'
            elif o_moves < x_moves:
                return True, 'x'
            else:
                return True, 'x'

        return False, None

    def player(self, state, current_player):
        """
        Which player has the move in the state.
        Parameters
        ----------
        state: A 3 X 3 matrix of board state.
        current_player: Supplied player if the initial state contains
        6 pieces already.
        Returns
        -------
        Either Max's(x) or Min's(o) based on game play logic.
        """

        new_piece, player = self.new_or_old_piece(state)

        if new_piece:
            return player
        else:
            return current_player

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
        # What kind of an action it will be
        # 1. Add a new piece to the game.
        # 2. Move and existing piece.
        new_piece, player = self.new_or_old_piece(state)

        # If we want to place a new piece in the game
        if new_piece:
            for i in range(3):
                for j in range(3):
                    if state[i][j] == '-':
                        # (player, to, from)
                        # Since we are introducing a new piece it's coming from
                        # an imaginary position i.e. (9, 9)
                        valid_actions.append((player, (i, j), (9, 9)))

        # when we moving an existing piece in the game
        else:
            for i in range(3):
                for j in range(3):
                    if state[i][j] != '-':
                        # Now check for places this player can move from this position
                        for ii, jj in self.valid_adjacent_positions[(i, j)]:
                            if state[ii][jj] == '-':
                                # (player, to, from)
                                valid_actions.append((state[i][j], (ii, jj), (i, j)))

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

        sc = copy.deepcopy(state)
        new_piece, player = self.new_or_old_piece(state)
        current_player, to_action, from_action = action

        # Make the move
        sc[to_action[0]][to_action[1]] = current_player

        # There can't be more than 6 pieces in any state.
        if not new_piece:
            # Now making from place as null again
            sc[from_action[0]][from_action[1]] = '-'

        return sc

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

        # There is no draw stage in this game, WTF.
        # It's always on !!
        if ended:
            return ended, winner
        else:
            # Checking if still game play is left
            return False, None

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

        return False, None

    def visited_nodes_to_file(self):
        """
        Writes the visited nodes with the corresponding minimax values to
        the specified path.
        """
        # Create and write file only if we have something to write
        if len(self.visited_node) > 0:
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

    # def utility_et(self, state):
    #     """
    #     Defines the final numeric value for a game that ends in
    #     terminal state s for a player p or by early termination logic.
    #     Parameters
    #     ----------
    #     state: A 3 X 3 matrix of board state.
    #
    #     Returns
    #     -------
    #     A payoff value.
    #     """
    #     ended, winner = self.terminal_test(state)
    #
    #     if ended and winner == 'x':
    #         return 1
    #     if ended and winner == 'o':
    #         return -1
    #     else:
    #         return 0

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
        weight_x, weight_o = 0, 0

        for i in range(3):
            for j in range(3):

                if state[i][j] != '-':
                    valid_moves = 0
                    for ii, jj in self.valid_adjacent_positions[(i, j)]:
                        if state[ii][jj] == '-':
                            valid_moves += 1

                    if state[i][j] == 'x':
                        weight_x += (valid_moves*-1)

                    if state[i][j] == 'o':
                        weight_o += (valid_moves*1)

        result = weight_x + weight_o
        return result

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
        player_current = self.player(state, self.initial_turn)
        best_action = ()

        # Early terminated alpha-beta pruned minimax algorithm
        if player_current == 'x':
            best_action = self.max_value_prune_et(state, (9, 9, 9), -999, 999, 0, player_current)
        else:
            best_action = self.min_value_prune_et(state, (9, 9, 9), -999, 999, 0, player_current)

        # Tuple of best action (best action value, to co-ordinate, from co-ordinate)
        return best_action

    def min_value_prune_et(self, state, l_action, alpha, beta, d, cp):
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
        beta: The value of the best (i.e., lowest-value) choice we have found so far at any choice point
                along the path for MIN.
        d: Current depth of the game tree.
        cp: Current player for the context.

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
        actions = []

        # Legal actions for the current player
        for action in self.actions(state):
            if action[0] == cp:
                actions.append(action)

        for action in actions:
            rd = self.result(state, action)
            vv = self.max_value_prune_et(rd, action, alpha, beta, d + 1, 'o' if cp == 'x' else 'x')

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

    def max_value_prune_et(self, state, l_action, alpha, beta, d, cp):
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
        cp: Current player for the context.

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
        actions = []

        # Legal actions for the current player
        for action in self.actions(state):
            if action[0] == cp:
                actions.append(action)

        for action in actions:
            rs = self.result(state, action)
            vv = self.min_value_prune_et(rs, action, alpha, beta, d + 1, 'o' if cp == 'x' else 'x')

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
        Simulates a three-men's-morris gameplay
        """
        state = copy.deepcopy(self.initial_state)
        # calculating the best move value and action for the given state
        best_action = self.minimax_decision(state)

        # To handle the case where there are no possible moves from the initial state
        if best_action[1] not in [(9, 9, 9), (6, 6), (5, 5)]:
            # Making the best move corresponding to the initial state
            state = copy.deepcopy(self.initial_state)
            expected_state = self.result(state, best_action[1])

            # Printing the board state resulting from the best move.
            print '{}'.format(self.convert_matrix_rastor(expected_state))


if __name__ == '__main__':
    # Capturing all the command line arguments
    state = sys.argv[1]
    path = sys.argv[2]
    ply = sys.argv[3]
    turn = sys.argv[4]

    # Initialising the three_men_morris game class
    game = three_men_morris(state, path, ply, turn)

    # Play the game
    game.play()

    # Print all the nodes visited to the specified output file
    game.visited_nodes_to_file()


