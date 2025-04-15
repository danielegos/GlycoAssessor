# Place vertex in Circle mode
import math

def add_vertex(self, x, y, func):
    # Define the fixed position for the first vertex
    fixed_x = 80
    fixed_y = 240

    grid_x = round(x / self.grid_size) * self.grid_size
    grid_y = round(y / self.grid_size) * self.grid_size

    if not self.first_circle_placed:
        func(fixed_x, fixed_y)
        self.first_circle_placed = True
    else:
        # Check if the distance condition (8 times the radius) and perpendicular/parallel condition hold
        radius = self.grid_size / 2
        for center in self.vertices:
            dx = grid_x - center[0]
            dy = grid_y - center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            required_distance = 8 * radius  # Distance should be eight times the radius

            # If the distance is correct, check for perpendicular or parallel alignment
            if abs(distance - required_distance) < self.grid_size / 2:
                if grid_x == center[0] or grid_y == center[1]:  # Same x or same y
                    func(grid_x, grid_y)
                    return  # Place only one circle per click