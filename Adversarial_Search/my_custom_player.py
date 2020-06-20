from sample_players import DataPlayer

class CustomPlayer(DataPlayer):
    """ Implement customized agent to play knight's Isolation """

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least
        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.
        See RandomPlayer and GreedyPlayer in sample_players for more examples.
        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        import random
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.alpha_beta_search(state, depth=3))
    
    def alpha_beta_search(self, state, depth):

        def min_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth-1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth-1))
                if value >= beta:
                    alpha = max(alpha, value)
            return value

        result = (None, float("-inf"), float("-inf"))
        for action in state.actions():
            (best_move, best_score, alpha) = result
            value = min_value(state.result(action), alpha, float("-inf"), depth-1)
            alpha = max(alpha, value)
            if value >= best_score: 
                result = (action, value, alpha)
            else: 
                result = (best_move, best_score, alpha)
        return result[0]
    
    def score(self, state):
        my_loc = state.locs[self.player_id]
        my_liberties = state.liberties(my_loc)
        his_loc = state.locs[(self.player_id+1)%2]
        his_liberties = state.liberties(his_loc)
        rem_my_liberties = 0
        for my_liberty in my_liberties:
            rem_my_liberties += len(state.liberties(my_liberty))
        rem_his_liberties = 0
        for his_liberty in his_liberties:
            rem_his_liberties += len(state.liberties(his_liberty))
        # Heuristic 1 studied is : Maximizing the survival of the agent while decreasing the survival chances of the opponent
        return len(my_liberties)-2*len(his_liberties)+rem_my_liberties-2*rem_his_liberties
        # Heuristic 2 studied is : Maximizing the survival of the agent
#         return len(my_liberties)+rem_my_liberties
        # No heuristic studied is : 
#         return len(my_liberties)-len(his_liberties)
       
    
     


