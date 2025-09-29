import tkinter as tk

def add_linkage_type(self, vertex1, vertex2, edge_label, type_tag):
    """Draw a black edge between two vertices."""
    # Draw a black edge between the selected vertices with increased width (3x)

    # Category 1: a1-2, a1-3, a1-4, a1-5, a1-6, a1-7, a1-9
    # Category 2: a2-3, a2-5, a2-6, a2-7, a2-8
    # Category 3: b1-2, b1-3, b1-4, b1-5, b1-6, b1-7, b1-8, b1-9

    edge = None

    if type_tag == 'a1to2' or type_tag == 'a1to3' or type_tag == 'a1to4' or type_tag == 'a1to5' or type_tag == 'a1to6' or type_tag == 'a1to7' or type_tag == 'a1to9':
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=5, fill="#F5791F", capstyle=tk.ROUND, tags=type_tag
        )
    elif type_tag == 'a2to3' or type_tag == 'a2to5' or type_tag == 'a2to6' or type_tag == 'a2to7' or type_tag == 'a2to8':
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=5, fill="#0072BB", capstyle=tk.ROUND, tags=type_tag
        )
    else:
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=5, fill="#01A653", capstyle=tk.ROUND, tags=type_tag
        )
    edge_text = self.canvas.create_text(
        (vertex1[0] + vertex2[0]) / 2, (vertex1[1] + vertex2[1]) / 2, text=edge_label, fill="#DFE1E5", anchor=tk.N, )
    self.edges[edge] = (vertex1, vertex2, type_tag)
    self.edge_text[edge_text] = edge_label
    self.undo_stack.append(edge)
    self.undo_stack.append(edge_text)
    # print(self.edges)