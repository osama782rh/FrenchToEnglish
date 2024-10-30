class Game:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.score_correct = 0
        self.score_incorrect = 0
        self.total_questions = 30  # Augmentation à 30 questions
        self.question_count = 0
        self.current_word = None
        self.current_translation = None
        self.time_left = 20  # Temps en secondes pour chaque question
        self.history = []  # Historique des réponses

    def get_random_word(self):
        """Récupère un mot français aléatoire et initialise l'indice pour l'utilisateur."""
        self.cursor.execute("SELECT mot_francais, traduction_anglaise FROM vocabulaire_toeic ORDER BY RAND() LIMIT 1")
        self.current_word, self.current_translation = self.cursor.fetchone()
        self.time_left = 20  # Réinitialiser le timer pour chaque question
        return self.current_word, self.generate_hint(self.current_translation)

    def generate_hint(self, word):
        """Génère un indice avec la première lettre et des tirets pour les lettres restantes."""
        hint = word[0].upper() + ' '.join('_' if char.isalpha() else ' ' for char in word[1:])
        return hint

    def check_answer(self, user_answer):
        """Vérifie la réponse de l'utilisateur et enregistre dans l'historique."""
        is_correct = user_answer.strip().lower() == self.current_translation.lower()

        if is_correct:
            self.score_correct += 1
        else:
            self.score_incorrect += 1

        self.history.append({
            "mot": self.current_word,
            "réponse_donnée": user_answer,
            "réponse_correcte": self.current_translation,
            "correct": is_correct
        })

        self.question_count += 1
        return is_correct, "Correct!" if is_correct else f"Incorrect! Réponse attendue : {self.current_translation}"

    def update_score(self):
        """Retourne le score actuel sous forme de texte."""
        return f"Score : {self.score_correct} / {self.total_questions} | Erreurs : {self.score_incorrect}"

    def is_game_over(self):
        """Vérifie si le jeu est terminé."""
        return self.question_count >= self.total_questions

    def reset_game(self):
        """Réinitialise le jeu pour recommencer."""
        self.score_correct = 0
        self.score_incorrect = 0
        self.question_count = 0
        self.history.clear()

    def close(self):
        """Ferme la connexion à la base de données."""
        self.cursor.close()
        self.conn.close()
