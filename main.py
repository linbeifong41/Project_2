import tkinter as tk 
from datetime import date 

def log_mood(level):
    today = date.today().isoformat()
    with open("mood_log.txt", "a") as file:
        file.write(f"{today}: Mood {level}/5\n")
    print(f"Mood {level} logged for {today}!")

root = tk.Tk()
root.title("Mind Garden")
root.geometry("400x300")
root.configure(bg="#E6F5EB")

label = tk.Label(root, text="How are you feeling today?", bg="#E6F5EB", font=("Arial", 14))
label.pack(pady=20)

for i in range(1, 6):
    btn = tk.Button(root, text=f"{i}", width=10, font=("Arial", 12), command=lambda i=i: log_mood(i))
    btn.pack(pady=5)

root.mainloop()


