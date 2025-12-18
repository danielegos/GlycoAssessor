import tkinter as tk
from collections import deque, defaultdict
from PIL import ImageGrab, Image, ImageTk
from prettytable import PrettyTable
from tkinter import filedialog
import pandas as pd
import sys
import os


# from Code.Shapes.Edge import add_edge
# from Code.Shapes.Linkage import add_linkage_type
# from Code.Shapes.Vertex import add_vertex
# from Code.Shapes.Polygon import add_polygon_shape


# from Code.Shapes.Edge import add_edge
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

# from Code.Shapes.Linkage import add_linkage_type
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

# from Code.Shapes.Vertex import add_vertex
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

# from Code.Shapes.Polygon import add_polygon_shape
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



# TODO: Make the canvas zoomable
# TODO: Add descriptive comments throughout

# *****COMPLETE***** 1. Change the sugar symbols to be the correct shape and color.
#       I mean that the buttons themselves should be shapes and colors instead of
#       colored rectangles containing text inside. See the second column in this image
#       for all the symbol patterns that you will need. The columns after Column 2
#       contain the colors you will need.
#       Source: https://en.wikipedia.org/wiki/Symbol_Nomenclature_For_Glycans
#       Note: For the buttons, you should also include the 3-letter code for each
#       monosaccharide along with the shape.
# 2. Keep in mind that the window that contains the shapes  should be able to accommodate
#       about 30 more distinct shapes later on. We started with a handful because they are
#       the common ones in vertebrates, but there are dozens more of them.
# *****COMPLETE***** 3. If the user places the first sugar too near the top, can they move everything down to
#       make room for a branch that moves toward the top of the drawing canvas? If not, we
#       need to build in regulations about where the first sugar must be placed to allow
#       for adequate branching space up or down.
# 4. Is there a way to extend the canvas to the right, up, and down? Sole glycans are very
#       long and will need more space than is on the default canvas size. We need to
#       accommodate this.
# *****COMPLETE***** 5. Change the canvas to have colors or something to let people know where they can place
#       a shape.
# *****COMPLETE***** # 6. For people who accidentally place a fucose on the base node that is on the wrong level,
#       the software should give some sort of warning.


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Fallback to the script directory
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    return os.path.join(base_path, relative_path)


# Define the class to redirect print() output to a Text widget
class PrintToText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # Insert text at the end of the widget
        self.text_widget.yview(tk.END)  # Scroll to the end to show the new text

    def flush(self):
        pass  # This is required to avoid errors, but we don’t need it for this purpose

# TODO: Organize buttons, both the code and the GUI
# Define the main application class
class GridApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("GlycoAssessor")

        column_0 = tk.Frame(self.master)
        column_0.pack(side="left", padx=20, pady=10, anchor="n")

        button_r0_c0 = tk.Frame(column_0)
        button_r0_c0.pack(pady=1, anchor="w")  # Aligns row to the left

        self.undo_stack = [] # Keep track of actions (item IDs)


    # Sugar buttons ______________________________________________________________
        self.sugar_buttons_dict = {}

        # Add "Sugar Menu" text to row 1
        tk.Label(button_r0_c0, text="Sugar Menu", font=("Arial", 11, "bold"), bg='lightgray').pack(side="left", padx=5)


        button_r1_c0 = tk.Frame(column_0)
        button_r1_c0.pack(pady=1, anchor="w")  # Aligns row to the left


        # Add individual sugars in this order:      --------NOTE: About 20 buttons fit horizontally --------
        sugar_button_x = 42
        sugar_button_y = 42

        # Glc - Blue circle

        # Try using resource_path
        self.glc_img = Image.open(resource_path("Assets/Sugars/Glc.png")).resize((sugar_button_x, sugar_button_y))
        self.glc_button_image = ImageTk.PhotoImage(self.glc_img)
        self.add_glc_button = tk.Button(button_r1_c0, image=self.glc_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_glc_mode)
        self.add_glc_button.pack(side="left", padx=5)

        # GlcNAc - Blue square
        self.glcnac_img = Image.open(resource_path("Assets/Sugars/GlcNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.glcnac_button_image = ImageTk.PhotoImage(self.glcnac_img)
        self.add_glcnac_button = tk.Button(button_r1_c0, image=self.glcnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_glcnac_mode)
        self.add_glcnac_button.pack(side="left", padx=5)

        # GlcN - Blue crossed square
        self.glcn_img = Image.open(resource_path("Assets/Sugars/GlcN.png")).resize((sugar_button_x, sugar_button_y))
        self.glcn_button_image = ImageTk.PhotoImage(self.glcn_img)
        self.add_glcn_button = tk.Button(button_r1_c0, image=self.glcn_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_glcn_mode)
        self.add_glcn_button.pack(side="left", padx=5)

        # GlcA - Blue divided diamond
        self.glca_img = Image.open(resource_path("Assets/Sugars/GlcA.png")).resize((sugar_button_x, sugar_button_y))
        self.glca_button_image = ImageTk.PhotoImage(self.glca_img)
        self.add_glca_button = tk.Button(button_r1_c0, image=self.glca_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_glca_mode)
        self.add_glca_button.pack(side="left", padx=5)

        # Qui - Blue triangle
        self.qui_img = Image.open(resource_path("Assets/Sugars/Qui.png")).resize((sugar_button_x, sugar_button_y))
        self.qui_button_image = ImageTk.PhotoImage(self.qui_img)
        self.add_qui_button = tk.Button(button_r1_c0, image=self.qui_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_qui_mode)
        self.add_qui_button.pack(side="left", padx=5)

        # QuiNAc - Blue divided triangle
        self.quinac_img = Image.open(resource_path("Assets/Sugars/QuiNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.quinac_button_image = ImageTk.PhotoImage(self.quinac_img)
        self.add_quinac_button = tk.Button(button_r1_c0, image=self.quinac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_quinac_mode)
        self.add_quinac_button.pack(side="left", padx=5)

        # Oli - Blue rectangle
        self.oli_img = Image.open(resource_path("Assets/Sugars/Oli.png")).resize((sugar_button_x, sugar_button_y))
        self.oli_button_image = ImageTk.PhotoImage(self.oli_img)
        self.add_oli_button = tk.Button(button_r1_c0, image=self.oli_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_oli_mode)
        self.add_oli_button.pack(side="left", padx=5)

        # Bac - Blue hexagon
        self.bac_img = Image.open(resource_path("Assets/Sugars/Bac.png")).resize((sugar_button_x, sugar_button_y))
        self.bac_button_image = ImageTk.PhotoImage(self.bac_img)
        self.add_bac_button = tk.Button(button_r1_c0, image=self.bac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_bac_mode)
        self.add_bac_button.pack(side="left", padx=5)

        # Api - Blue pentagon
        self.api_img = Image.open(resource_path("Assets/Sugars/Api.png")).resize((sugar_button_x, sugar_button_y))
        self.api_button_image = ImageTk.PhotoImage(self.api_img)
        self.add_api_button = tk.Button(button_r1_c0, image=self.api_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_api_mode)
        self.add_api_button.pack(side="left", padx=5)

        # Man - Green circle
        self.man_img = Image.open(resource_path("Assets/Sugars/Man.png")).resize((sugar_button_x, sugar_button_y))
        self.man_button_image = ImageTk.PhotoImage(self.man_img)
        self.add_man_button = tk.Button(button_r1_c0, image=self.man_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_man_mode)
        self.add_man_button.pack(side="left", padx=5)

        # ManNAc - Green square
        self.mannac_img = Image.open(resource_path("Assets/Sugars/ManNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.mannac_button_image = ImageTk.PhotoImage(self.mannac_img)
        self.add_mannac_button = tk.Button(button_r1_c0, image=self.mannac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_mannac_mode)
        self.add_mannac_button.pack(side="left", padx=5)

        # ManN - Green crossed square
        self.mann_img = Image.open(resource_path("Assets/Sugars/ManN.png")).resize((sugar_button_x, sugar_button_y))
        self.mann_button_image = ImageTk.PhotoImage(self.mann_img)
        self.add_mann_button = tk.Button(button_r1_c0, image=self.mann_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_mann_mode)
        self.add_mann_button.pack(side="left", padx=5)

        # ManA - Green divided diamond
        self.mana_img = Image.open(resource_path("Assets/Sugars/ManA.png")).resize((sugar_button_x, sugar_button_y))
        self.mana_button_image = ImageTk.PhotoImage(self.mana_img)
        self.add_mana_button = tk.Button(button_r1_c0, image=self.mana_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_mana_mode)
        self.add_mana_button.pack(side="left", padx=5)

        # Rha - Green triangle
        self.rha_img = Image.open(resource_path("Assets/Sugars/Rha.png")).resize((sugar_button_x, sugar_button_y))
        self.rha_button_image = ImageTk.PhotoImage(self.rha_img)
        self.add_rha_button = tk.Button(button_r1_c0, image=self.rha_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_rha_mode)
        self.add_rha_button.pack(side="left", padx=5)

        # RhaNAc - Green divided triangle
        self.rhanac_img = Image.open(resource_path("Assets/Sugars/RhaNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.rhanac_button_image = ImageTk.PhotoImage(self.rhanac_img)
        self.add_rhanac_button = tk.Button(button_r1_c0, image=self.rhanac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_rhanac_mode)
        self.add_rhanac_button.pack(side="left", padx=5)

        # Tyv - Green rectangle
        self.tyv_img = Image.open(resource_path("Assets/Sugars/Tyv.png")).resize((sugar_button_x, sugar_button_y))
        self.tyv_button_image = ImageTk.PhotoImage(self.tyv_img)
        self.add_tyv_button = tk.Button(button_r1_c0, image=self.tyv_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_tyv_mode)
        self.add_tyv_button.pack(side="left", padx=5)

        # Ara - Green star
        self.ara_img = Image.open(resource_path("Assets/Sugars/Ara.png")).resize((sugar_button_x, sugar_button_y))
        self.ara_button_image = ImageTk.PhotoImage(self.ara_img)
        self.add_ara_button = tk.Button(button_r1_c0, image=self.ara_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_ara_mode)
        self.add_ara_button.pack(side="left", padx=5)

        # Kdn - Green diamond
        self.kdn_img = Image.open(resource_path("Assets/Sugars/Kdn.png")).resize((sugar_button_x, sugar_button_y))
        self.kdn_button_image = ImageTk.PhotoImage(self.kdn_img)
        self.add_kdn_button = tk.Button(button_r1_c0, image=self.kdn_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_kdn_mode)
        self.add_kdn_button.pack(side="left", padx=5)

        # Pse - Green flat diamond
        self.pse_img = Image.open(resource_path("Assets/Sugars/Pse.png")).resize((sugar_button_x, sugar_button_y))
        self.pse_button_image = ImageTk.PhotoImage(self.pse_img)
        self.add_pse_button = tk.Button(button_r1_c0, image=self.pse_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_pse_mode)
        self.add_pse_button.pack(side="left", padx=5)

        # LDManHep - Green hexagon
        self.ldmanhep_img = Image.open(resource_path("Assets/Sugars/LDManHep.png")).resize((sugar_button_x, sugar_button_y))
        self.ldmanhep_button_image = ImageTk.PhotoImage(self.ldmanhep_img)
        self.add_ldmanhep_button = tk.Button(button_r1_c0, image=self.ldmanhep_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_ldmanhep_mode)
        self.add_ldmanhep_button.pack(side="left", padx=5)

        # Fruc - Green pentagon
        self.fruc_img = Image.open(resource_path("Assets/Sugars/Fruc.png")).resize((sugar_button_x, sugar_button_y))
        self.fruc_button_image = ImageTk.PhotoImage(self.fruc_img)
        self.add_fruc_button = tk.Button(button_r1_c0, image=self.fruc_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_fruc_mode)
        self.add_fruc_button.pack(side="left", padx=5)

        # Gal - Yellow circle
        self.gal_img = Image.open(resource_path("Assets/Sugars/Gal.png")).resize((sugar_button_x, sugar_button_y))
        self.gal_button_image = ImageTk.PhotoImage(self.gal_img)
        self.add_gal_button = tk.Button(button_r1_c0, image=self.gal_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_gal_mode)
        self.add_gal_button.pack(side="left", padx=5)

        # GalNAc - Yellow square
        self.galnac_img = Image.open(resource_path("Assets/Sugars/GalNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.galnac_button_image = ImageTk.PhotoImage(self.galnac_img)
        self.add_galnac_button = tk.Button(button_r1_c0, image=self.galnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_galnac_mode)
        self.add_galnac_button.pack(side="left", padx=5)

        # GalN - Yellow crossed square
        self.galn_img = Image.open(resource_path("Assets/Sugars/GalN.png")).resize((sugar_button_x, sugar_button_y))
        self.galn_button_image = ImageTk.PhotoImage(self.galn_img)
        self.add_galn_button = tk.Button(button_r1_c0, image=self.galn_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_galn_mode)
        self.add_galn_button.pack(side="left", padx=5)

        # GalA - Yellow divided diamond
        self.gala_img = Image.open(resource_path("Assets/Sugars/GalA.png")).resize((sugar_button_x, sugar_button_y))
        self.gala_button_image = ImageTk.PhotoImage(self.gala_img)
        self.add_gala_button = tk.Button(button_r1_c0, image=self.gala_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_gala_mode)
        self.add_gala_button.pack(side="left", padx=5)

        # Move to row 2
        button_r2_c0 = tk.Frame(column_0)
        button_r2_c0.pack(pady=5, anchor="w")  # Aligns row to the left

        # Lyx - Yellow star
        self.lyx_img = Image.open(resource_path("Assets/Sugars/Lyx.png")).resize((sugar_button_x, sugar_button_y))
        self.lyx_button_image = ImageTk.PhotoImage(self.lyx_img)
        self.add_lyx_button = tk.Button(button_r2_c0, image=self.lyx_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_lyx_mode)
        self.add_lyx_button.pack(side="left", padx=5)

        # Leg - Yellow flat diamond
        self.leg_img = Image.open(resource_path("Assets/Sugars/Leg.png")).resize((sugar_button_x, sugar_button_y))
        self.leg_button_image = ImageTk.PhotoImage(self.leg_img)
        self.add_leg_button = tk.Button(button_r2_c0, image=self.leg_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_leg_mode)
        self.add_leg_button.pack(side="left", padx=5)

        # Kdo - Yellow hexagon
        self.kdo_img = Image.open(resource_path("Assets/Sugars/Kdo.png")).resize((sugar_button_x, sugar_button_y))
        self.kdo_button_image = ImageTk.PhotoImage(self.kdo_img)
        self.add_kdo_button = tk.Button(button_r2_c0, image=self.kdo_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_kdo_mode)
        self.add_kdo_button.pack(side="left", padx=5)

        # Tag - Yellow pentagon
        self.tag_img = Image.open(resource_path("Assets/Sugars/Tag.png")).resize((sugar_button_x, sugar_button_y))
        self.tag_button_image = ImageTk.PhotoImage(self.tag_img)
        self.add_tag_button = tk.Button(button_r2_c0, image=self.tag_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_tag_mode)
        self.add_tag_button.pack(side="left", padx=5)

        # Gul - Orange circle
        self.gul_img = Image.open(resource_path("Assets/Sugars/Gul.png")).resize((sugar_button_x, sugar_button_y))
        self.gul_button_image = ImageTk.PhotoImage(self.gul_img)
        self.add_gul_button = tk.Button(button_r2_c0, image=self.gul_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_gul_mode)
        self.add_gul_button.pack(side="left", padx=5)

        # GulNAc - Orange square
        self.gulnac_img = Image.open(resource_path("Assets/Sugars/GulNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.gulnac_button_image = ImageTk.PhotoImage(self.gulnac_img)
        self.add_gulnac_button = tk.Button(button_r2_c0, image=self.gulnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_gulnac_mode)
        self.add_gulnac_button.pack(side="left", padx=5)

        # GulN - Orange crossed square
        self.guln_img = Image.open(resource_path("Assets/Sugars/GulN.png")).resize((sugar_button_x, sugar_button_y))
        self.guln_button_image = ImageTk.PhotoImage(self.guln_img)
        self.add_guln_button = tk.Button(button_r2_c0, image=self.guln_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_guln_mode)
        self.add_guln_button.pack(side="left", padx=5)

        # GulA - Orange divided diamond
        self.gula_img = Image.open(resource_path("Assets/Sugars/GulA.png")).resize((sugar_button_x, sugar_button_y))
        self.gula_button_image = ImageTk.PhotoImage(self.gula_img)
        self.add_gula_button = tk.Button(button_r2_c0, image=self.gula_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_gula_mode)
        self.add_gula_button.pack(side="left", padx=5)

        # 6dGul - Orange triangle
        self._6dgul_img = Image.open(resource_path("Assets/Sugars/6dGul.png")).resize((sugar_button_x, sugar_button_y))
        self._6dgul_button_image = ImageTk.PhotoImage(self._6dgul_img)
        self.add_6dgul_button = tk.Button(button_r2_c0, image=self._6dgul_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_6dgul_mode)
        self.add_6dgul_button.pack(side="left", padx=5)

        # Abe - Orange rectangle
        self.abe_img = Image.open(resource_path("Assets/Sugars/Abe.png")).resize((sugar_button_x, sugar_button_y))
        self.abe_button_image = ImageTk.PhotoImage(self.abe_img)
        self.add_abe_button = tk.Button(button_r2_c0, image=self.abe_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_abe_mode)
        self.add_abe_button.pack(side="left", padx=5)

        # Xyl - Orange star
        self.xyl_img = Image.open(resource_path("Assets/Sugars/Xyl.png")).resize((sugar_button_x, sugar_button_y))
        self.xyl_button_image = ImageTk.PhotoImage(self.xyl_img)
        self.add_xyl_button = tk.Button(button_r2_c0, image=self.xyl_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_xyl_mode)
        self.add_xyl_button.pack(side="left", padx=5)

        # Dha - Orange hexagon
        self.dha_img = Image.open(resource_path("Assets/Sugars/Dha.png")).resize((sugar_button_x, sugar_button_y))
        self.dha_button_image = ImageTk.PhotoImage(self.dha_img)
        self.add_dha_button = tk.Button(button_r2_c0, image=self.dha_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_dha_mode)
        self.add_dha_button.pack(side="left", padx=5)

        # Sor - Orange pentagon
        self.sor_img = Image.open(resource_path("Assets/Sugars/Sor.png")).resize((sugar_button_x, sugar_button_y))
        self.sor_button_image = ImageTk.PhotoImage(self.sor_img)
        self.add_sor_button = tk.Button(button_r2_c0, image=self.sor_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_sor_mode)
        self.add_sor_button.pack(side="left", padx=5)

        # Alt - Pink circle
        self.alt_img = Image.open(resource_path("Assets/Sugars/Alt.png")).resize((sugar_button_x, sugar_button_y))
        self.alt_button_image = ImageTk.PhotoImage(self.alt_img)
        self.add_alt_button = tk.Button(button_r2_c0, image=self.alt_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_alt_mode)
        self.add_alt_button.pack(side="left", padx=5)

        # AltNAc - Pink square
        self.altnac_img = Image.open(resource_path("Assets/Sugars/AltNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.altnac_button_image = ImageTk.PhotoImage(self.altnac_img)
        self.add_altnac_button = tk.Button(button_r2_c0, image=self.altnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_altnac_mode)
        self.add_altnac_button.pack(side="left", padx=5)

        # AltN - Pink crossed square
        self.altn_img = Image.open(resource_path("Assets/Sugars/AltN.png")).resize((sugar_button_x, sugar_button_y))
        self.altn_button_image = ImageTk.PhotoImage(self.altn_img)
        self.add_altn_button = tk.Button(button_r2_c0, image=self.altn_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_altn_mode)
        self.add_altn_button.pack(side="left", padx=5)

        # AltA - Pink divided diamond
        self.alta_img = Image.open(resource_path("Assets/Sugars/AltA.png")).resize((sugar_button_x, sugar_button_y))
        self.alta_button_image = ImageTk.PhotoImage(self.alta_img)
        self.add_alta_button = tk.Button(button_r2_c0, image=self.alta_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_alta_mode)
        self.add_alta_button.pack(side="left", padx=5)

        # 6dAlt - Pink triangle
        self._6dalt_img = Image.open(resource_path("Assets/Sugars/6dAlt.png")).resize((sugar_button_x, sugar_button_y))
        self._6dalt_button_image = ImageTk.PhotoImage(self._6dalt_img)
        self.add_6dalt_button = tk.Button(button_r2_c0, image=self._6dalt_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_6dalt_mode)
        self.add_6dalt_button.pack(side="left", padx=5)

        # 6dAltNAc - Pink divided triangle
        self._6daltnac_img = Image.open(resource_path("Assets/Sugars/6dAltNAc.png")).resize((sugar_button_x, sugar_button_y))
        self._6daltnac_button_image = ImageTk.PhotoImage(self._6daltnac_img)
        self.add_6daltnac_button = tk.Button(button_r2_c0, image=self._6daltnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_6daltnac_mode)
        self.add_6daltnac_button.pack(side="left", padx=5)

        # Par - Pink rectangle
        self.par_img = Image.open(resource_path("Assets/Sugars/Par.png")).resize((sugar_button_x, sugar_button_y))
        self.par_button_image = ImageTk.PhotoImage(self.par_img)
        self.add_par_button = tk.Button(button_r2_c0, image=self.par_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_par_mode)
        self.add_par_button.pack(side="left", padx=5)

        # Rib - Pink star
        self.rib_img = Image.open(resource_path("Assets/Sugars/Rib.png")).resize((sugar_button_x, sugar_button_y))
        self.rib_button_image = ImageTk.PhotoImage(self.rib_img)
        self.add_rib_button = tk.Button(button_r2_c0, image=self.rib_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_rib_mode)
        self.add_rib_button.pack(side="left", padx=5)

        # Aci - Pink flat diamond
        self.aci_img = Image.open(resource_path("Assets/Sugars/Aci.png")).resize((sugar_button_x, sugar_button_y))
        self.aci_button_image = ImageTk.PhotoImage(self.aci_img)
        self.add_aci_button = tk.Button(button_r2_c0, image=self.aci_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_aci_mode)
        self.add_aci_button.pack(side="left", padx=5)

        # DDManHep - Pink hexagon
        self.ddmanhep_img = Image.open(resource_path("Assets/Sugars/DDManHep.png")).resize((sugar_button_x, sugar_button_y))
        self.ddmanhep_button_image = ImageTk.PhotoImage(self.ddmanhep_img)
        self.add_ddmanhep_button = tk.Button(button_r2_c0, image=self.ddmanhep_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_ddmanhep_mode)
        self.add_ddmanhep_button.pack(side="left", padx=5)

        # Psi - Pink pentagon
        self.psi_img = Image.open(resource_path("Assets/Sugars/Psi.png")).resize((sugar_button_x, sugar_button_y))
        self.psi_button_image = ImageTk.PhotoImage(self.psi_img)
        self.add_psi_button = tk.Button(button_r2_c0, image=self.psi_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_psi_mode)
        self.add_psi_button.pack(side="left", padx=5)

        # All - Purple circle
        self.all_img = Image.open(resource_path("Assets/Sugars/All.png")).resize((sugar_button_x, sugar_button_y))
        self.all_button_image = ImageTk.PhotoImage(self.all_img)
        self.add_all_button = tk.Button(button_r2_c0, image=self.all_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_all_mode)
        self.add_all_button.pack(side="left", padx=5)

        # Move to row 3
        button_r3_c0 = tk.Frame(column_0)
        button_r3_c0.pack(pady=5, anchor="w")  # Aligns row to the left

        # AllNAc - Purple square
        self.allnac_img = Image.open(resource_path("Assets/Sugars/AllNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.allnac_button_image = ImageTk.PhotoImage(self.allnac_img)
        self.add_allnac_button = tk.Button(button_r3_c0, image=self.allnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_allnac_mode)
        self.add_allnac_button.pack(side="left", padx=5)

        # AllN - Purple crossed square
        self.alln_img = Image.open(resource_path("Assets/Sugars/AllN.png")).resize((sugar_button_x, sugar_button_y))
        self.alln_button_image = ImageTk.PhotoImage(self.alln_img)
        self.add_alln_button = tk.Button(button_r3_c0, image=self.alln_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_alln_mode)
        self.add_alln_button.pack(side="left", padx=5)

        # AllA - Purple divided diamond
        self.alla_img = Image.open(resource_path("Assets/Sugars/AllA.png")).resize((sugar_button_x, sugar_button_y))
        self.alla_button_image = ImageTk.PhotoImage(self.alla_img)
        self.add_alla_button = tk.Button(button_r3_c0, image=self.alla_button_image, borderwidth=0,
                                         highlightthickness=0, command=self.select_add_alla_mode)
        self.add_alla_button.pack(side="left", padx=5)

        # Dig - Purple rectangle
        self.dig_img = Image.open(resource_path("Assets/Sugars/Dig.png")).resize((sugar_button_x, sugar_button_y))
        self.dig_button_image = ImageTk.PhotoImage(self.dig_img)
        self.add_dig_button = tk.Button(button_r3_c0, image=self.dig_button_image, borderwidth=0,
                                         highlightthickness=0, command=self.select_add_dig_mode)
        self.add_dig_button.pack(side="left", padx=5)

        # Neu5Ac - Purple diamond
        self.neu5ac_img = Image.open(resource_path("Assets/Sugars/Neu5Ac.png")).resize((sugar_button_x, sugar_button_y))
        self.neu5ac_button_image = ImageTk.PhotoImage(self.neu5ac_img)
        self.add_neu5ac_button = tk.Button(button_r3_c0, image=self.neu5ac_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_neu5ac_mode)
        self.add_neu5ac_button.pack(side="left", padx=5)

        # MurNAc - Purple hexagon
        self.murnac_img = Image.open(resource_path("Assets/Sugars/MurNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.murnac_button_image = ImageTk.PhotoImage(self.murnac_img)
        self.add_murnac_button = tk.Button(button_r3_c0, image=self.murnac_button_image, borderwidth=0,
                                         highlightthickness=0, command=self.select_add_murnac_mode)
        self.add_murnac_button.pack(side="left", padx=5)

        # Tal - Light Blue circle
        self.tal_img = Image.open(resource_path("Assets/Sugars/Tal.png")).resize((sugar_button_x, sugar_button_y))
        self.tal_button_image = ImageTk.PhotoImage(self.tal_img)
        self.add_tal_button = tk.Button(button_r3_c0, image=self.tal_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_tal_mode)
        self.add_tal_button.pack(side="left", padx=5)

        # TalNAc - Light Blue square
        self.talnac_img = Image.open(resource_path("Assets/Sugars/TalNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.talnac_button_image = ImageTk.PhotoImage(self.talnac_img)
        self.add_talnac_button = tk.Button(button_r3_c0, image=self.talnac_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_talnac_mode)
        self.add_talnac_button.pack(side="left", padx=5)

        # TalN - Light Blue crossed square
        self.taln_img = Image.open(resource_path("Assets/Sugars/TalN.png")).resize((sugar_button_x, sugar_button_y))
        self.taln_button_image = ImageTk.PhotoImage(self.taln_img)
        self.add_taln_button = tk.Button(button_r3_c0, image=self.taln_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_taln_mode)
        self.add_taln_button.pack(side="left", padx=5)

        # TalA - Light Blue divided diamond
        self.tala_img = Image.open(resource_path("Assets/Sugars/TalA.png")).resize((sugar_button_x, sugar_button_y))
        self.tala_button_image = ImageTk.PhotoImage(self.tala_img)
        self.add_tala_button = tk.Button(button_r3_c0, image=self.tala_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_tala_mode)
        self.add_tala_button.pack(side="left", padx=5)

        # 6dTal - Light Blue triangle
        self._6dtal_img = Image.open(resource_path("Assets/Sugars/6dTal.png")).resize((sugar_button_x, sugar_button_y))
        self._6dtal_button_image = ImageTk.PhotoImage(self._6dtal_img)
        self.add_6dtal_button = tk.Button(button_r3_c0, image=self._6dtal_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_6dtal_mode)
        self.add_6dtal_button.pack(side="left", padx=5)

        # 6dTalNAc - Light Blue diided triangle
        self._6dtalnac_img = Image.open(resource_path("Assets/Sugars/6dTalNAc.png")).resize((sugar_button_x, sugar_button_y))
        self._6dtalnac_button_image = ImageTk.PhotoImage(self._6dtalnac_img)
        self.add_6dtalnac_button = tk.Button(button_r3_c0, image=self._6dtalnac_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_6dtalnac_mode)
        self.add_6dtalnac_button.pack(side="left", padx=5)

        # Col - Light Blue rectangle
        self.col_img = Image.open(resource_path("Assets/Sugars/Col.png")).resize((sugar_button_x, sugar_button_y))
        self.col_button_image = ImageTk.PhotoImage(self.col_img)
        self.add_col_button = tk.Button(button_r3_c0, image=self.col_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_col_mode)
        self.add_col_button.pack(side="left", padx=5)

        # Neu5Gc - Light Blue diamond
        self.neu5gc_img = Image.open(resource_path("Assets/Sugars/Neu5Gc.png")).resize((sugar_button_x, sugar_button_y))
        self.neu5gc_button_image = ImageTk.PhotoImage(self.neu5gc_img)
        self.add_neu5gc_button = tk.Button(button_r3_c0, image=self.neu5gc_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_neu5gc_mode)
        self.add_neu5gc_button.pack(side="left", padx=5)

        # 4eLeg - Light Blue flat diamond
        self._4eleg_img = Image.open(resource_path("Assets/Sugars/4eLeg.png")).resize((sugar_button_x, sugar_button_y))
        self._4eleg_button_image = ImageTk.PhotoImage(self._4eleg_img)
        self.add_4eleg_button = tk.Button(button_r3_c0, image=self._4eleg_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_4eleg_mode)
        self.add_4eleg_button.pack(side="left", padx=5)

        # MurNGc - Light Blue hexagon
        self._murngc_img = Image.open(resource_path("Assets/Sugars/MurNGc.png")).resize((sugar_button_x, sugar_button_y))
        self._murngc_button_image = ImageTk.PhotoImage(self._murngc_img)
        self.add_murngc_button = tk.Button(button_r3_c0, image=self._murngc_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_murngc_mode)
        self.add_murngc_button.pack(side="left", padx=5)

        # Ido - Brown circle
        self._ido_img = Image.open(resource_path("Assets/Sugars/Ido.png")).resize((sugar_button_x, sugar_button_y))
        self._ido_button_image = ImageTk.PhotoImage(self._ido_img)
        self.add_ido_button = tk.Button(button_r3_c0, image=self._ido_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_ido_mode)
        self.add_ido_button.pack(side="left", padx=5)

        # IdoNAc - Brown square
        self._idonac_img = Image.open(resource_path("Assets/Sugars/IdoNAc.png")).resize((sugar_button_x, sugar_button_y))
        self._idonac_button_image = ImageTk.PhotoImage(self._idonac_img)
        self.add_idonac_button = tk.Button(button_r3_c0, image=self._idonac_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_idonac_mode)
        self.add_idonac_button.pack(side="left", padx=5)

        # IdoN - Brown crossed square
        self._idon_img = Image.open(resource_path("Assets/Sugars/IdoN.png")).resize((sugar_button_x, sugar_button_y))
        self._idon_button_image = ImageTk.PhotoImage(self._idon_img)
        self.add_idon_button = tk.Button(button_r3_c0, image=self._idon_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_idon_mode)
        self.add_idon_button.pack(side="left", padx=5)

        # IdoA - Brown divided diamond
        self._idoa_img = Image.open(resource_path("Assets/Sugars/IdoA.png")).resize((sugar_button_x, sugar_button_y))
        self._idoa_button_image = ImageTk.PhotoImage(self._idoa_img)
        self.add_idoa_button = tk.Button(button_r3_c0, image=self._idoa_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_idoa_mode)
        self.add_idoa_button.pack(side="left", padx=5)

        # Neu - Brown diamond
        self._neu_img = Image.open(resource_path("Assets/Sugars/Neu.png")).resize((sugar_button_x, sugar_button_y))
        self._neu_button_image = ImageTk.PhotoImage(self._neu_img)
        self.add_neu_button = tk.Button(button_r3_c0, image=self._neu_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_neu_mode)
        self.add_neu_button.pack(side="left", padx=5)

        # Mur - Brown hexagon
        self._mur_img = Image.open(resource_path("Assets/Sugars/Mur.png")).resize((sugar_button_x, sugar_button_y))
        self._mur_button_image = ImageTk.PhotoImage(self._mur_img)
        self.add_mur_button = tk.Button(button_r3_c0, image=self._mur_button_image,
                                         borderwidth=0, highlightthickness=0, command=self.select_add_mur_mode)
        self.add_mur_button.pack(side="left", padx=5)

        # Fuc - Red triangle
        self.fuc_img = Image.open(resource_path("Assets/Sugars/Fuc.png")).resize((sugar_button_x, sugar_button_y))
        self.fuc_button_image = ImageTk.PhotoImage(self.fuc_img)
        self.add_fuc_button = tk.Button(button_r3_c0, image=self.fuc_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_fuc_mode)
        self.add_fuc_button.pack(side="left", padx=5)

        # FucNAc - Red divided triangle
        self.fucnac_img = Image.open(resource_path("Assets/Sugars/FucNAc.png")).resize((sugar_button_x, sugar_button_y))
        self.fucnac_button_image = ImageTk.PhotoImage(self.fucnac_img)
        self.add_fucnac_button = tk.Button(button_r3_c0, image=self.fucnac_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_fucnac_mode)
        self.add_fucnac_button.pack(side="left", padx=5)

        # Sia - Red diamond
        self.sia_img = Image.open(resource_path("Assets/Sugars/Sia.png")).resize((sugar_button_x, sugar_button_y))
        self.sia_button_image = ImageTk.PhotoImage(self.sia_img)
        self.add_sia_button = tk.Button(button_r3_c0, image=self.sia_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_sia_mode)
        self.add_sia_button.pack(side="left", padx=5)



    # Linkage buttons ____________________________________________________________

        button_r2_0_c0 = tk.Frame(column_0)
        button_r2_0_c0.pack(pady=1, anchor="w")

        tk.Label(button_r2_0_c0, text="Linkage Menu", font=("Arial", 11, "bold"), bg='lightgray').pack()

        button_r2_1_c0 = tk.Frame(column_0)
        button_r2_1_c0.pack(pady=1, anchor="w")

        # Category 1: a1-2, a1-3, a1-4, a1-5, a1-6, a1-7, a1-9
        # Category 2: a2-3, a2-5, a2-6, a2-7, a2-8
        # Category 3: b1-2, b1-3, b1-4, b1-5, b1-6, b1-7, b1-8, b1-9

        # Category 1 -----------------------------------------------------------
        self.a1to2_img = Image.open(resource_path("Assets/Button_imgs/α1,2.png")).resize((36, 27))
        self.a1to2_button_image = ImageTk.PhotoImage(self.a1to2_img)
        self.add_a1to2_button = tk.Button(button_r2_1_c0, image=self.a1to2_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a1to2_mode)
        self.add_a1to2_button.pack(side="left", padx=5)

        # self.add_a1to2_button = tk.Button(button_r2_1_c0, text="Add α1,2", command=self.select_add_a1to2_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to2_button.pack(side="left", padx=5)

        self.a1to3_img = Image.open(resource_path("Assets/Button_imgs/α1,3.png")).resize((36, 27))
        self.a1to3_button_image = ImageTk.PhotoImage(self.a1to3_img)
        self.add_a1to3_button = tk.Button(button_r2_1_c0, image=self.a1to3_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to3_mode)
        self.add_a1to3_button.pack(side="left", padx=5)

        # self.add_a1to3_button = tk.Button(button_r2_1_c0, text="Add α1,3", command=self.select_add_a1to3_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to3_button.pack(side="left", padx=5)

        self.a1to4_img = Image.open(resource_path("Assets/Button_imgs/α1,4.png")).resize((36, 27))
        self.a1to4_button_image = ImageTk.PhotoImage(self.a1to4_img)
        self.add_a1to4_button = tk.Button(button_r2_1_c0, image=self.a1to4_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to4_mode)
        self.add_a1to4_button.pack(side="left", padx=5)
        #
        # self.add_a1to4_button = tk.Button(button_r2_1_c0, text="Add α1,4", command=self.select_add_a1to4_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to4_button.pack(side="left", padx=5)

        self.a1to5_img = Image.open(resource_path("Assets/Button_imgs/α1,5.png")).resize((36, 27))
        self.a1to5_button_image = ImageTk.PhotoImage(self.a1to5_img)
        self.add_a1to5_button = tk.Button(button_r2_1_c0, image=self.a1to5_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to5_mode)
        self.add_a1to5_button.pack(side="left", padx=5)

        # self.add_a1to5_button = tk.Button(button_r2_1_c0, text="Add α1,5", command=self.select_add_a1to5_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to5_button.pack(side="left", padx=5)

        self.a1to6_img = Image.open(resource_path("Assets/Button_imgs/α1,6.png")).resize((36, 27))
        self.a1to6_button_image = ImageTk.PhotoImage(self.a1to6_img)
        self.add_a1to6_button = tk.Button(button_r2_1_c0, image=self.a1to6_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to6_mode)
        self.add_a1to6_button.pack(side="left", padx=5)

        # self.add_a1to6_button = tk.Button(button_r2_1_c0, text="Add α1,6", command=self.select_add_a1to6_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to6_button.pack(side="left", padx=5)

        self.a1to7_img = Image.open(resource_path("Assets/Button_imgs/α1,7.png")).resize((36, 27))
        self.a1to7_button_image = ImageTk.PhotoImage(self.a1to7_img)
        self.add_a1to7_button = tk.Button(button_r2_1_c0, image=self.a1to7_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to7_mode)
        self.add_a1to7_button.pack(side="left", padx=5)

        # self.add_a1to7_button = tk.Button(button_r2_1_c0, text="Add α1,7", command=self.select_add_a1to7_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to7_button.pack(side="left", padx=5)

        self.a1to9_img = Image.open(resource_path("Assets/Button_imgs/α1,9.png")).resize((36, 27))
        self.a1to9_button_image = ImageTk.PhotoImage(self.a1to9_img)
        self.add_a1to9_button = tk.Button(button_r2_1_c0, image=self.a1to9_button_image,
                                          borderwidth=0, highlightthickness=0, command=self.select_add_a1to9_mode)
        self.add_a1to9_button.pack(side="left", padx=5)

        # self.add_a1to9_button = tk.Button(button_r2_1_c0, text="Add α1,9", command=self.select_add_a1to9_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a1to9_button.pack(side="left", padx=5)

        # Category 2 -----------------------------------------------------------
        # ADD a2-3
        self.a2to3_img = Image.open(resource_path("Assets/Button_imgs/α2,3.png")).resize((36, 27))
        self.a2to3_button_image = ImageTk.PhotoImage(self.a2to3_img)
        self.add_a2to3_button = tk.Button(button_r2_1_c0, image=self.a2to3_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a2to3_mode)
        self.add_a2to3_button.pack(side="left", padx=5)

        # self.add_a2to3_button = tk.Button(button_r2_1_c0, text="Add α2,3", command=self.select_add_a2to3_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a2to3_button.pack(side="left", padx=5)

        # ADD a2-5
        self.a2to5_img = Image.open(resource_path("Assets/Button_imgs/α2,5.png")).resize((36, 27))
        self.a2to5_button_image = ImageTk.PhotoImage(self.a2to5_img)
        self.add_a2to5_button = tk.Button(button_r2_1_c0, image=self.a2to5_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a2to5_mode)
        self.add_a2to5_button.pack(side="left", padx=5)
        #
        # self.add_a2to5_button = tk.Button(button_r2_1_c0, text="Add α2,5", command=self.select_add_a2to5_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a2to5_button.pack(side="left", padx=5)
        #
        # ADD a2-6
        self.a2to6_img = Image.open(resource_path("Assets/Button_imgs/α2,6.png")).resize((36, 27))
        self.a2to6_button_image = ImageTk.PhotoImage(self.a2to6_img)
        self.add_a2to6_button = tk.Button(button_r2_1_c0, image=self.a2to6_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a2to6_mode)
        self.add_a2to6_button.pack(side="left", padx=5)

        # self.add_a2to6_button = tk.Button(button_r2_1_c0, text="Add α2,6", command=self.select_add_a2to6_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a2to6_button.pack(side="left", padx=5)
        #
        # ADD a2-7
        self.a2to7_img = Image.open(resource_path("Assets/Button_imgs/α2,7.png")).resize((36, 27))
        self.a2to7_button_image = ImageTk.PhotoImage(self.a2to7_img)
        self.add_a2to7_button = tk.Button(button_r2_1_c0, image=self.a2to7_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a2to7_mode)
        self.add_a2to7_button.pack(side="left", padx=5)
        #
        # self.add_a2to7_button = tk.Button(button_r2_1_c0, text="Add α2,7", command=self.select_add_a2to7_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a2to7_button.pack(side="left", padx=5)
        #
        # ADD a2-8
        self.a2to8_img = Image.open(resource_path("Assets/Button_imgs/α2,8.png")).resize((36, 27))
        self.a2to8_button_image = ImageTk.PhotoImage(self.a2to8_img)
        self.add_a2to8_button = tk.Button(button_r2_1_c0, image=self.a2to8_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_a2to8_mode)
        self.add_a2to8_button.pack(side="left", padx=5)
        #
        # self.add_a2to8_button = tk.Button(button_r2_1_c0, text="Add α2,8", command=self.select_add_a2to8_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_a2to8_button.pack(side="left", padx=5)


        # Category 3 -----------------------------------------------------------
        self.b1to2_img = Image.open(resource_path("Assets/Button_imgs/ß1,2.png")).resize((36, 27))
        self.b1to2_button_image = ImageTk.PhotoImage(self.b1to2_img)
        self.add_b1to2_button = tk.Button(button_r2_1_c0, image=self.b1to2_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to2_mode)
        self.add_b1to2_button.pack(side="left", padx=5)

        # self.add_b1to2_button = tk.Button(button_r2_1_c0, text="Add ß1,2", command=self.select_add_b1to2_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to2_button.pack(side="left", padx=5)

        self.b1to3_img = Image.open(resource_path("Assets/Button_imgs/ß1,3.png")).resize((36, 27))
        self.b1to3_button_image = ImageTk.PhotoImage(self.b1to3_img)
        self.add_b1to3_button = tk.Button(button_r2_1_c0, image=self.b1to3_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to3_mode)
        self.add_b1to3_button.pack(side="left", padx=5)
        #
        # self.add_b1to3_button = tk.Button(button_r2_1_c0, text="Add ß1,3", command=self.select_add_b1to3_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to3_button.pack(side="left", padx=5)

        self.b1to4_img = Image.open(resource_path("Assets/Button_imgs/ß1,4.png")).resize((36, 27))
        self.b1to4_button_image = ImageTk.PhotoImage(self.b1to4_img)
        self.add_b1to4_button = tk.Button(button_r2_1_c0, image=self.b1to4_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to4_mode)
        self.add_b1to4_button.pack(side="left", padx=5)
        #
        # self.add_b1to4_button = tk.Button(button_r2_1_c0, text="Add ß1,4", command=self.select_add_b1to4_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to4_button.pack(side="left", padx=5)

        self.b1to5_img = Image.open(resource_path("Assets/Button_imgs/ß1,5.png")).resize((36, 27))
        self.b1to5_button_image = ImageTk.PhotoImage(self.b1to5_img)
        self.add_b1to5_button = tk.Button(button_r2_1_c0, image=self.b1to5_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to5_mode)
        self.add_b1to5_button.pack(side="left", padx=5)
        #
        # self.add_b1to5_button = tk.Button(button_r2_1_c0, text="Add ß1,5", command=self.select_add_b1to5_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to5_button.pack(side="left", padx=5)

        self.b1to6_img = Image.open(resource_path("Assets/Button_imgs/ß1,6.png")).resize((36, 27))
        self.b1to6_button_image = ImageTk.PhotoImage(self.b1to6_img)
        self.add_b1to6_button = tk.Button(button_r2_1_c0, image=self.b1to6_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to6_mode)
        self.add_b1to6_button.pack(side="left", padx=5)
        #
        # self.add_b1to6_button = tk.Button(button_r2_1_c0, text="Add ß1,6", command=self.select_add_b1to6_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to6_button.pack(side="left", padx=5)

        self.b1to7_img = Image.open(resource_path("Assets/Button_imgs/ß1,7.png")).resize((36, 27))
        self.b1to7_button_image = ImageTk.PhotoImage(self.b1to7_img)
        self.add_b1to7_button = tk.Button(button_r2_1_c0, image=self.b1to7_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to7_mode)
        self.add_b1to7_button.pack(side="left", padx=5)
        #
        # self.add_b1to7_button = tk.Button(button_r2_1_c0, text="Add ß1,7", command=self.select_add_b1to7_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to7_button.pack(side="left", padx=5)
        #

        self.b1to8_img = Image.open(resource_path("Assets/Button_imgs/ß1,8.png")).resize((36, 27))
        self.b1to8_button_image = ImageTk.PhotoImage(self.b1to8_img)
        self.add_b1to8_button = tk.Button(button_r2_1_c0, image=self.b1to8_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to8_mode)
        self.add_b1to8_button.pack(side="left", padx=5)
        #
        # self.add_b1to8_button = tk.Button(button_r2_1_c0, text="Add ß1,8", command=self.select_add_b1to8_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to8_button.pack(side="left", padx=5)
        #
        self.b1to9_img = Image.open(resource_path("Assets/Button_imgs/ß1,9.png")).resize((36, 27))
        self.b1to9_button_image = ImageTk.PhotoImage(self.b1to9_img)
        self.add_b1to9_button = tk.Button(button_r2_1_c0, image=self.b1to9_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_b1to9_mode)
        self.add_b1to9_button.pack(side="left", padx=5)
        #
        # self.add_b1to9_button = tk.Button(button_r2_1_c0, text="Add ß1,9", command=self.select_add_b1to9_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.add_b1to9_button.pack(side="left", padx=5)


        #TODO: Fix the delete buttons!

        self.rm_edge_button = tk.Button(button_r2_1_c0, text="Remove Edge", command=self.select_rm_edge_mode)
        self.rm_edge_button.pack(side="left", padx=5)

        self.rm_edge_text_button = tk.Button(button_r2_1_c0, text="Remove Edge Text", command=self.select_rm_edge_text_mode)
        self.rm_edge_text_button.pack(side="left", padx=5)

        self.rm_circle_button = tk.Button(button_r2_1_c0, text="Remove Node", command=self.select_rm_circle_mode)
        self.rm_circle_button.pack(side="left", padx=5)


    # Analysis buttons ___________________________________________________________

        button_r3_1_c0 = tk.Frame(column_0)
        button_r3_1_c0.pack(pady=1, anchor="w")

        tk.Label(button_r3_1_c0, text="Analysis Tools", font=("Arial", 11, "bold"), bg='lightgray').pack()

        button_r3_c0 = tk.Frame(column_0)
        button_r3_c0.pack(pady=1, anchor="w")

        # Calculate DCI

        self.dci_img = Image.open(resource_path("Assets/Button_imgs/dci_img.png")).resize((92, 42))
        self.dci_button_image = ImageTk.PhotoImage(self.dci_img)
        self.add_dci_button = tk.Button(button_r3_c0, image=self.dci_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_calc_dci_mode)
        self.add_dci_button.pack(side="left", padx=5)


        # Calculate PCI with new button image

        self.pci_img = Image.open(resource_path("Assets/Button_imgs/pci_img.png")).resize((92, 42))
        self.pci_button_image = ImageTk.PhotoImage(self.pci_img)
        self.add_pci_button = tk.Button(button_r3_c0, image=self.pci_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_calc_pci_mode)
        self.add_pci_button.pack(side="left", padx=5)

        # Export image
        self.export_img = Image.open(resource_path("Assets/Button_imgs/exportImage.png")).resize((92, 42))
        self.export_button_image = ImageTk.PhotoImage(self.export_img)
        self.export_button = tk.Button(button_r3_c0, image = self.export_button_image, borderwidth=0,
                                       highlightthickness=0, command=self.select_export_image_mode)
        self.export_button.pack(side="left", padx=5)
        #
        # # Button to calculate DCI
        # self.dci_calc_button = tk.Button(button_r3_c0, text="Calculate DCI", command=self.select_calc_dci_mode,
        #                                  background="#639F52", foreground="#1E1F22", height = 3)
        # self.dci_calc_button.pack(side="left", padx=5)
        #
        # # Button to calculate PCI
        # self.pci_calc_button = tk.Button(button_r3_c0, text="Calculate PCI", command=self.select_calc_pci_mode,
        #                                  background="#639F52", foreground="#1E1F22", height = 3)
        # self.pci_calc_button.pack(side="left", padx=5)

        # # Undo Button
        # self.undo_button = tk.Button(button_r3_c0, text="Undo", command=self.undo)
        # self.undo_button.pack(side="left", padx=5)

        # Button to reset the program
        # self.reset_button = tk.Button(button_r3_c0, text="Reset", command=self.reset_app,
        #                                  background="#EC1B25", foreground="black", height = 3)
        # self.reset_button.pack(side="left", padx=25)

        self.reset_img = Image.open(resource_path("Assets/Button_imgs/reset.png")).resize((42, 42))
        self.reset_button_image = ImageTk.PhotoImage(self.reset_img)
        self.reset_button = tk.Button(button_r3_c0, image=self.reset_button_image, borderwidth=0,
                                       highlightthickness=0, command=self.reset_app)
        self.reset_button.pack(side="left", padx=5)

   # Canvas _____________________________________________________________________

        # # Original Canvas widget
        button_r4_c0 = tk.Frame(column_0)
        button_r4_c0.pack(pady=1, anchor="w")


        self.canvas = tk.Canvas(button_r4_c0, width=1920, height=1080, bg='#2B2D30')  # Uncomment for large UI
        self.canvas.pack()

        # Grid size
        self.grid_size = 20
        self.vertices = []  # List to store the centers of circles

        # Dictionaries to store edges and circles
        self.edges = {}  # List to store edges
        self.circles = {}  # Dictionary to store circle items
        self.edge_text = {}  # Dict to store edge text (linkage type labels)

        # Flag to track if the first circle has been placed
        self.first_circle_placed = False
        self.first_vertex = None  # Track the first selected vertex for edges

        # Mode tracking
        self.mode = None  # Default mode is Circle
        self.start_x = None
        self.start_y = None
        self.current_line = None  # To track the current line being drawn

        # Draw grid
        self.draw_grid()

    # Instructions and Log ________________________________________________________

        tk.Label(button_r3_c0, text="Instructions and Log", font=("Arial", 12, "bold"), bg='lightgray').pack(side="left", padx=5)

        # Create a Text widget for printing output
        self.text_area = tk.Text(button_r3_c0, height=4, width=200)
        self.text_area.pack(side="left",padx=5)

        # Redirect print() to the Text widget
        printer = PrintToText(self.text_area)
        sys.stdout = printer

        print("Instructions:"
              "\nSelect a sugar type. Click the left side of the grid to place the base node."
              "\n\nPlacement of subsequent nodes is restricted to specific points."
              "\n\nSelect a linkage type. Click on two sugar nodes to connect them with the linkage."
              "\n\nOrient the N-glycan with the base node at the left and the furthest node on the right.")

        print("\nGitHub repo: https://github.com/danielegos/GlycoAssessor")
        print("\n\nSee video tutorial at this link: https://youtu.be/4d3WOO03Q34")

        print("\nAssumptions:"
              "\n1) The leftmost node you add is the base node of the N-glycan. "
              "\n2) You will not attempt to duplicate edges."
              "\n3) You will only draw edges between two adjacent nodes."
              "\n4) You must place base-node Fucosylations at the 2nd level explicitly."
              "\n5) Glycans must be drawn from left to right.\n")


        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.handle_click)  # Left click to place vertices or start edge



    def reset_app(self):
        self.canvas.delete("all")  # Clear canvas
        self.draw_grid()  # Redraw grid
        self.vertices = []  # List to store the centers of circles

        # Dictionaries to store edges and circles
        self.edges = {}  # List to store edges
        self.circles = {}  # Dictionary to store circle items
        self.edge_text = {}  # Dict to store edge text (linkage type labels)

        # Flag to track if the first circle has been placed
        self.first_circle_placed = False
        self.first_vertex = None  # Track the first selected vertex for edges

        # Mode tracking
        self.mode = None  # Default mode is Circle
        self.start_x = None
        self.start_y = None
        self.current_line = None  # To track the current line being drawn

        print("Reset")


    def draw_grid(self):
        """Draw the grid lines on the canvas."""
        radius = 5 # Radius for the small intersection circles
        for i in range(0, 1800, self.grid_size):
            self.canvas.create_line(i, 0, i, 1800, fill="#545557", tags="grid")
            self.canvas.create_line(0, i, 1800, i, fill="#545557", tags="grid")

            # Circle gap
            circle_spacing = 80

            # Add small circles at intersection points
            for x in range(0, 1600, circle_spacing):
                for y in range(0, 1600, circle_spacing):
                    self.canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius,
                        fill="#545557", outline="", tags="grid_dot"
                    )
            start_radius = 20
            # Add start indicator circle
            self.canvas.create_oval(
                80 - start_radius, 240 - start_radius, 80 + start_radius, 240 + start_radius,
                fill="black", outline="", tags="grid_dot"
            )

            self.canvas.create_text(
                80, 240, text="START", fill="white")

# Modes to add circles

    # Glc - Blue circle
    def select_add_glc_mode(self):
        self.mode = "Add Glc Node"

    # GlcNAc - Blue square
    def select_add_glcnac_mode(self):
        self.mode = "Add GlcNAc Node"

    # GlcN - Blue crossed square
    def select_add_glcn_mode(self):
        self.mode = "Add GlcN Node"

    # GlcA - Blue divided diamond
    def select_add_glca_mode(self):
        self.mode = "Add GlcA Node"

    # Qui - Blue triangle
    def select_add_qui_mode(self):
        self.mode = "Add Qui Node"

    # QuiNAc - Blue divided triangle
    def select_add_quinac_mode(self):
        self.mode = "Add QuiNAc Node"

    # Oli - Blue rectangle
    def select_add_oli_mode(self):
        self.mode = "Add Oli Node"

    # Bac - Blue hexagon
    def select_add_bac_mode(self):
        self.mode = "Add Bac Node"

    # Api - Blue pentagon
    def select_add_api_mode(self):
        self.mode = "Add Api Node"

    # Man - Green circle
    def select_add_man_mode(self):
        self.mode = "Add Man Node"

    # ManNAc - Green square
    def select_add_mannac_mode(self):
        self.mode = "Add ManNAc Node"

    # ManN - Green crossed square
    def select_add_mann_mode(self):
        self.mode = "Add ManN Node"

    # ManA - Green divided diamond
    def select_add_mana_mode(self):
        self.mode = "Add ManA Node"

    # Rha - Green triangle
    def select_add_rha_mode(self):
        self.mode = "Add Rha Node"

    # RhaNAc - Green divided triangle
    def select_add_rhanac_mode(self):
        self.mode = "Add RhaNAc Node"

    # Tyv - Green rectangle
    def select_add_tyv_mode(self):
        self.mode = "Add Tyv Node"

    # Ara - Green star
    def select_add_ara_mode(self):
        self.mode = "Add Ara Node"

    # Kdn - Green diamond
    def select_add_kdn_mode(self):
        self.mode = "Add Kdn Node"

    # Pse - Green flat diamond
    def select_add_pse_mode(self):
        self.mode = "Add Pse Node"

    # LDManHep - Green hexagon
    def select_add_ldmanhep_mode(self):
        self.mode = "Add LDManHep Node"

    # Fruc - Green pentagon
    def select_add_fruc_mode(self):
        self.mode = "Add Fruc Node"

    # Gal - Yellow circle
    def select_add_gal_mode(self):
        self.mode = "Add Gal Node"

    # GalNAc - Yellow square
    def select_add_galnac_mode(self):
        self.mode = "Add GalNAc Node"

    # GalN - Yellow crossed square
    def select_add_galn_mode(self):
        self.mode = "Add GalN Node"

    # GalA - Yellow divided diamond
    def select_add_gala_mode(self):
        self.mode = "Add GalA Node"

    # Lyx - Yellow star
    def select_add_lyx_mode(self):
        self.mode = "Add Lyx Node"

    # Leg - Yellow flat diamond
    def select_add_leg_mode(self):
        self.mode = "Add Leg Node"

    # Kdo - Yellow hexagon
    def select_add_kdo_mode(self):
        self.mode = "Add Kdo Node"

    # Tag - Yellow pentagon
    def select_add_tag_mode(self):
        self.mode = "Add Tag Node"

    # Gul - Orange circle
    def select_add_gul_mode(self):
        self.mode = "Add Gul Node"

    # GulNAc - Orange square
    def select_add_gulnac_mode(self):
        self.mode = "Add GulNAc Node"

    # GulN - Orange crossed square
    def select_add_guln_mode(self):
        self.mode = "Add GulN Node"

    # GulA - Orange divided diamond
    def select_add_gula_mode(self):
        self.mode = "Add GulA Node"

    # 6dGul - Orange triangle
    def select_add_6dgul_mode(self):
        self.mode = "Add 6dGul Node"

    # Abe - Orange rectangle
    def select_add_abe_mode(self):
        self.mode = "Add Abe Node"

    # Xyl - Orange star
    def select_add_xyl_mode(self):
        self.mode = "Add Xyl Node"

    # Dha - Orange hexagon
    def select_add_dha_mode(self):
        self.mode = "Add Dha Node"

    # Sor - Orange pentagon
    def select_add_sor_mode(self):
        self.mode = "Add Sor Node"

    # Alt - Pink circle
    def select_add_alt_mode(self):
        self.mode = "Add Alt Node"

    # AltNAc - Pink square
    def select_add_altnac_mode(self):
        self.mode = "Add AltNAc Node"

    # AltN - Pink crossed square
    def select_add_altn_mode(self):
        self.mode = "Add AltN Node"

    # AltA - Pink divided diamond
    def select_add_alta_mode(self):
        self.mode = "Add AltA Node"

    # 6dAlt - Pink triangle
    def select_add_6dalt_mode(self):
        self.mode = "Add 6dAlt Node"

    # 6dAltNAc - Pink divided triangle
    def select_add_6daltnac_mode(self):
        self.mode = "Add 6dAltNAc Node"

    # Par - Pink rectangle
    def select_add_par_mode(self):
        self.mode = "Add Par Node"

    # Rib - Pink star
    def select_add_rib_mode(self):
        self.mode = "Add Rib Node"

    # Aci - Pink flat diamond
    def select_add_aci_mode(self):
        self.mode = "Add Aci Node"

    # DDManHep - Pink hexagon
    def select_add_ddmanhep_mode(self):
        self.mode = "Add DDManHep Node"

    # Psi - Pink pentagon
    def select_add_psi_mode(self):
        self.mode = "Add Psi Node"

    # All - Purple circle
    def select_add_all_mode(self):
        self.mode = "Add All Node"

    # AllNAc - Purple square
    def select_add_allnac_mode(self):
        self.mode = "Add AllNAc Node"

    # AllN - Purple crossed square
    def select_add_alln_mode(self):
        self.mode = "Add AllN Node"

    # AllA - Purple divided diamond
    def select_add_alla_mode(self):
        self.mode = "Add AllA Node"

    # Dig - Purple rectangle
    def select_add_dig_mode(self):
        self.mode = "Add Dig Node"

    # Neu5Ac - Purple diamond
    def select_add_neu5ac_mode(self):
        self.mode = "Add Neu5Ac Node"

    # MurNAc - Purple hexagon
    def select_add_murnac_mode(self):
        self.mode = "Add MurNAc Node"

    # Tal - Light Blue circle
    def select_add_tal_mode(self):
        self.mode = "Add Tal Node"

    # TalNAc - Light Blue square
    def select_add_talnac_mode(self):
        self.mode = "Add TalNAc Node"

    # TalN - Light Blue crossed square
    def select_add_taln_mode(self):
        self.mode = "Add TalN Node"

    # TalA - Light Blue divided diamond
    def select_add_tala_mode(self):
        self.mode = "Add TalA Node"

    # 6dTal - Light Blue triangle
    def select_add_6dtal_mode(self):
        self.mode = "Add 6dTal Node"

    # 6dTalNAc - Light Blue diided triangle
    def select_add_6dtalnac_mode(self):
        self.mode = "Add 6dTalNAc Node"

    # Col - Light Blue rectangle
    def select_add_col_mode(self):
        self.mode = "Add Col Node"

    # Neu5Gc - Light Blue diamond
    def select_add_neu5gc_mode(self):
        self.mode = "Add Neu5Gc Node"

    # 4eLeg - Light Blue flat diamond
    def select_add_4eleg_mode(self):
        self.mode = "Add 4eLeg Node"

    # MurNGc - Light Blue hexagon
    def select_add_murngc_mode(self):
        self.mode = "Add MurNGc Node"

    # Ido - Brown circle
    def select_add_ido_mode(self):
        self.mode = "Add Ido Node"

    # IdoNAc - Brown square
    def select_add_idonac_mode(self):
        self.mode = "Add IdoNAc Node"

    # IdoN - Brown crossed square
    def select_add_idon_mode(self):
        self.mode = "Add IdoN Node"

    # IdoA - Brown divided diamond
    def select_add_idoa_mode(self):
        self.mode = "Add IdoA Node"

    # Neu - Brown diamond
    def select_add_neu_mode(self):
        self.mode = "Add Neu Node"

    # Mur - Brown hexagon
    def select_add_mur_mode(self):
        self.mode = "Add Mur Node"

    # Fuc - Red triangle
    def select_add_fuc_mode(self):
        self.mode = "Add Fuc Node"

    # FucNAc - Red divided triangle
    def select_add_fucnac_mode(self):
        self.mode = "Add FucNAc Node"

    # Sia - Red diamond
    def select_add_sia_mode(self):
        self.mode = "Add Sia Node"

    # Remove and edge mode selection

    def select_rm_circle_mode(self):
        """Switch to Remove Circle mode."""
        self.mode = "Remove Circle"

    def select_rm_edge_mode(self):
        """Switch to Remove Edge mode."""
        self.mode = "Remove Edge"

    # Category 1 -----------------------------------------------------------


    def select_add_a1to2_mode(self):
        """Switch to Add A1to2 mode."""
        self.mode = "Add A1to2"

    def select_add_a1to3_mode(self):
        """Switch to Add A1to3 mode."""
        self.mode = "Add A1to3"

    def select_add_a1to4_mode(self):
        """Switch to Add A1to4 mode."""
        self.mode = "Add A1to4"

    def select_add_a1to5_mode(self):
        """Switch to Add A1to5 mode."""
        self.mode = "Add A1to5"

    def select_add_a1to6_mode(self):
        """Switch to Add A1to6 mode."""
        self.mode = "Add A1to6"

    def select_add_a1to7_mode(self):
        """Switch to Add A1to7 mode."""
        self.mode = "Add A1to7"

    def select_add_a1to9_mode(self):
        """Switch to Add A1to9 mode."""
        self.mode = "Add A1to9"



    # Category 2 -----------------------------------------------------------
    def select_add_a2to3_mode(self):
        """Switch to Add A2to3 mode."""
        self.mode = "Add A2to3"

    def select_add_a2to5_mode(self):
        """Switch to Add A2to5 mode."""
        self.mode = "Add A2to5"

    def select_add_a2to6_mode(self):
        """Switch to Add A2to6 mode."""
        self.mode = "Add A2to6"

    def select_add_a2to7_mode(self):
        """Switch to Add A2to7 mode."""
        self.mode = "Add A2to7"

    def select_add_a2to8_mode(self):
        """Switch to Add A2to8 mode."""
        self.mode = "Add A2to8"


    # Category 3 -----------------------------------------------------------
    def select_add_b1to2_mode(self):
        """Switch to Add B1to2 mode."""
        self.mode = "Add B1to2"

    def select_add_b1to3_mode(self):
        """Switch to Add B1to3 mode."""
        self.mode = "Add B1to3"

    def select_add_b1to4_mode(self):
        """Switch to Add B1to4 mode."""
        self.mode = "Add B1to4"

    def select_add_b1to5_mode(self):
        """Switch to Add B1to5 mode."""
        self.mode = "Add B1to5"

    def select_add_b1to6_mode(self):
        """Switch to Add B1to6 mode."""
        self.mode = "Add B1to6"

    def select_add_b1to7_mode(self):
        """Switch to Add B1to7 mode."""
        self.mode = "Add B1to7"

    def select_add_b1to8_mode(self):
        """Switch to Add B1to8 mode."""
        self.mode = "Add B1to8"

    def select_add_b1to9_mode(self):
        """Switch to Add B1to9 mode."""
        self.mode = "Add B1to9"

    # Remove Elements

    def select_rm_edge_text_mode(self):
        """Switch to Remove Edge text mode."""
        self.mode = "Remove Edge Text"

    def handle_click(self, event):
        """Handle click events for adding vertices or starting edges."""
        x, y = event.x, event.y

        # Check for sugar modes

        # TODO: Add all other nodes
        # Glc - Blue circle
        if self.mode == "Add Glc Node":
            add_vertex(self, x, y, self.add_glc_node)

        # GlcNAc - Blue square
        elif self.mode == "Add GlcNAc Node":
            add_vertex(self, x, y, self.add_glcnac_node)

        # GlcN - Blue crossed square
        elif self.mode == "Add GlcN Node":
            add_vertex(self, x, y, self.add_glcn_node)

        # GlcA - Blue divided diamond
        elif self.mode == "Add GlcA Node":
            add_vertex(self, x, y, self.add_glca_node)

        # Qui - Blue triangle
        elif self.mode == "Add Qui Node":
            add_vertex(self, x, y, self.add_qui_node)

        # QuiNAc - Blue divided triangle
        elif self.mode == "Add QuiNAc Node":
            add_vertex(self, x, y, self.add_quinac_node)

        # Oli - Blue rectangle
        elif self.mode == "Add Oli Node":
            add_vertex(self, x, y, self.add_oli_node)

        # Bac - Blue hexagon
        elif self.mode == "Add Bac Node":
            add_vertex(self, x, y, self.add_bac_node)

        # Api - Blue pentagon
        elif self.mode == "Add Api Node":
            add_vertex(self, x, y, self.add_api_node)

        # Man - Green circle
        elif self.mode == "Add Man Node":
            add_vertex(self, x, y, self.add_man_node)

        # ManNAc - Green square
        elif self.mode == "Add ManNAc Node":
            add_vertex(self, x, y, self.add_mannac_node)

        # ManN - Green crossed square
        elif self.mode == "Add ManN Node":
            add_vertex(self, x, y, self.add_mann_node)

        # ManA - Green divided diamond
        elif self.mode == "Add ManA Node":
            add_vertex(self, x, y, self.add_mana_node)

        # Rha - Green triangle
        elif self.mode == "Add Rha Node":
            add_vertex(self, x, y, self.add_rha_node)

        # RhaNAc - Green divided triangle
        elif self.mode == "Add RhaNAc Node":
            add_vertex(self, x, y, self.add_rhanac_node)

        # Tyv - Green rectangle
        elif self.mode == "Add Tyv Node":
            add_vertex(self, x, y, self.add_tyv_node)

        # Ara - Green star
        elif self.mode == "Add Ara Node":
            add_vertex(self, x, y, self.add_ara_node)

        # Kdn - Green diamond
        elif self.mode == "Add Kdn Node":
            add_vertex(self, x, y, self.add_kdn_node)

        # Pse - Green flat diamond
        elif self.mode == "Add Pse Node":
            add_vertex(self, x, y, self.add_pse_node)

        # LDManHep - Green hexagon
        elif self.mode == "Add LDManHep Node":
            add_vertex(self, x, y, self.add_ldmanhep_node)

        # Fruc - Green pentagon
        elif self.mode == "Add Fruc Node":
            add_vertex(self, x, y, self.add_fruc_node)

        # Gal - Yellow circle
        elif self.mode == "Add Gal Node":
            add_vertex(self, x, y, self.add_gal_node)

        # GalNAc - Yellow square
        elif self.mode == "Add GalNAc Node":
            add_vertex(self, x, y, self.add_galnac_node)

        # GalN - Yellow crossed square
        elif self.mode == "Add GalN Node":
            add_vertex(self, x, y, self.add_galn_node)

        # GalA - Yellow divided diamond
        elif self.mode == "Add GalA Node":
            add_vertex(self, x, y, self.add_gala_node)

        # Lyx - Yellow star
        elif self.mode == "Add Lyx Node":
            add_vertex(self, x, y, self.add_lyx_node)

        # Leg - Yellow flat diamond
        elif self.mode == "Add Leg Node":
            add_vertex(self, x, y, self.add_leg_node)

        # Kdo - Yellow hexagon
        elif self.mode == "Add Kdo Node":
            add_vertex(self, x, y, self.add_kdo_node)

        # Tag - Yellow pentagon
        elif self.mode == "Add Tag Node":
            add_vertex(self, x, y, self.add_tag_node)

        # Gul - Orange circle
        elif self.mode == "Add Gul Node":
            add_vertex(self, x, y, self.add_gul_node)

        # GulNAc - Orange square
        elif self.mode == "Add GulNAc Node":
            add_vertex(self, x, y, self.add_gulnac_node)

        # GulN - Orange crossed square
        elif self.mode == "Add GulN Node":
            add_vertex(self, x, y, self.add_guln_node)

        # GulA - Orange divided diamond
        elif self.mode == "Add GulA Node":
            add_vertex(self, x, y, self.add_gula_node)

        # 6dGul - Orange triangle
        elif self.mode == "Add 6dGul Node":
            add_vertex(self, x, y, self.add_6dgul_node)

        # Abe - Orange rectangle
        elif self.mode == "Add Abe Node":
            add_vertex(self, x, y, self.add_abe_node)

        # Xyl - Orange star
        elif self.mode == "Add Xyl Node":
            add_vertex(self, x, y, self.add_xyl_node)

        # Dha - Orange hexagon
        elif self.mode == "Add Dha Node":
            add_vertex(self, x, y, self.add_dha_node)

        # Sor - Orange pentagon
        elif self.mode == "Add Sor Node":
            add_vertex(self, x, y, self.add_sor_node)

        # Alt - Pink circle
        elif self.mode == "Add Alt Node":
            add_vertex(self, x, y, self.add_alt_node)

        # AltNAc - Pink square
        elif self.mode == "Add AltNAc Node":
            add_vertex(self, x, y, self.add_altnac_node)

        # AltN - Pink crossed square
        elif self.mode == "Add AltN Node":
            add_vertex(self, x, y, self.add_altn_node)

        # AltA - Pink divided diamond
        elif self.mode == "Add AltA Node":
            add_vertex(self, x, y, self.add_alta_node)

        # 6dAlt - Pink triangle
        elif self.mode == "Add 6dAlt Node":
            add_vertex(self, x, y, self.add_6dalt_node)

        # 6dAltNAc - Pink divided triangle
        elif self.mode == "Add 6dAltNAc Node":
            add_vertex(self, x, y, self.add_6daltnac_node)

        # Par - Pink rectangle
        elif self.mode == "Add Par Node":
            add_vertex(self, x, y, self.add_par_node)

        # Rib - Pink star
        elif self.mode == "Add Rib Node":
            add_vertex(self, x, y, self.add_rib_node)

        # Aci - Pink flat diamond
        elif self.mode == "Add Aci Node":
            add_vertex(self, x, y, self.add_aci_node)

        # DDManHep - Pink hexagon
        elif self.mode == "Add DDManHep Node":
            add_vertex(self, x, y, self.add_ddmanhep_node)

        # Psi - Pink pentagon
        elif self.mode == "Add Psi Node":
            add_vertex(self, x, y, self.add_psi_node)

        # All - Purple circle
        elif self.mode == "Add All Node":
            add_vertex(self, x, y, self.add_all_node)

        # AllNAc - Purple square
        elif self.mode == "Add AllNAc Node":
            add_vertex(self, x, y, self.add_allnac_node)

        # AllN - Purple crossed square
        elif self.mode == "Add AllN Node":
            add_vertex(self, x, y, self.add_alln_node)

        # AllA - Purple divided diamond
        elif self.mode == "Add AllA Node":
            add_vertex(self, x, y, self.add_alla_node)

        # Dig - Purple rectangle
        elif self.mode == "Add Dig Node":
            add_vertex(self, x, y, self.add_dig_node)

        # Neu5Ac - Purple diamond
        elif self.mode == "Add Neu5Ac Node":
            add_vertex(self, x, y, self.add_neu5ac_node)

        # MurNAc - Purple hexagon
        elif self.mode == "Add MurNAc Node":
            add_vertex(self, x, y, self.add_murnac_node)

        # Tal - Light Blue circle
        elif self.mode == "Add Tal Node":
            add_vertex(self, x, y, self.add_tal_node)

        # TalNAc - Light Blue square
        elif self.mode == "Add TalNAc Node":
            add_vertex(self, x, y, self.add_talnac_node)

        # TalN - Light Blue crossed square
        elif self.mode == "Add TalN Node":
            add_vertex(self, x, y, self.add_taln_node)

        # TalA - Light Blue divided diamond
        elif self.mode == "Add TalA Node":
            add_vertex(self, x, y, self.add_tala_node)

        # 6dTal - Light Blue triangle
        elif self.mode == "Add 6dTal Node":
            add_vertex(self, x, y, self.add_6dtal_node)

        # 6dTalNAc - Light Blue divided triangle
        elif self.mode == "Add 6dTalNAc Node":
            add_vertex(self, x, y, self.add_6dtalnac_node)

        # Col - Light Blue rectangle
        elif self.mode == "Add Col Node":
            add_vertex(self, x, y, self.add_col_node)

        # Neu5Gc - Light Blue diamond
        elif self.mode == "Add Neu5Gc Node":
            add_vertex(self, x, y, self.add_neu5gc_node)

        # 4eLeg - Light Blue flat diamond
        elif self.mode == "Add 4eLeg Node":
            add_vertex(self, x, y, self.add_4eleg_node)

        # MurNGc - Light Blue hexagon
        elif self.mode == "Add MurNGc Node":
            add_vertex(self, x, y, self.add_murngc_node)

        # Ido - Brown circle
        elif self.mode == "Add Ido Node":
            add_vertex(self, x, y, self.add_ido_node)

        # IdoNAc - Brown square
        elif self.mode == "Add IdoNAc Node":
            add_vertex(self, x, y, self.add_idonac_node)

        # IdoN - Brown crossed square
        elif self.mode == "Add IdoN Node":
            add_vertex(self, x, y, self.add_idon_node)

        # IdoA - Brown divided diamond
        elif self.mode == "Add IdoA Node":
            add_vertex(self, x, y, self.add_idoa_node)

        # Neu - Brown diamond
        elif self.mode == "Add Neu Node":
            add_vertex(self, x, y, self.add_neu_node)

        # Mur - Brown hexagon
        elif self.mode == "Add Mur Node":
            add_vertex(self, x, y, self.add_mur_node)

        # Fuc - Red triangle
        elif self.mode == "Add Fuc Node":
            # if user attempts to add a Fuc node to the first level AND the first sugar has already been placed,
            if x in range (60, 91) and self.first_circle_placed == True:
                # then print a message and do not add a fuc node
                print("Base node Fucosylations MUST be placed at the 2nd level explicitly!")
            else:
                add_vertex(self, x, y, self.add_fuc_node)

        # FucNAc - Red divided triangle
        elif self.mode == "Add FucNAc Node":
            add_vertex(self, x, y, self.add_fucnac_node)

        # Sia - Red diamond
        elif self.mode == "Add Sia Node":
            add_vertex(self, x, y, self.add_sia_node)

    # Check for linkage modes
        # Category 1 ---------------------------
        elif self.mode == "Add A1to2":
            add_edge(self, x, y, self.add_a1to2)

        elif self.mode == "Add A1to3":
            add_edge(self, x, y, self.add_a1to3)

        elif self.mode == "Add A1to4":
            add_edge(self, x, y, self.add_a1to4)

        elif self.mode == "Add A1to5":
            add_edge(self, x, y, self.add_a1to5)

        elif self.mode == "Add A1to6":
            add_edge(self, x, y, self.add_a1to6)

        elif self.mode == "Add A1to7":
            add_edge(self, x, y, self.add_a1to7)

        elif self.mode == "Add A1to9":
            add_edge(self, x, y, self.add_a1to9)

        # Category 2 ---------------------------
        elif self.mode == "Add A2to3":
            add_edge(self, x, y, self.add_a2to3)

        elif self.mode == "Add A2to5":
            add_edge(self, x, y, self.add_a2to5)

        elif self.mode == "Add A2to6":
            add_edge(self, x, y, self.add_a2to6)

        elif self.mode == "Add A2to7":
            add_edge(self, x, y, self.add_a2to7)

        elif self.mode == "Add A2to8":
            add_edge(self, x, y, self.add_a2to8)

        # Category 3 ---------------------------
        elif self.mode == "Add B1to2":
            add_edge(self, x, y, self.add_b1to2)

        elif self.mode == "Add B1to3":
            add_edge(self, x, y, self.add_b1to3)

        elif self.mode == "Add B1to4":
            add_edge(self, x, y, self.add_b1to4)

        elif self.mode == "Add B1to5":
            add_edge(self, x, y, self.add_b1to5)

        elif self.mode == "Add B1to6":
            add_edge(self, x, y, self.add_b1to6)

        elif self.mode == "Add B1to7":
            add_edge(self, x, y, self.add_b1to7)

        elif self.mode == "Add B1to8":
            add_edge(self, x, y, self.add_b1to8)

        elif self.mode == "Add B1to9":
            add_edge(self, x, y, self.add_b1to9)


        # Check for removal modes
        elif self.mode == "Remove Circle":
            # Check if a circle exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.circles:
                self.canvas.delete(item)
                # print(self.circles[item])
                self.vertices.remove(self.circles[item])
                del self.circles[item]

        elif self.mode == "Remove Edge":
            # Check if an edge exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.edges:
                self.canvas.delete(item)
                del self.edges[item]

        elif self.mode == "Remove Edge Text":
            # Check if text exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.edge_text:
                self.canvas.delete(item)
                del self.edge_text[item]



    # Sugars _______________________________________________________________

    # TODO: Define all other sugar add node functions
    # Glc - Blue circle
    def add_glc_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'blue', 'Glc')

    # GlcNAc - Blue square
    def add_glcnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'blue', 'GlcNAc')

    # GlcN - Blue crossed square
    def add_glcn_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'blue', 'GlcN')

    # GlcA - Blue divided diamond
    def add_glca_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'blue', 'GlcA')

    # Qui - Blue triangle
    def add_qui_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'blue', 'Qui')

    # QuiNAc - Blue divided triangle
    def add_quinac_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided triangle', 'blue', 'QuiNAc')

    # Oli - Blue rectangle
    def add_oli_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'blue', 'Oli')

    # Bac - Blue hexagon
    def add_bac_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'blue', 'Bac')

    # Api - Blue pentagon
    def add_api_node(self, x, y):
        add_polygon_shape(self, x, y, 'pentagon', 'blue', 'Api')

    # Man - Green circle
    def add_man_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'green', 'Man')

    # ManNAc - Green square
    def add_mannac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'green', 'ManNAc')

    # ManN - Green crossed square
    def add_mann_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'green', 'ManN')

    # ManA - Green divided diamond
    def add_mana_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'green', 'ManA')

    # Rha - Green triangle
    def add_rha_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'green', 'Rha')

    # RhaNAc - Green divided triangle
    def add_rhanac_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided triangle', 'green', 'RhaNAc')

    # Tyv - Green rectangle
    def add_tyv_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'green', 'Tyv')

    # Ara - Green star
    def add_ara_node(self, x, y):
        add_polygon_shape(self, x, y, 'star', 'green', 'Ara')

    # Kdn - Green diamond
    def add_kdn_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'green', 'Kdn')

    # Pse - Green flat diamond
    def add_pse_node(self, x, y):
        add_polygon_shape(self, x, y, 'flat diamond', 'green', 'Pse')

    # LDManHep - Green hexagon
    def add_ldmanhep_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'green', 'LDManHep')

    # Fruc - Green pentagon
    def add_fruc_node(self, x, y):
        add_polygon_shape(self, x, y, 'pentagon', 'green', 'Fruc')

    # Gal - Yellow circle
    def add_gal_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'yellow', 'Gal')

    # GalNAc - Yellow square
    def add_galnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'yellow', 'GalNAc')

    # GalN - Yellow crossed square
    def add_galn_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'yellow', 'GalN')

    # GalA - Yellow divided diamond
    def add_gala_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'yellow', 'GalA')

    # Lyx - Yellow star
    def add_lyx_node(self, x, y):
        add_polygon_shape(self, x, y, 'star', 'yellow', 'Lyx')

    # Leg - Yellow flat diamond
    def add_leg_node(self, x, y):
        add_polygon_shape(self, x, y, 'flat diamond', 'yellow', 'Leg')

    # Kdo - Yellow hexagon
    def add_kdo_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'yellow', 'Kdo')

    # Tag - Yellow pentagon
    def add_tag_node(self, x, y):
        add_polygon_shape(self, x, y, 'pentagon', 'yellow', 'Tag')

    # Gul - Orange circle
    def add_gul_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'orange', 'Gul')

    # GulNAc - Orange square
    def add_gulnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'orange', 'GulNAc')

    # GulN - Orange crossed square
    def add_guln_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'orange', 'GulN')

    # GulA - Orange divided diamond
    def add_gula_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'orange', 'GulA')

    # 6dGul - Orange triangle
    def add_6dgul_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'orange', '6dGul')

    # Abe - Orange rectangle
    def add_abe_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'orange', 'Abe')

    # Xyl - Orange star
    def add_xyl_node(self, x, y):
        add_polygon_shape(self, x, y, 'star', 'orange', 'Xyl')

    # Dha - Orange hexagon
    def add_dha_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'orange', 'Dha')

    # Sor - Orange pentagon
    def add_sor_node(self, x, y):
        add_polygon_shape(self, x, y, 'pentagon', 'orange', 'Sor')

    # Alt - Pink circle
    def add_alt_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'pink', 'Alt')

    # AltNAc - Pink square
    def add_altnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'pink', 'AltNAc')

    # AltN - Pink crossed square
    def add_altn_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'pink', 'AltN')

    # AltA - Pink divided diamond
    def add_alta_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'pink', 'AltA')

    # 6dAlt - Pink triangle
    def add_6dalt_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'pink', '6dAlt')

    # 6dAltNAc - Pink divided triangle
    def add_6daltnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided triangle', 'pink', '6dAltNAc')

    # Par - Pink rectangle
    def add_par_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'pink', 'Par')

    # Rib - Pink star
    def add_rib_node(self, x, y):
        add_polygon_shape(self, x, y, 'star', 'pink', 'Rib')

    # Aci - Pink flat diamond
    def add_aci_node(self, x, y):
        add_polygon_shape(self, x, y, 'flat diamond', 'pink', 'Aci')

    # DDManHep - Pink hexagon
    def add_ddmanhep_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'pink', 'DDManHep')

    # Psi - Pink pentagon
    def add_psi_node(self, x, y):
        add_polygon_shape(self, x, y, 'pentagon', 'pink', 'Psi')

    # All - Purple circle
    def add_all_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'purple', 'All')

    # AllNAc - Purple square
    def add_allnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'purple', 'AllNAc')

    # AllN - Purple crossed square
    def add_alln_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'purple', 'AllN')

    # AllA - Purple divided diamond
    def add_alla_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'purple', 'AllA')

    # Dig - Purple rectangle
    def add_dig_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'purple', 'Dig')

    # Neu5Ac - Purple diamond
    def add_neu5ac_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'purple', 'Neu5Ac')

    # MurNAc - Purple hexagon
    def add_murnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'purple', 'MurNAc')

    # Tal - Light Blue circle
    def add_tal_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'skyblue', 'Tal')

    # TalNAc - Light Blue square
    def add_talnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'skyblue', 'TalNAc')

    # TalN - Light Blue crossed square
    def add_taln_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', 'skyblue', 'TalN')

    # TalA - Light Blue divided diamond
    def add_tala_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', 'skyblue', 'TalA')

    # 6dTal - Light Blue triangle
    def add_6dtal_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'skyblue', '6dTal')

    # 6dTalNAc - Light Blue divided triangle
    def add_6dtalnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided triangle', 'skyblue', '6dTalNAc')

    # Col - Light Blue rectangle
    def add_col_node(self, x, y):
        add_polygon_shape(self, x, y, 'rectangle', 'skyblue', 'Col')

    # Neu5Gc - Light Blue diamond
    def add_neu5gc_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'skyblue', 'Neu5Gc')

    # 4eLeg - Light Blue flat diamond
    def add_4eleg_node(self, x, y):
        add_polygon_shape(self, x, y, 'flat diamond', 'skyblue', '4eLeg')

    # MurNGc - Light Blue hexagon
    def add_murngc_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', 'skyblue', 'MurNGc')

    # Ido - Brown circle
    def add_ido_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', '#A07A4D', 'Ido')

    # IdoNAc - Brown square
    def add_idonac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', '#A07A4D', 'IdoNAc')

    # IdoN - Brown crossed square
    def add_idon_node(self, x, y):
        add_polygon_shape(self, x, y, 'crossed square', '#A07A4D', 'IdoN')

    # IdoA - Brown divided diamond
    def add_idoa_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided diamond', '#A07A4D', 'IdoA')

    # Neu - Brown diamond
    def add_neu_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', '#A07A4D', 'Neu')

    # Mur - Brown hexagon
    def add_mur_node(self, x, y):
        add_polygon_shape(self, x, y, 'hexagon', '#A07A4D', 'Mur')

    # Fuc - Red triangle
    def add_fuc_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'red', 'Fuc')

    # FucNAc - Red divided triangle
    def add_fucnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'divided triangle', 'red', 'FucNAc')

    # Sia - Red diamond
    def add_sia_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'red', 'Sia')

    # Linkages _______________________________________________________________
    # Category 1 --------------------------
    # Add α1,2
    def add_a1to2(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,2", "a1to2")

    # Add α1,3
    def add_a1to3(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,3", "a1to3")

    # Add α1,4
    def add_a1to4(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,4", "a1to4")

    # Add α1,5
    def add_a1to5(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,5", "a1to5")

    # Add α1,6
    def add_a1to6(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,6", "a1to6")

    # Add α1,7
    def add_a1to7(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,7", "a1to7")

    # Add α1,9
    def add_a1to9(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,9", "a1to9")

    # Category 2 --------------------------
    def add_a2to3(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α2,3", "a2to3")

    def add_a2to5(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α2,5", "a2to5")

    def add_a2to6(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α2,6", "a2to6")

    def add_a2to7(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α2,7", "a2to7")

    def add_a2to8(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α2,8", "a2to8")

    # Category 3 --------------------------
    # Add ß1,2
    def add_b1to2(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,2", "b1to2")

    # Add ß1,3
    def add_b1to3(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,3", "b1to3")

    # Add ß1,4
    def add_b1to4(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,4", "b1to4")

    # Add ß1,5
    def add_b1to5(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,5", "b1to5")

    # Add ß1,6
    def add_b1to6(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,6", "b1to6")

    # Add ß1,7
    def add_b1to7(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,7", "b1to7")

    # Add ß1,8
    def add_b1to8(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,8", "b1to8")

    # Add ß1,9
    def add_b1to9(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,9", "b1to9")


    def find_node_degrees(self, edges):
        """Computes the degree of each node in the graph."""
        graph = {}
        for edge in edges.values():
            a, b = edge[0], edge[1]
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []
            graph[a].append(b)
            graph[b].append(a)

        return {node: len(neighbors) for node, neighbors in graph.items()}

    # Find Paths to Base Node ___________________________________________________________

    def find_paths_to_base(self, edges):
        # Step 1: Extract all nodes and find the base node
        #   Original:
        # nodes = set()
        # for edge in edges.values():
        #     nodes.update(edge)
        # base_node = min(nodes, key=lambda p: p[0])  # Node with lowest x-coordinate

        # Updated to ignore strings at third position
        nodes = set()

        for edge in edges.values():  # Loop through the edges
            for node in edge:
                # Ensure we only add nodes where the first two elements are numeric
                if isinstance(node[0], (int, float)) and isinstance(node[1], (int, float)):
                    nodes.add((node[0], node[1]))  # Add the (x, y) tuple without the string

        # Find the node with the lowest x-coordinate
        base_node = min(nodes, key=lambda p: p[0])  # Node with the lowest x-coordinate

        # Step 2: Build adjacency list
        graph = {node: [] for node in nodes}
        for edge in edges.values():
            a, b = edge[0], edge[1]
            graph[a].append(b)
            graph[b].append(a)

        # Step 3: BFS to find shortest paths to base node
        paths = {"A": {"path": [], "steps to base node": 0,
                       "degree_counts": {"2nd": 0, "3rd": 0, "4th": 0}}}  # Base node entry
        queue = deque([(base_node, [base_node])])
        visited = {base_node}

        key_label = iter("BCDEFGHIJKLMNOPQRSTUVWXYZ")
        key_map = {}

        # Get node_degrees
        node_degrees = self.find_node_degrees(edges)

        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    # print("Printing new_path variable: ", new_path)
                    # print("Steps to base node of new_path: ", len(new_path) - 1)

                    # Increment node degrees based on whether each node in node_degrees is in new_path
                    second_degree_counter = 0
                    third_degree_counter = 0
                    fourth_degree_counter = 0

                    # Loop over keys
                    for key in node_degrees:
                        # print("Printing key label: ", key)
                        # print("Printing value label: ", value)
                        #                     print("Printing value at key label: ", node_degrees[key])
                        degree_for_node = node_degrees[key]
                        #                     print("Printing node_degrees: ", node_degrees)
                        # Check if key is in this node's path, but not including the node itself (exclude last index)
                        if key in new_path[:-1]:
                            # Increment the correct n-degree counter
                            if degree_for_node == 2:
                                second_degree_counter += 1
                                # print("Incrementing second degree counter: ", second_degree_counter)
                            if degree_for_node == 3:
                                third_degree_counter += 1
                            if degree_for_node == 4:
                                fourth_degree_counter += 1

                    key = next(key_label)
                    key_map[key] = {"path": new_path, "steps to base node": len(new_path) - 1, "degree_counts": {
                        "2nd": second_degree_counter,
                        "3rd": third_degree_counter,
                        "4th": fourth_degree_counter}
                                    }
                    queue.append((neighbor, new_path))

        paths.update(key_map)
        return paths

    # Calculate DC Matrix ___________________________________________________________

    def calculate_dci(self, paths):
        node_table = PrettyTable()
        node_table.field_names = ["Node",
                                  "Steps to Base Node",
                                  "2ndDeg Nodes\u2E4B * 2",
                                  "3rdDeg Nodes\u2E4B * 3",
                                  "4thDeg Nodes\u2E4B * 4",
                                  "Node Score"]

        # Extract information from paths dictionary and append that into the node_table_rows list
        #   Keep track of dci_score
        dci_score = 0

        # export data as prettytable and csv
        df = pd.DataFrame(columns=(['Node',
                                    'Steps to Base Node',
                                    '2ndDeg Nodes*2',
                                    '3rdDeg Nodes*3',
                                    '4thDeg Nodes*4',
                                    'Node Score',]))
        # print("Printing df before adding rows: ", df)
        # input("Press Enter to continue...")
        for path in paths:
            row = []
            # print("Node:", path, "Path: ", paths[path]["path"], "Steps: ", paths[path]["steps to base node"], "2ndDeg Nodes: ", paths[path]["degree_counts"]["2nd"])
            # Use syntax above to get information from each path
            row.append(path)  # Path letter symbol

            steps_to_base = paths[path]["steps to base node"]
            row.append(steps_to_base)  # Steps to base node

            num_2nd_weighted = paths[path]["degree_counts"]["2nd"] * 2
            row.append(num_2nd_weighted)  # Number of second degree nodes * Weight of 2

            num_3rd_weighted = paths[path]["degree_counts"]["3rd"] * 3
            row.append(num_3rd_weighted)  # Number of third degree nodes * Weight of 3

            num_4th_weighted = paths[path]["degree_counts"]["4th"] * 4
            row.append(num_4th_weighted)  # Number of fourth degree nodes * Weight of 4

            node_score = sum(row[1:5])
            row.append(node_score)

            # Increment dci_score for each node (i.e., for each row in this table)
            dci_score += row[5]

            # Add row to node_table prettytable
            node_table.add_row(row)

            # Add row to DataFrame
            new_row_df = pd.DataFrame({'Node': path,
                                       'Steps to Base Node': [steps_to_base],
                                       '2ndDeg Nodes*2': [num_2nd_weighted],
                                       '3rdDeg Nodes*3': [num_3rd_weighted],
                                       '4thDeg Nodes*4': [num_4th_weighted],
                                       'Node Score': [node_score]
                                       })
            df = pd.concat([df, new_row_df], ignore_index=True)

        # Print completed, pretty table
        # print("Printing df after concat: ", df)
        print("\nPrinting Distance & Connectivity Matrix for Structure:")
        print(node_table,
              "\n\u2E4BExcluding the degree of the node in question. Weights equal node degree.")

        # Calculate dci_score by summing all node scores in node_table
        print("\nDistance & Connectivity Index"
              "\n(DCI Score): ", dci_score)

        # print("Printing circles: ", self.circles)
        # print("Printing edges: ", self.edges)

        # FIXME: export dci matrix as csv

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                 initialfile="DCI_Matrix.csv",)
        if file_path:
            df.to_csv(file_path, index=False)

    # Calculate PC Matrix ___________________________________________________________

    def calculate_pci(self, circles, edges):

        # Step 1: Sort nodes by x-coordinate to determine layers
        sorted_nodes = sorted(circles.items(), key=lambda x: x[1][0])  # Sort by x-coordinate
        layers = {}
        current_layer = 1
        last_x = None

        # print("Printing circles and edges")
        # print("Circles:", circles)
        # print("Edges:", edges)
        # input("Press Enter to continue...\n")

        for node_id, (x, y, color) in sorted_nodes:
            if x != last_x:
                layers[current_layer] = [node_id]
                current_layer += 1
                last_x = x
            else:
                layers[current_layer - 1].append(node_id)

        # Step 2: Initialize storage for derived values
        results = defaultdict(dict)

        # print("Printing Results dict: ", results)

        # Step 3: Compute derived values for each layer
        for layer_num, node_ids in layers.items():
            # Layer: Layer Number
            results[layer_num]['Layer'] = 'L' + str(layer_num)

            # FIXME: Count unique sugar codes, not colors
            # NMT: Count unique colors
            node_colors = {circles[node_id][2] for node_id in node_ids}
            NMT = len(node_colors)
            results[layer_num]['NMT'] = NMT
            # print("Printing Node_colors dict: ", node_colors)
            # print("Printing node_ids dict: ", node_ids, "Printing node_ids type: ", type(node_ids))

            # input("\nPress Enter to continue to TNU...")

            # TNU: Total number of nodes in the layer
            TNU = len(node_ids)
            results[layer_num]['TNU'] = TNU

            # NEL: Count inter-layer linkages
            NEL = 0
            edge_types = set()

            # NLT: Count distinct edge types
            for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
                # print("Edge ID: ", edge_id)
                # print("Nodes in Edge: ", (x1, y1), (x2, y2), edge_type)

                # If any edge in the edges_dict touches the node based on its node_id, increment NEL
                # if (x1, y1) == circles[node_id]

                for node_id in node_ids:
                    # print("Printing circles[node_id]: ", circles[node_id])
                    # print("Printing circles[node_id][0]: ", circles[node_id][0], "Printing circles[node_id][1]: ", circles[node_id][1])

                    if (x1 == circles[node_id][0] and y1 == circles[node_id][1]) or (
                            x2 == circles[node_id][0] and y2 == circles[node_id][1]):
                        NEL += 1
                        edge_types.add(edge_type)

                #
                # nodes_in_edge = {x1, x2}
                # nodes_in_layer = set(node_ids)
                # # print("\nPrinting edge types dict: ", edge_type)
                # # print("Printing nodes dict: ", nodes_in_edge)
                # # print("Printing nodes in layer: ", nodes_in_layer)
                #
                # # If the edge connects nodes from the current layer to another layer
                # if nodes_in_edge & nodes_in_layer:
                #     # Count inter-layer linkages
                #     if (nodes_in_edge & nodes_in_layer) != nodes_in_layer:
                #         NEL += 1
                #
                #     # Track edge types for NLT
                #     edge_types.add(edge_type)

            results[layer_num]['NEL'] = NEL

            NLT = len(edge_types)

            results[layer_num]['NLT'] = NLT

            # print("Printing Edge_colors dict: ", edge_types)

            # print("Layer ", layer_num)
            # input("Press Enter to begin NCDSPL calculation\n")
            # NCDSPL: Count nodes connecting to different colored nodes in the previous layer
            NCDSPL = 0
            if layer_num > 1:
                previous_layer_nodes = layers[layer_num - 1]
                # print("previous_layer_nodes:", previous_layer_nodes)
                for node_id in node_ids:
                    # print("Printing node color of node in this layer:", circles[node_id][2])
                    # Get colors of all nodes in layers
                    node_color = circles[node_id][2]
                    for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
                        # Loop over previous layer nodes
                        for previous_node_id in previous_layer_nodes:
                            # If the previous node and the current node are connected by an edge (check x and y values),
                            # then if their colors are different, increment NCDSPL
                            # print("Previous Node ID: ", previous_node_id)
                            # print("circles[previous_node_id]:", circles[previous_node_id])
                            #
                            if ((circles[previous_node_id][0] == x1 and circles[previous_node_id][1] == y1) and (
                                    circles[node_id][0] == x2 and circles[node_id][1] == y2)) or \
                                    ((circles[previous_node_id][0] == x2 and circles[previous_node_id][1] == y2) and (
                                            circles[node_id][0] == x1 and circles[node_id][1] == y1)):
                                if circles[previous_node_id][2] != circles[node_id][2]:
                                    NCDSPL += 1

            results[layer_num]['NCDSPL'] = NCDSPL

            # Add layer score
            results[layer_num]['Layer Score'] = NMT + TNU + NEL + NLT + NCDSPL

        pci_score = 0

        table = PrettyTable()
        table.field_names = ["Layer", "NMT", "TNU", "NEL", "NLT", "NCDSPL", "Layer Score"]

        # Populate table rows
        for layer, values in sorted(results.items()):  # Ensure sorted layer order
            layer_score_value = values.get("Layer Score", 0)
            pci_score += layer_score_value  # Add to total sum

            table.add_row([
                layer,
                values.get("NMT", ""),
                values.get("TNU", ""),
                values.get("NEL", ""),
                values.get("NLT", ""),
                values.get("NCDSPL", ""),
                layer_score_value
            ])



        print("\n\nPrinting Position & Composition Matrix for Structure:")
        print(table)

        print("NMT: Number of Monosaccharide Types; TNU: Total Number of Units; "
              "NEL: Number of Inter-layer Linkages; NLT: Number of Linkage Types (NLT); "
              "NCDSPL: Number of Monomers Connected to a Different Species in the Previous Layer")

        print("\nPosition & Composition Index "
              "\n(PCI Score): ", pci_score)

        # Export results dict to a pandas df, then the df to csv
        df = pd.DataFrame.from_dict(results, orient='index')

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                 initialfile="PCI_Matrix.csv", )
        if file_path:
            df.to_csv(file_path, index=False)



        return results

    def select_calc_dci_mode(self):
        """Switch to Calculate DCI mode."""
        self.mode = "Calculate DCI"
        paths = self.find_paths_to_base(self.edges)
        self.calculate_dci(paths)

    def select_calc_pci_mode(self):
        """Switch to Calculate PCI mode."""
        self.mode = "Calculate PCI"
        self.calculate_pci(self.circles, self.edges)

    def undo(self):
        if self.undo_stack:
            last_item = self.undo_stack.pop()
            self.canvas.delete(last_item)

    def select_export_image_mode(self):
        """Switch to Export Image mode."""
        self.mode = "Export Image"
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        # image = ImageGrab.grab(bbox=(x, y, x1, y1))
        image = ImageGrab.grab(bbox=(40, 500, 1880, 1080))

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image.save(file_path)



# Create the main window and run the application
def main():
    root = tk.Tk()
    app = GridApplication(root)
    root.mainloop()

if __name__ == "__main__":

    main()
