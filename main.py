from db import connect_to_db
from game import Game
from ui import MasterLangUI
import tkinter as tk

# Connexion à la base de données
db_connection = connect_to_db()

# Création de la logique de jeu
game = Game(db_connection)

# Lancement de l'interface
root = tk.Tk()
app = MasterLangUI(root, game)
root.mainloop()
