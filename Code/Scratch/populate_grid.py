import tkinter as tk

class GlycoAssessorApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.first_shape_added = False
        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        self.add_shape(event.x, event.y)

    def add_shape(self, x, y):
        # Draw the main shape (e.g., a monosaccharide node)
        r = 20  # radius of shape
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='blue', outline='black')

        # If this is the first shape, add a grid of white circles
        if not self.first_shape_added:
            self.add_white_circle_grid(x, y)
            self.first_shape_added = True

    def add_white_circle_grid(self, x_center, y_center, grid_size=5, spacing=40):
        r = 4  # radius of each small white circle

        half = grid_size // 2  # how far to go in each direction

        for i in range(-half, half + 1):
            for j in range(-half, half + 1):
                cx = x_center + i * spacing
                cy = y_center + j * spacing

                # Skip drawing a circle directly on top of the center shape
                if i == 0 and j == 0:
                    continue

                self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='white', outline='black')

# Run the app
root = tk.Tk()
app = GlycoAssessorApp(root)
root.mainloop()
