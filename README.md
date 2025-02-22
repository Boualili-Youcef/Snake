# Snake

## Project Overview
Ce projet implémente un jeu de Snake en Python en utilisant des concepts de Machine Learning pour optimiser la stratégie du serpent. Le code est structuré pour être facilement extensible et maintenable.

## Aperçu du Projet
Voici un aperçu de ce à quoi ressemble le jeu :
![Image](https://github.com/user-attachments/assets/0b745bc8-302c-47cd-b3ae-4fa3609208f6)
## Installation et Exécution
Suivez les étapes ci-dessous pour configurer et exécuter le projet :

1. Créez un environnement virtuel :
   ```
   python3 -m venv venv
   ```
2. Activez l'environnement virtuel :
   ```
   source venv/bin/activate
   ```
3. Lancez le jeu avec différents modes :
   ```
   python3 snake_game.py [mode]
   ```
   où [mode] peut être "training", "ai", "ai_vs_ai", "human" ou "human_vs_ai".

## Architecture et Design
Ce projet a été conçu en appliquant des techniques avancées de Machine Learning.  
- Utilisation de Q-learning pour entraîner l'agent à partir d'états définis et une récompense adaptative.  
- Hyperparamètres (alpha=0.1, gamma=0.95, epsilon décroissant) soigneusement calibrés pour équilibrer exploration et exploitation.  
- Modularisation du code assurant facilité de maintenabilité et évolutivité avec des composants réutilisables et testables.

## Q-learning et Q-table
Le système d'apprentissage est basé sur une méthode de Q-learning. Chaque état du jeu est représenté par une clé compacte qui inclut la direction de la nourriture, la présence de dangers aux alentours et la direction actuelle du serpent. La Q-table est un dictionnaire qui associe à chaque combinaison (état, action) une valeur représentant l'estimation de la récompense cumulée future.

La mise à jour de la Q-table se fait selon la formule suivante :

$$
Q(s, a) = Q(s, a) + \alpha \times \Bigl( R + \gamma \times \max_{a'} Q(s', a') - Q(s, a) \Bigr)
$$

où :
- Q(s, a) : valeur actuelle pour l'état s et l'action a.
- \(\alpha\) (alpha) : taux d'apprentissage, contrôle la vitesse d'adaptation (valeur utilisée : 0.1).
- R : récompense immédiate.
- \(\gamma\) (gamma) : facteur de discount, qui mesure l'importance des récompenses futures (valeur utilisée : 0.95).
- s' : nouvel état après avoir exécuté l'action a.

Cette approche professionnelle permet d'équilibrer exploration et exploitation grâce à un taux d'exploration (epsilon) qui décroît progressivement après chaque itération.
