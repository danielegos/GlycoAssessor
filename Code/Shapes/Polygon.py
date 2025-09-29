import math

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
        print(x, y, sugar_code)
        self.circles[circle] = (x, y, sugar_code)
        self.undo_stack.append(circle)

    elif shape == 'triangle':
        triangle = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        print(x, y, sugar_code)
        self.circles[triangle] = (x, y, sugar_code)
        self.undo_stack.append(triangle)

    elif shape == 'diamond':
        diamond = self.canvas.create_polygon(
            x, y - 2 * radius, x + 2 * radius, y, x, y + 2 * radius, x - 2 * radius, y,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        print(x, y, sugar_code)
        self.circles[diamond] = (x, y, sugar_code)
        self.undo_stack.append(diamond)

    elif shape == 'square':
        square = self.canvas.create_rectangle(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        print(x, y, sugar_code)
        self.circles[square] = (x, y, sugar_code)
        self.undo_stack.append(square)

    # Add crossed square
    elif shape == 'crossed square':
        half = 2 * radius

        crossed_square = self.canvas.create_rectangle(
            x - half, y - half, x + half, y + half,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        cross = self.canvas.create_line(x - half, y - half, x + half, y + half, fill="black", width=5, tags=sugar_code)
        crossed = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x - 2 * radius, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill='white', outline="black", width=5, tags=sugar_code  # , width=10
        )
        print(x, y, sugar_code)
        self.circles[crossed_square] = (x, y, sugar_code)
        self.undo_stack.append(crossed_square)
        self.undo_stack.append(cross)
        self.undo_stack.append(crossed)

    # Add divided diamond
    elif shape == 'divided diamond':
        points = [x, y - 2 * radius, x + 2 * radius, y, x, y + 2 * radius, x - 2 * radius, y]
        div_diamond = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.canvas.create_line(x - 2 * radius, y, x + 2 * radius, y, fill="black", width=5, tags=sugar_code)

        # if AltA or IdoA, place white triangle on top
        div_2 = None
        if sugar_code == 'AltA' or sugar_code == 'IdoA':
            div2 = self.canvas.create_polygon(
                x - 2 * radius, y, x, y - 2 * radius, x + 2 * radius, y,
                fill='white', outline="black", width=5, tags=sugar_code  # , width=10
            )
        # else, place it on bottom
        else:
            div2 = self.canvas.create_polygon(
                x - 2 * radius, y, x, y + 2 * radius, x + 2 * radius, y,
                fill='white', outline="black", width=5, tags=sugar_code  # , width=10
            )
        print(x, y, sugar_code)
        self.circles[div_diamond] = (x, y, sugar_code)
        self.undo_stack.append(div_diamond)
        self.undo_stack.append(div2)

    # Add divided triangle
    elif shape == 'divided triangle':
        triangle = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code  # , width=10
        )
        tri2 = self.canvas.create_polygon(
            x, y + 2 * radius, x, y - 2 * radius, x - 2 * radius, y + 2 * radius,
            fill='white', outline="black", width=5, tags=sugar_code  # , width=10
        )
        print(x, y, sugar_code)
        self.circles[triangle] = (x, y, sugar_code)

        self.undo_stack.append(triangle)
        self.undo_stack.append(tri2)

    # Add rectangle
    elif shape == 'rectangle':
        rectangle = self.canvas.create_rectangle(x - 2 * radius, y - 1.2 * radius, x + 2 * radius, y + 1.2 * radius,
                                fill=color, outline="black", width=5, tags=sugar_code )
        print(x, y, sugar_code)
        self.circles[rectangle] = (x, y, sugar_code)
        self.undo_stack.append(rectangle)

    # Add star
    elif shape == 'star':
        points = []
        for i in range(10):
            angle = math.pi / 5 * i
            r = 2 * radius if i % 2 == 0 else radius
            px = x + r * math.sin(angle)
            py = y - r * math.cos(angle)
            points.extend([px, py])

        star = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        print(x, y, sugar_code)
        self.circles[star] = (x, y, sugar_code)
        self.undo_stack.append(star)

    # Add flat diamond
    elif shape == 'flat diamond':
        points = [x, y - 1.3 * radius, x + 2 * radius, y, x, y + 1.3 * radius, x - 2 * radius, y]

        flat_diamond = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)

        print(x, y, sugar_code)
        self.circles[flat_diamond] = (x, y, sugar_code)
        self.undo_stack.append(flat_diamond)

    # Add hexagon
    elif shape == 'hexagon':
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            px = x + 2 * radius * math.cos(angle)
            py = y + 1.5 * radius * math.sin(angle)
            points.extend([px, py])

        hexagon = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)

        print(x, y, sugar_code)
        self.circles[hexagon] = (x, y, sugar_code)
        self.undo_stack.append(hexagon)

    # Add pentagon
    elif shape == 'pentagon':
        points = []
        for i in range(5):
            angle = math.radians(72 * i - 90)
            px = x + 2 * radius * math.cos(angle)
            py = y + 2 * radius * math.sin(angle)
            points.extend([px, py])

        pentagon = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        print(x, y, sugar_code)
        self.circles[pentagon] = (x, y, sugar_code)
        self.undo_stack.append(pentagon)

