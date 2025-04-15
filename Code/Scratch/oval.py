import tkinter as tk

window = tk.Tk()
canvas = tk.Canvas(window, width=400, height=300)
canvas.pack()

# Create multiple ovals with different properties
oval1 = canvas.create_oval(20, 20, 180, 100, fill="lightblue", outline="blue", width=3)
oval2 = canvas.create_oval(220, 50, 380, 200, fill="lightgreen", outline="green", width=2, state="normal",
                           tags="oval_group")
oval3 = canvas.create_oval(100, 150, 300, 280, fill="yellow", outline="orange", width=4, state="normal",
                           tags=("oval_group", "removable"))

window.mainloop()