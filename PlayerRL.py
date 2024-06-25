import random
from collections import defaultdict
import numpy as np
from utils import calculate_hand_value

class RLAgent:
  def __init__(self):
  
    # Learning rate - 
    self.alpha = 0.1
    # Discount factor - Balanço entre priorizar recompensas futuras e atuais
    self.gamma = 0.9
    # Exploration rate - epsilon greedy
    self.epsilon = 0.1
    # Lembrando a ultima acao
    self.last_opponent_action = None
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False  
    self.player_wins = 0
    # Q table
    self.Q = defaultdict(lambda: [0.0, 0.0])
    self.action_list = ["hit", "stop"]
    self.next_action = "hit"
    self.current_input = None
    self.current_output = None    
    
  def extract_rl_state(self, your_hand, dealer_first_card):
    # versão bem básica onde apenas verificamos se o total
    # em nossa mão é maior que 11, assim podemos
    # ter uma característica para indicar se tem
    # uma chance de 'estourar' a mão mas isso 
    # não leva em conta várias pontos importantes
    sum_hand = calculate_hand_value(your_hand)
    dealer = calculate_hand_value([dealer_first_card])
    tem_ace = any([hand.value == "ace" for hand in your_hand])
    return (sum_hand, tem_ace, dealer);
 
  def choose_action(self, state):
    #
    # Pode ser melhorado!
    #
    if np.random.uniform(0, 1) < self.epsilon:
      # Explore: Choose a random action
      action = np.random.choice(self.action_list)
    else:
      # Exploit: Choose the action with the maximum Q-value
      action = self.action_list[np.argmax(self.Q[state])]
    return action
    
    
  def update_qtable(self, state, action, reward, next_state, next_action, alg):
    alp = self.alpha
    gam = self.gamma
    action_index = self.action_list.index(action)
    next_action_index = self.action_list.index(next_action)
    soma_mao = state[0]
    tem_ace = state[1]
    dealer_value = state[2]
    '''
    Politica 1:
          (action == "stop" and soma_mao < 19)
      or
      (action == "hit" and soma_mao >= 19)
    '''
    #Politica 2
    if(
      (action == "stop" and (soma_mao > 17 and not tem_ace))
      or
      (action == "stop" and (not tem_ace and soma_mao < 17 and soma_mao > 12 and dealer_value < 7))
      or
      (action == "hit" and (not tem_ace and soma_mao < 17 and soma_mao > 12 and dealer_value > 7))
      or
      (action == "hit" and (not tem_ace and soma_mao < 12))
      or
      (action == "stop" and (tem_ace and soma_mao > 17))
      or
      (action == "stop" and (tem_ace and soma_mao < 18 and soma_mao >= 16 and dealer_value > 7))
      or
      (action == "hit" and (tem_ace and soma_mao < 18 and soma_mao >= 16 and dealer_value < 7))
      or
      (action == "hit" and (tem_ace and soma_mao < 12))
      ):
      reward += 1
    else:
      reward -= 1
    if alg == 'Q':
      self.Q[state][action_index] = (1 - alp) * self.Q[state][action_index] + alp * (reward + gam * np.max(self.Q[next_state])) 
    else:
      self.Q[state][action_index] = self.Q[state][action_index] + alp + ((reward + gam * self.Q[next_action][next_action_index]) - self.Q[state][action_index])
    
  # Essa função toma a decisão após observar
  # o estado observável do campo
  def decision(self, your_hand, dealer_first_card):
    player_hand = [d for d in your_hand]
    print("======== Start of turn =======")
    print(f"Player hand: {player_hand} vs dealer {dealer_first_card}, ...", ) 
    state = self.extract_rl_state(your_hand=your_hand, dealer_first_card=dealer_first_card)
    choice = self.choose_action(state)
    print(f"You made the decision '{choice}'")
    return choice

  # Essa função deveria atualiza QTable
  def result(self, your_hand, dealer_first_card, decision, reward, is_not_done):
    player_hand = [d for d in your_hand]
    game_status = "still going" if is_not_done else "is done" 
    print(f"{your_hand=}")
    state = self.extract_rl_state(your_hand=your_hand[:-1], dealer_first_card=dealer_first_card)
    next_state = self.extract_rl_state(your_hand=your_hand, dealer_first_card=dealer_first_card)
    self.next_action = self.choose_action(next_state)
    self.update_qtable(state, decision, reward, next_state, self.next_action, 'S')
    self.print_q_table(self.Q)
    print(f"Your hand ({calculate_hand_value(your_hand)}) after decision '{decision}' with {reward=} and game {game_status}")

    print("======== End of turn =======")    
  
  def print_q_table(self, Q):
    for k,v in Q.items():
      print(f"For state={k}")
      for idx, a in enumerate(self.action_list):
        print(f"  Q for {a}", Q[k][idx])
    
  # Nome de seu agente deve ser colocado aqui  
  def get_name(self):
    return "Drungas"


