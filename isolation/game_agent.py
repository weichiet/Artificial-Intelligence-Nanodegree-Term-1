"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

#%%
def custom_score(game, player):        
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    The first heuristic calculates the square of the difference of 
    the number of the player's legal moves and 2 times the number 
    of opponent's legal moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2 * opp_moves)**2
    

#%%
def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    The second heuristic first calculates two scores equal to square of the 
    distance from the center of the board to the position of the active player
    and the opponent player respectively. 
    It then returns the difference of these two scores.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y1, x1 = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))    
    player_1_score = float((h - y1)**2 + (w - x1)**2)
    player_2_score = float((h - y2)**2 + (w - x2)**2) 
        
    return float(player_1_score - player_2_score)

#%%
def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    The third heuristic combines the above two heuristic functions.
    It calculates the sum of the scores in heuristic one and heuristic two.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")   
        
    w, h = game.width / 2., game.height / 2.
    y1, x1 = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))    
    player_1_score = float((h - y1)**2 + (w - x1)**2)
    player_2_score = float((h - y2)**2 + (w - x2)**2) 
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
   
    return float(10 * (own_moves - 2 * opp_moves) + (player_1_score - player_2_score))


#%%
class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=30.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

#%%
class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
       
        def terminal_test(game):
            """A state is terminal if it is won or
            there are no more legal moves
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            return game.is_winner(game.active_player) or \
                    not game.get_legal_moves()
        
        def min_value(game, depth):
            """ Return the value for a win if the game is over or reach the
            search depth, otherwise return the minimum value over all 
            legal child nodes.
            """            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
    
            if terminal_test(game) or depth == 1:
                return self.score(game, self)
    
            score = float("inf")
            for move in game.get_legal_moves():
               score = min(score, max_value(game.forecast_move(move),\
                                            depth - 1))
            return score

        def max_value(game, depth):
            """ Return the value for a loss if the game is over or reach the
            search depth, otherwise return the maximum value over all 
            legal child nodes.
            """                  
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
    
            if terminal_test(game) or depth == 1:
                return self.score(game, self)
    
            score = float("-inf")
            for move in game.get_legal_moves():
                score = max(score, min_value(game.forecast_move(move),\
                                             depth - 1))
            return score  
        
        # Body of minimax
        # Return the move along a branch of the game tree that
        # has the best possible value
        
        best_score = float("-inf")
        best_move = (-1, -1)
        
        for move in game.get_legal_moves():
            score = min_value(game.forecast_move(move), depth)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move             
        

#%%
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            
            # Iterative deepening search implementation
            while True:
                move = self.alphabeta(game, depth)
                best_move = move
                depth += 1
                
        except SearchTimeout:
            pass # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration		
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def terminal_test(game):
            """A state is terminal if it is won or
            there are no more legal moves
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            return game.is_winner(game.active_player) or \
                    not game.get_legal_moves()
        
        def min_value(game, depth, alpha, beta):
            """ Return the value for a win if the game is over or reach the
            search depth, otherwise return the minimum value over all 
            legal child nodes.
            """            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
    
            if terminal_test(game) or depth == 1:
                return self.score(game, self)
    
            score = float("inf")
            for move in game.get_legal_moves():
               score = min(score, max_value(game.forecast_move(move),\
                                            depth - 1, alpha, beta))
               if score <= alpha:
                   return score
               
               beta = min(beta, score)
               
            return score


        def max_value(game, depth, alpha, beta):
            """ Return the value for a loss if the game is over or reach the
            search depth, otherwise return the maximum value over all 
            legal child nodes.
            """                  
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
    
            if terminal_test(game) or depth == 1:
                return self.score(game, self)
    
            score = float("-inf")
            for move in game.get_legal_moves():
                score = max(score, min_value(game.forecast_move(move),\
                                             depth - 1, alpha, beta))
                if score >= beta:
                    return score
                
                alpha = max(alpha, score)
                
            return score

        # Body of Alphabeta
        best_score = float("-inf")
        beta = float("inf")
        best_move = None
        
        for move in game.get_legal_moves():
            score = min_value(game.forecast_move(move), depth,\
                              best_score, beta)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move     

