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
        print(self.Q)

    def update_q_table(self, next_state: State, reward: float, state: State, action: str):
        index_action = self.actions_index[action]
        maximo_q_next_state = max(self.Q[next_state])
        self.Q[state][index_action] = self.equation_q_learning(self.Q[state][index_action], maximo_q_next_state, reward)

    def best_action(self, state: State):
        index = self.Q[state].index(max(self.Q[state]))
        list_action = self.actions_index.items()
        resultado = filter(list_action, lambda x: x[1] == index)
        resultado = tuple(resultado)
        return self.actions_index[resultado[0]]
        

    def random_action(self, state: State):
        rand = random.randrange(0, 1)
        list_action = self.actions_index.items()
        resultado = filter(list_action, lambda x: x[1] == rand)
        resultado = tuple(resultado)
        return self.actions_index[resultado[0]]

    def choose_action(self):
        if random.random() < self.epsilon:
            self.random_action()
        else:
            self.best_action()


    def equation_q_learning(self, current_q_value, next_q_value, reward):
        return current_q_value + self.ALPHA * (reward + self.GAMMA *next_q_value - current_q_value)
        

        