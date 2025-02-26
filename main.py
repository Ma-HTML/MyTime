import time
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
import ctypes  # Utilisation de ctypes pour une notification basique

# Fonction pour afficher une notification Windows sans librairie externe
def show_notification_windows(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Notification", 0x40 | 0x1)

# Fonction pour démarrer la notification à une heure précise
def notification_heure_precise():
    try:
        # Récupérer l'heure de la zone de texte
        heure = entry_heure.get()
        notification_time = datetime.strptime(heure, "%H:%M")
        
        now = datetime.now()
        notification_time = notification_time.replace(year=now.year, month=now.month, day=now.day)
        
        # Si l'heure est déjà passée, la mettre pour demain
        if notification_time < now:
            notification_time += timedelta(days=1)

        # Calculer le temps restant
        delta_t = (notification_time - now).total_seconds()

        # Message avant l'attente
        minutes_remaining = delta_t // 60
        label_info.config(text=f"Notification dans {int(minutes_remaining)} minutes...", fg="green")

        # Attendre jusqu'à l'heure
        root.after(int(delta_t * 1000), show_notification_windows, "C'est l'heure de la notification !")

        # Réinitialiser les champs après clic
        entry_heure.delete(0, tk.END)
        button_heure.config(state=tk.DISABLED)
        button_minuteur.config(state=tk.DISABLED)

    except ValueError:
        show_notification_windows("Veuillez entrer une heure valide au format HH:MM.")

# Fonction pour démarrer le minuteur avec secondes
def notification_minuteur():
    try:
        # Récupérer le nombre de minutes et secondes
        minutes_seconds = entry_minuteur.get().split(':')
        
        if len(minutes_seconds) == 2:  # Si les secondes sont présentes
            minutes = int(minutes_seconds[0])
            seconds = int(minutes_seconds[1])
            total_seconds = (minutes * 60) + seconds
        elif len(minutes_seconds) == 1:  # Si seulement les minutes sont présentes
            minutes = int(minutes_seconds[0])
            total_seconds = minutes * 60
        else:
            raise ValueError

        label_info.config(text=f"Notification dans {total_seconds // 60} minutes et {total_seconds % 60} secondes...", fg="blue")

        # Réinitialiser les champs après clic
        entry_minuteur.delete(0, tk.END)
        button_heure.config(state=tk.DISABLED)
        button_minuteur.config(state=tk.DISABLED)

        # Attendre pendant le temps spécifié
        root.after(total_seconds * 1000, show_notification_windows, "Le temps est écoulé !")

    except ValueError:
        show_notification_windows("Veuillez entrer un temps valide au format MM:SS ou MM.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Gestion des Notifications")
root.geometry("400x300")
root.config(bg="#2b2b2b")  # Couleur de fond moderne

# Ajouter un titre
label_title = tk.Label(root, text="Gestion des Notifications", font=("Arial", 18, "bold"), fg="white", bg="#2b2b2b")
label_title.pack(pady=20)

# Ajouter une étiquette d'information
label_info = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#2b2b2b")
label_info.pack(pady=10)

# Partie pour l'heure précise
frame_heure = tk.Frame(root, bg="#2b2b2b")
label_heure = tk.Label(frame_heure, text="Entrez l'heure (HH:MM) :", font=("Arial", 12), fg="white", bg="#2b2b2b")
label_heure.pack(side="left", padx=10)
entry_heure = tk.Entry(frame_heure, font=("Arial", 12), width=10)
entry_heure.pack(side="left", padx=10)
button_heure = tk.Button(frame_heure, text="Notifier à cette heure", font=("Arial", 12), fg="white", bg="#007BFF", command=notification_heure_precise)
button_heure.pack(side="left", padx=10)
frame_heure.pack(pady=10)

# Partie pour le minuteur
frame_minuteur = tk.Frame(root, bg="#2b2b2b")
label_minuteur = tk.Label(frame_minuteur, text="Entrez le minuteur (MM:SS) :", font=("Arial", 12), fg="white", bg="#2b2b2b")
label_minuteur.pack(side="left", padx=10)
entry_minuteur = tk.Entry(frame_minuteur, font=("Arial", 12), width=10)
entry_minuteur.pack(side="left", padx=10)
button_minuteur = tk.Button(frame_minuteur, text="Démarrer le minuteur", font=("Arial", 12), fg="white", bg="#28a745", command=notification_minuteur)
button_minuteur.pack(side="left", padx=10)
frame_minuteur.pack(pady=10)

# Lancer la boucle principale de l'interface
root.mainloop()

