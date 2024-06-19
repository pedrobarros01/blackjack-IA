from collections import defaultdict
import random
class State:
    def __init__(self, sum: int, is_As: str, dealer: str) -> None:
        self.sum = sum
        self.is_As = is_As
        self.dealer = dealer

    def __str__(self) -> str:
        return f'{self.sum}-{self.is_As}-{self.dealer}'

class Transiction:
    def __init__(self, next_state: State, reward: float) -> None:
        self.next_state = next_state
        self.reward = reward

class QLearningModel:
    ALPHA = 0
    GAMMA = 0
    EPSILON = 0.5
    def __init__(self, states: list[str], action: list[str] = ['cavar', 'passar']) -> None:
        #cavar = 0 e passar = 1
        self.Q = defaultdict(list)
        self.actions_index = {
            action[0]:0,
            action[1]:1
        }
        self.epsilon = self.EPSILON
        
        for state in states:
            self.Q[state] = [0, 0]
    
    def print(self):
        pass

    def update_q_table(self, next_state: State, reward: float):
        pass

    def best_action(self):
        pass

    def random_action(self):
        pass

    def choose_action(self):
        pass


    def equation_q_learning(self, current_q_value, next_q_value, reward):
        return current_q_value + self.ALPHA * (reward + self.GAMMA *next_q_value - current_q_value)
        

        