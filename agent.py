import random
import pickle
import os
import numpy as np
from config import WIDTH, HEIGHT, BLOCK_SIZE   # utilisation des constantes depuis config.py

class RLAgent:
    def __init__(self, action_size=4, epsilon=0.1):
        self.action_size = action_size
        self.q_table = {}
        self.alpha = 0.1    #taux d'apprentissage Nouvelle estimation=10+0.5×(15−10)=12.5 exemple avec taux d'apprentissage 0.5 apprend vite mais oublie vite
        self.gamma = 0.95  # pour un focus long terme 0.05 pour un focus court terme
        self.epsilon = epsilon # taux d'exploration c'est a dire la probabilité de choisir une action aléatoire est de 10%
        self.epsilon_min = 0.01 # action aléatoire minimale de 1%
        self.epsilon_decay = 0.995   # taux de décrémentation de l'epsilon
        self.load()

    # Cette fonction c'est pour choisir si le serpent va faire une action aléatoire (exploration) ou une action optimale
    def choose_action(self, state):
        if random.random() < self.epsilon: # 10% de chance de choisir une action aléatoire
            return random.randint(0, self.action_size - 1)
        else:
            state_key = self._state_to_key(state)
            q_values = [self.q_table.get((state_key, a), 0) for a in range(self.action_size)]
            return int(np.argmax(q_values))
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def _state_to_key(self, state):
        if state is None:
            return None
        head_x, head_y = state['head'] # recuperation de la position de la tête du serpent
        # Calcul de la direction relative de la nourriture ou ce trouve la bouffe quoi vers ou aller pour la manger
        food_dx = 1 if state['food'][0] > head_x else -1 if state['food'][0] < head_x else 0
        food_dy = 1 if state['food'][1] > head_y else -1 if state['food'][1] < head_y else 0
        # Calcul d'un drapeau danger sur les 4 directions
        dangers = []
        directions = [(0, -BLOCK_SIZE), (BLOCK_SIZE, 0), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0)]
        for d in directions:
            new_head = (head_x + d[0], head_y + d[1])
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in state['body']:
                dangers.append(1)
            else:
                dangers.append(0)
        # Clé d'état compacte incluant la direction actuelle du snake
        # Découverte de l'opérateur * pour déballer une liste exemple : *dangers = 0, 0, 0, 0
        return (food_dx, food_dy, *dangers, state['direction'][0], state['direction'][1])
    
    def learn(self, state, action, reward, next_state, done):
        state_key = self._state_to_key(state)
        next_key = self._state_to_key(next_state) if not done else None
        
        current_q = self.q_table.get((state_key, action), 0)
        max_next_q = max([self.q_table.get((next_key, a), 0) for a in range(self.action_size)]) if next_key else 0
        
        # Le coeur du truc c'est ici
        target = reward + self.gamma * max_next_q * (not done)
        new_q = current_q + self.alpha * (target - current_q)
        
        self.q_table[(state_key, action)] = new_q
        self.decay_epsilon()
    
    def save(self, filename="qtable.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
        print("Q-table saved.")

    def load(self, filename="qtable.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
            print("Q-table loaded.")
        else:
            self.q_table = {}
