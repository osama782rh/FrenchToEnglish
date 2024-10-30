import tkinter as tk
from tkinter import messagebox
import winsound  # Utilisé pour jouer les sons système
from game import Game

class MasterLangUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.time_left = game.time_left
        self.is_paused = False  # Indicateur de pause
        self.setup_ui()
        self.get_next_word()

    def setup_ui(self):
        """Configure l'interface utilisateur Tkinter."""
        self.root.title("MasterLang - Jeu de Traduction Français-Anglais")
        self.root.geometry("500x450")
        self.root.configure(bg="#f0f0f0")
        self.root.bind('<Return>', lambda event: self.check_answer())

        # Widgets
        self.question_label = tk.Label(self.root, font=("Helvetica", 16, "bold"), fg="#333", bg="#f0f0f0")
        self.question_label.pack(pady=10)

        self.hint_label = tk.Label(self.root, font=("Helvetica", 14, "italic"), fg="#007acc", bg="#f0f0f0")
        self.hint_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, font=("Arial", 12), bg="#f0f0f0")
        self.timer_label.pack(pady=5)

        self.question_progress_label = tk.Label(self.root, font=("Arial", 12), bg="#f0f0f0")
        self.question_progress_label.pack(pady=5)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()

        self.submit_button = tk.Button(self.root, text="Valider", command=self.check_answer, font=("Arial", 14), bg="#cccccc", activebackground="#a0a0a0")
        self.submit_button.pack(pady=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause, font=("Arial", 12), bg="#cccccc", activebackground="#a0a0a0")
        self.pause_button.pack(pady=10)

        self.result_label = tk.Label(self.root, font=("Arial", 12), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(self.root, font=("Arial", 12), bg="#f0f0f0")
        self.score_label.pack(pady=10)

    def get_next_word(self):
        """Affiche le prochain mot avec son indice et réinitialise le timer."""
        if hasattr(self, 'timer_job'):
            self.root.after_cancel(self.timer_job)  # Annule le timer précédent
        word, hint = self.game.get_random_word()
        self.question_label.config(text=f"Mot : {word}")
        self.hint_label.config(text=f"Indice : {hint}")
        self.question_progress_label.config(text=f"Question {self.game.question_count + 1} / {self.game.total_questions}")
        self.time_left = 20  # Réinitialiser le temps à 20 secondes
        self.update_timer()  # Lancer le timer pour la nouvelle question

    def update_timer(self):
        """Met à jour le timer de la question actuelle."""
        if not self.is_paused:
            if self.time_left > 0:
                self.timer_label.config(text=f"Temps restant : {self.time_left} s")
                self.time_left -= 1
                self.timer_job = self.root.after(1000, self.update_timer)  # Appelle la fonction toutes les secondes
            else:
                self.check_answer()  # Temps écoulé, vérifie la réponse

    def toggle_pause(self):
        """Pause ou reprend le chronomètre."""
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.update_timer()  # Reprendre le timer
        else:
            self.is_paused = True
            self.pause_button.config(text="Reprendre")

    def play_correct_sound(self):
        """Joue un son pour une réponse correcte."""
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

    def play_wrong_sound(self):
        """Joue un son pour une réponse incorrecte."""
        winsound.MessageBeep(winsound.MB_ICONHAND)

    def check_answer(self):
        """Vérifie la réponse et met à jour l'interface."""
        # Annuler le timer actuel car la réponse est vérifiée
        if hasattr(self, 'timer_job'):
            self.root.after_cancel(self.timer_job)

        user_answer = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)
        correct, message = self.game.check_answer(user_answer)

        # Affiche le message approprié en fonction de la réponse
        if correct:
            self.result_label.config(text="Correct !", fg="green")
            self.play_correct_sound()
        else:
            self.result_label.config(text=f"Incorrect ! Réponse attendue : {self.game.current_translation}", fg="red")
            self.play_wrong_sound()

        # Mettre à jour le score et l'affichage
        self.score_label.config(text=self.game.update_score())
        if self.game.is_game_over():
            self.show_summary()
        else:
            self.get_next_word()

    def show_summary(self):
        """Affiche le récapitulatif des réponses dans un tableau avec des couleurs pour correct/incorrect."""
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Récapitulatif des Réponses")
        summary_window.geometry("500x600")

        # En-têtes de tableau
        header_frame = tk.Frame(summary_window)
        header_frame.grid(row=0, column=0, columnspan=3, pady=5)

        tk.Label(header_frame, text="Mot en Français", font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=10)
        tk.Label(header_frame, text="Réponse en Anglais", font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=10)
        tk.Label(header_frame, text="Correct ?", font=("Arial", 10, "bold"), width=10, anchor="w").grid(row=0, column=2,
                                                                                                        padx=10)

        # Création du tableau avec les résultats
        for idx, item in enumerate(self.game.history):
            color = "green" if item["correct"] else "red"
            answer_text = item["réponse_donnée"] if item[
                "correct"] else f"{item['réponse_donnée']} (Attendu: {item['réponse_correcte']})"

            # Créer une ligne pour chaque mot et réponse
            tk.Label(summary_window, text=item["mot"], font=("Arial", 10), width=20, anchor="w").grid(row=idx + 1,
                                                                                                      column=0, padx=10,
                                                                                                      pady=2)
            tk.Label(summary_window, text=answer_text, font=("Arial", 10), fg=color, width=20, anchor="w").grid(
                row=idx + 1, column=1, padx=10, pady=2)
            tk.Label(summary_window, text="Oui" if item["correct"] else "Non", font=("Arial", 10), fg=color, width=10,
                     anchor="w").grid(row=idx + 1, column=2, padx=10, pady=2)

        # Bouton Recommencer
        restart_button = tk.Button(summary_window, text="Recommencer", command=self.restart_game, font=("Arial", 12),
                                   bg="#cccccc", activebackground="#a0a0a0")
        restart_button.grid(row=len(self.game.history) + 1, column=0, columnspan=3, pady=20)

    def restart_game(self):
        """Réinitialise le jeu et recommence."""
        self.game.reset_game()
        self.score_label.config(text=self.game.update_score())
        self.result_label.config(text="")
        self.get_next_word()

    def end_game(self):
        """Affiche un message de fin du jeu et ferme l'application."""
        messagebox.showinfo("Fin du jeu", f"Partie terminée!\nScore final : {self.game.score_correct} / {self.game.total_questions}\nErreurs : {self.game.score_incorrect}")
        self.root.destroy()
        self.game.close()
