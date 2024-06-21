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
    ALPHA = 0.1
    GAMMA = 0.9
    EPSILON = 0.1
    def __init__(self,  dealer_hand ,action: list[str] = ["hit", "stop"]) -> None:
        #cavar = 0 e passar = 1
        self.states = []
        for u in range(2, 22):
            for d in dealer_hand:
                state_sem_as = State(u, 'H', d)
                state_com_as = State(u, 'S', d)
                self.states.extend([state_sem_as, state_com_as])
        self.Q = defaultdict(list)
        self.actions_index = {
            action[0]:0,
            action[1]:1
        }
        self.epsilon = self.EPSILON
        
        for state in self.states:
            self.Q[state.__str__()] = [0.5, 0.5]
    
    def print(self):
        print(self.Q)

    def update_q_table(self, next_state: State, reward: float, state: State, action: str):
        print(action)
        print(self.actions_index)
        print(f'proximo estado: {next_state}')
        print(f'estado atual: {state}')
        index_action = self.actions_index[action[0]]
        maximo_q_next_state = max(self.Q[next_state.__str__()])
        self.Q[state.__str__()][index_action] = self.equation_q_learning(self.Q[state.__str__()][index_action], maximo_q_next_state, reward)

    def best_action(self, state: State):
        print(state.__str__())
        print(self.Q[state.__str__()])
        index = self.Q[state.__str__()].index(max(self.Q[state.__str__()]))
        list_action = self.actions_index.items()
        print(list_action)
        resultado = filter(lambda x: x[1] == index, list_action)
        resultado = tuple(resultado)
        return resultado[0]
        

    def random_action(self, state: State):
        rand = random.randrange(0, 1)
        list_action = self.actions_index.items()
        resultado = filter( lambda x: x[1] == rand, list_action)
        resultado = tuple(resultado)
        return resultado[0]

    def choose_action(self, state: State):
        escolha = None
        if random.random() < self.epsilon:
            escolha = self.random_action(state)
        else:
            escolha = self.best_action(state)
        
        return escolha


    def equation_q_learning(self, current_q_value, next_q_value, reward):
        return current_q_value + self.ALPHA * (reward + self.GAMMA * next_q_value - current_q_value)
        

        