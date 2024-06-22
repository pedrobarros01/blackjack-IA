import random 
from utils import calculate_hand_value
from Qlearning import QLearningModel, Transiction, State
 ######################################
 #
 # Seu agente deve ser colocado nessa região
 # Lembre-se que a regra do blackjack foi modificada
 # nesse versão o dealer joga primeiro que você
 # e você joga vendo a primeira carta dele
 #
 #
class Player:
  def __init__(self, model: QLearningModel) -> None:
    self.qlearning = model
    self.current_state = None
    self.action = None
  # Essa função toma a decisão após observar
  # o estado observável do campo
  def decision(self, your_hand, dealer_first_card):
    print("======== Start of turn =======")
    print(f"Player hand: {your_hand} vs dealer {dealer_first_card}, ...", )
    dealer_first_card_aux = dealer_first_card.value
    player_hand = [d for d in your_hand]
    is_As = 'H'
    for hand in player_hand:
      if hand.value == 'ace':
        is_As = 'S'
        break
    self.current_state = State(calculate_hand_value(your_hand), is_As, dealer_first_card_aux)
    choice = self.qlearning.choose_action(self.current_state)
    self.action = choice
    if  calculate_hand_value(your_hand) >= 19:
      print(f"You made the decision 'stop'")
      self.action = ("stop", 1)
      return "stop"
    
    print(f"You made the decision '{choice}'")
    return choice[0]

  # Essa função deveria utilizar o resultado para 
  # atualizar a QTable
  def result(self, your_hand, dealer_first_card, decision, reward, is_not_done):
    dealer_first_card_aux = dealer_first_card.value
    player_hand = [d for d in your_hand]
    is_As = 'H'
    for hand in player_hand:
      if hand.value == 'ace':
        is_As = 'S'
        break
    transiction = Transiction(State(calculate_hand_value(your_hand), is_As, dealer_first_card_aux), reward)
    if self.current_state == None:
      self.current_state = transiction.next_state
      self.action = ("hit", 0) 
    if calculate_hand_value(your_hand) < 22:
      self.qlearning.update_q_table(transiction.next_state, transiction.reward, self.current_state, decision)
    game_status = "still going" if is_not_done else "is done" 
    print(f"Your hand ({calculate_hand_value(your_hand)}) after decision '{decision}' with {reward=} and game {game_status}")
    if not is_not_done:
      print("======== End of turn =======")
