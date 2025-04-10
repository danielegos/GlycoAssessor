def add_polygon_shape(self, x, y, shape, color, sugar_code):
    """Add a vertex and draw a green node."""
    radius = self.grid_size / 2
    self.vertices.append((x, y))

    if shape == 'circle':
        # Draw green circle with radius = 2 * vertex radius
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        self.circles[circle] = (x, y, sugar_code)

    elif shape == 'triangle':
        triangle = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        self.circles[triangle] = (x, y, sugar_code)

    elif shape == 'diamond':
        circle = self.canvas.create_polygon(
            x, y - 2 * radius, x + 2 * radius, y, x, y + 2 * radius, x - 2 * radius, y,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        self.circles[circle] = (x, y, sugar_code)

    elif shape == 'square':
        square = self.canvas.create_rectangle(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        self.circles[square] = (x, y, sugar_code)
