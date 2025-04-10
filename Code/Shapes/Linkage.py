import tkinter as tk

def add_linkage_type(self, vertex1, vertex2, edge_label, type_tag):
    """Draw a black edge between two vertices."""
    # Draw a black edge between the selected vertices with increased width (3x)
    edge = self.canvas.create_line(
        vertex1[0], vertex1[1], vertex2[0], vertex2[1],
        width=10, fill="black", capstyle=tk.ROUND, tags=type_tag
    )
    edge_text = self.canvas.create_text(
        (vertex1[0] + vertex2[0]) / 2, (vertex1[1] + vertex2[1]) / 2, text=edge_label, fill="#DFE1E5", anchor=tk.N, )
    self.edges[edge] = (vertex1, vertex2, type_tag)
    self.edge_text[edge_text] = edge_label
    # print(self.edges)