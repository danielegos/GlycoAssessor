def add_edge(self, x, y, func):
# Handle adding edges (black) between two vertices
    grid_x = round(x / self.grid_size) * self.grid_size
    grid_y = round(y / self.grid_size) * self.grid_size

    if not self.first_vertex:
        # First click to select the first vertex for the edge
        if (grid_x, grid_y) in self.vertices:
            self.first_vertex = (grid_x, grid_y)
        else:
            print("First point must be an existing vertex!")
    else:
        # Second click to select the second vertex and add an edge
        if (grid_x, grid_y) in self.vertices and (grid_x, grid_y) != self.first_vertex:
            func(self.first_vertex, (grid_x, grid_y))
            self.first_vertex = None  # Reset for the next edge creation
        else:
            print("Second point must be an existing vertex and different from the first one!")