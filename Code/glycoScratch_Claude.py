# 092526 Update — refactored for maintainability (see notes at bottom of file)

import tkinter as tk
import re
import math
import sys
import os
from collections import deque, defaultdict
from PIL import ImageGrab, Image, ImageTk
from prettytable import PrettyTable
from tkinter import filedialog
import pandas as pd

# TODO (remaining, not addressed by this pass — see notes at end of file)
# 2. Make the canvas area larger and the actual structure smaller
# 4. Low priority: edit colors
# 5. Add the PC Index and DC Index to the filename? Or some other way to retain it
#    that does not mess up the matrix excel files


# =============================================================================
# Sugar catalog — THE place to add a new monomer.
#
# To add a new sugar: add one line below with its code, shape, color, and
# which button row it should appear in (0, 1, or 2). Then drop a PNG named
# "<code>.png" into Assets/Sugars/. Nothing else needs to change — no new
# button-creation code, no new mode method, no new elif branch, no new
# add_X_node method. This is what used to require editing 4 different places.
# =============================================================================
sugar_dict = {
    # code:        shape                        color               row
    "Glc":        {"shape": "circle",           "color": "blue",   "row": 0},
    "GlcNAc":     {"shape": "square",           "color": "blue",   "row": 0},
    "GlcN":       {"shape": "crossed square",   "color": "blue",   "row": 0},
    "GlcA":       {"shape": "divided diamond",  "color": "blue",   "row": 0},
    "Qui":        {"shape": "triangle",         "color": "blue",   "row": 0},
    "QuiNAc":     {"shape": "divided triangle", "color": "blue",   "row": 0},
    "Oli":        {"shape": "rectangle",        "color": "blue",   "row": 0},
    "Bac":        {"shape": "hexagon",          "color": "blue",   "row": 0},
    "Api":        {"shape": "pentagon",         "color": "blue",   "row": 0},

    "Man":        {"shape": "circle",           "color": "green",  "row": 0},
    "ManNAc":     {"shape": "square",           "color": "green",  "row": 0},
    "ManN":       {"shape": "crossed square",   "color": "green",  "row": 0},
    "ManA":       {"shape": "divided diamond",  "color": "green",  "row": 0},
    "Rha":        {"shape": "triangle",         "color": "green",  "row": 0},
    "RhaNAc":     {"shape": "divided triangle", "color": "green",  "row": 0},
    "Tyv":        {"shape": "rectangle",        "color": "green",  "row": 0},
    "Ara":        {"shape": "star",             "color": "green",  "row": 0},
    "Kdn":        {"shape": "diamond",          "color": "green",  "row": 0},
    "Pse":        {"shape": "flat diamond",     "color": "green",  "row": 0},
    "LDManHep":   {"shape": "hexagon",          "color": "green",  "row": 0},
    "Fruc":       {"shape": "pentagon",         "color": "green",  "row": 0},

    "Gal":        {"shape": "circle",           "color": "yellow", "row": 0},
    "GalNAc":     {"shape": "square",           "color": "yellow", "row": 0},
    "GalN":       {"shape": "crossed square",   "color": "yellow", "row": 0},
    "GalA":       {"shape": "divided diamond",  "color": "yellow", "row": 0},

    "Lyx":        {"shape": "star",             "color": "yellow", "row": 1},
    "Leg":        {"shape": "flat diamond",     "color": "yellow", "row": 1},
    "Kdo":        {"shape": "hexagon",          "color": "yellow", "row": 1},
    "Tag":        {"shape": "pentagon",         "color": "yellow", "row": 1},

    "Gul":        {"shape": "circle",           "color": "orange", "row": 1},
    "GulNAc":     {"shape": "square",           "color": "orange", "row": 1},
    "GulN":       {"shape": "crossed square",   "color": "orange", "row": 1},
    "GulA":       {"shape": "divided diamond",  "color": "orange", "row": 1},
    "6dGul":      {"shape": "triangle",         "color": "orange", "row": 1},
    "Abe":        {"shape": "rectangle",        "color": "orange", "row": 1},
    "Xyl":        {"shape": "star",             "color": "orange", "row": 1},
    "Dha":        {"shape": "hexagon",          "color": "orange", "row": 1},
    "Sor":        {"shape": "pentagon",         "color": "orange", "row": 1},

    "Alt":        {"shape": "circle",           "color": "pink",   "row": 1},
    "AltNAc":     {"shape": "square",           "color": "pink",   "row": 1},
    "AltN":       {"shape": "crossed square",   "color": "pink",   "row": 1},
    "AltA":       {"shape": "divided diamond",  "color": "pink",   "row": 1},
    "6dAlt":      {"shape": "triangle",         "color": "pink",   "row": 1},
    "6dAltNAc":   {"shape": "divided triangle", "color": "pink",   "row": 1},
    "Par":        {"shape": "rectangle",        "color": "pink",   "row": 1},
    "Rib":        {"shape": "star",             "color": "pink",   "row": 1},
    "Aci":        {"shape": "flat diamond",     "color": "pink",   "row": 1},
    "DDManHep":   {"shape": "hexagon",          "color": "pink",   "row": 1},
    "Psi":        {"shape": "pentagon",         "color": "pink",   "row": 1},

    "All":        {"shape": "circle",           "color": "purple", "row": 1},

    "AllNAc":     {"shape": "square",           "color": "purple", "row": 2},
    "AllN":       {"shape": "crossed square",   "color": "purple", "row": 2},
    "AllA":       {"shape": "divided diamond",  "color": "purple", "row": 2},
    "Dig":        {"shape": "rectangle",        "color": "purple", "row": 2},
    "Neu5Ac":     {"shape": "diamond",          "color": "purple", "row": 2},
    "MurNAc":     {"shape": "hexagon",          "color": "purple", "row": 2},

    "Tal":        {"shape": "circle",           "color": "skyblue", "row": 2},
    "TalNAc":     {"shape": "square",           "color": "skyblue", "row": 2},
    "TalN":       {"shape": "crossed square",   "color": "skyblue", "row": 2},
    "TalA":       {"shape": "divided diamond",  "color": "skyblue", "row": 2},
    "6dTal":      {"shape": "triangle",         "color": "skyblue", "row": 2},
    "6dTalNAc":   {"shape": "divided triangle", "color": "skyblue", "row": 2},
    "Col":        {"shape": "rectangle",        "color": "skyblue", "row": 2},
    "Neu5Gc":     {"shape": "diamond",          "color": "skyblue", "row": 2},
    "4eLeg":      {"shape": "flat diamond",     "color": "skyblue", "row": 2},
    "MurNGc":     {"shape": "hexagon",          "color": "skyblue", "row": 2},

    "Ido":        {"shape": "circle",           "color": "#A07A4D", "row": 2},
    "IdoNAc":     {"shape": "square",           "color": "#A07A4D", "row": 2},
    "IdoN":       {"shape": "crossed square",   "color": "#A07A4D", "row": 2},
    "IdoA":       {"shape": "divided diamond",  "color": "#A07A4D", "row": 2},
    "Neu":        {"shape": "diamond",          "color": "#A07A4D", "row": 2},
    "Mur":        {"shape": "hexagon",          "color": "#A07A4D", "row": 2},

    "Fuc":        {"shape": "triangle",         "color": "red",     "row": 2},
    "FucNAc":     {"shape": "divided triangle", "color": "red",     "row": 2},
    "Sia":        {"shape": "diamond",          "color": "red",     "row": 2},
    # Add new sugar types below ...
}

# Sugars that need the same shape twist as "AltA"/"IdoA" in divided-diamond
# rendering (white wedge on top instead of bottom). Kept as a set so it's a
# one-line edit instead of a hardcoded string comparison buried in the shape code.
DIVIDED_DIAMOND_TOP_WEDGE = {"AltA", "IdoA"}


# =============================================================================
# Linkage catalog — same idea: one entry per linkage, everything else generic.
# Category is derived from the tag, not hand-checked lists of tag names.
# =============================================================================
LINKAGE_ORDER = [
    "a1to2", "a1to3", "a1to4", "a1to5", "a1to6", "a1to7", "a1to9",
    "a2to3", "a2to5", "a2to6", "a2to7", "a2to8",
    "b1to2", "b1to3", "b1to4", "b1to5", "b1to6", "b1to7", "b1to8", "b1to9",
]

_LINKAGE_TAG_RE = re.compile(r"([ab])(\d+)to(\d+)")


def linkage_label(tag):
    """'a1to2' -> 'α1,2', 'b1to4' -> 'ß1,4' (also the asset filename stem)."""
    m = _LINKAGE_TAG_RE.match(tag)
    greek = "α" if m.group(1) == "a" else "ß"
    return f"{greek}{m.group(2)},{m.group(3)}"


def linkage_color(tag):
    if tag.startswith("a1"):
        return "#F5791F"
    elif tag.startswith("a2"):
        return "#0072BB"
    else:
        return "#01A653"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_path, relative_path)


# =============================================================================
# Canvas primitives (grid/vertex/edge/shape drawing). Unchanged in behavior
# from the original — the duplication problem lived in the GUI wiring above
# these, not here.
# =============================================================================

def add_edge(self, x, y, func):
    """Handle adding edges (black) between two vertices."""
    grid_x = round(x / self.grid_size) * self.grid_size
    grid_y = round(y / self.grid_size) * self.grid_size

    if not self.first_vertex:
        if (grid_x, grid_y) in self.vertices:
            self.first_vertex = (grid_x, grid_y)
        else:
            print("First point must be an existing vertex!")
    else:
        if (grid_x, grid_y) in self.vertices and (grid_x, grid_y) != self.first_vertex:
            func(self.first_vertex, (grid_x, grid_y))
            self.first_vertex = None
        else:
            print("Second point must be an existing vertex and different from the first one!")


def add_linkage_type(self, vertex1, vertex2, type_tag):
    """Draw a colored edge (color/label derived from type_tag) between two vertices."""
    label = linkage_label(type_tag)
    color = linkage_color(type_tag)

    edge = self.canvas.create_line(
        vertex1[0], vertex1[1], vertex2[0], vertex2[1],
        width=5, fill=color, capstyle=tk.ROUND, tags=type_tag
    )
    edge_text = self.canvas.create_text(
        (vertex1[0] + vertex2[0]) / 2, (vertex1[1] + vertex2[1]) / 2,
        text=label, fill="#DFE1E5", anchor=tk.N,
    )
    self.edges[edge] = (vertex1, vertex2, type_tag)
    self.edge_text[edge_text] = label
    self.undo_stack.append(edge)
    self.undo_stack.append(edge_text)


def add_vertex(self, x, y, func):
    """Place vertex in Circle mode."""
    fixed_x = 60
    fixed_y = 240

    grid_x = round(x / self.grid_size) * self.grid_size
    grid_y = round(y / self.grid_size) * self.grid_size

    if not self.first_circle_placed:
        func(fixed_x, fixed_y)
        self.first_circle_placed = True
    else:
        radius = self.grid_size / 2
        for center in self.vertices:
            dx = grid_x - center[0]
            dy = grid_y - center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            required_distance = 8 * radius

            if abs(distance - required_distance) < self.grid_size / 2:
                if grid_x == center[0] or grid_y == center[1]:
                    func(grid_x, grid_y)
                    return


def add_polygon_shape(self, x, y, shape, color, sugar_code):
    """Add a vertex and draw the shape for a sugar node."""
    radius = self.grid_size / 2
    self.vertices.append((x, y))

    if shape == 'circle':
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        self.circles[circle] = (x, y, sugar_code)
        self.undo_stack.append(circle)

    elif shape == 'triangle':
        triangle = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        self.circles[triangle] = (x, y, sugar_code)
        self.undo_stack.append(triangle)

    elif shape == 'diamond':
        diamond = self.canvas.create_polygon(
            x, y - 2 * radius, x + 2 * radius, y, x, y + 2 * radius, x - 2 * radius, y,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        self.circles[diamond] = (x, y, sugar_code)
        self.undo_stack.append(diamond)

    elif shape == 'square':
        square = self.canvas.create_rectangle(
            x - 2 * radius, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        self.circles[square] = (x, y, sugar_code)
        self.undo_stack.append(square)

    elif shape == 'crossed square':
        half = 2 * radius
        crossed_square = self.canvas.create_rectangle(
            x - half, y - half, x + half, y + half,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        cross = self.canvas.create_line(
            x - half, y - half, x + half, y + half, fill="black", width=5, tags=sugar_code
        )
        crossed = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x - 2 * radius, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill='white', outline="black", width=5, tags=sugar_code
        )
        self.circles[crossed_square] = (x, y, sugar_code)
        self.undo_stack.append(crossed_square)
        self.undo_stack.append(cross)
        self.undo_stack.append(crossed)

    elif shape == 'divided diamond':
        points = [x, y - 2 * radius, x + 2 * radius, y, x, y + 2 * radius, x - 2 * radius, y]
        div_diamond = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.canvas.create_line(x - 2 * radius, y, x + 2 * radius, y, fill="black", width=5, tags=sugar_code)

        if sugar_code in DIVIDED_DIAMOND_TOP_WEDGE:
            div2 = self.canvas.create_polygon(
                x - 2 * radius, y, x, y - 2 * radius, x + 2 * radius, y,
                fill='white', outline="black", width=5, tags=sugar_code
            )
        else:
            div2 = self.canvas.create_polygon(
                x - 2 * radius, y, x, y + 2 * radius, x + 2 * radius, y,
                fill='white', outline="black", width=5, tags=sugar_code
            )
        self.circles[div_diamond] = (x, y, sugar_code)
        self.undo_stack.append(div_diamond)
        self.undo_stack.append(div2)

    elif shape == 'divided triangle':
        triangle = self.canvas.create_polygon(
            x - 2 * radius, y + 2 * radius, x, y - 2 * radius, x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        tri2 = self.canvas.create_polygon(
            x, y + 2 * radius, x, y - 2 * radius, x - 2 * radius, y + 2 * radius,
            fill='white', outline="black", width=5, tags=sugar_code
        )
        self.circles[triangle] = (x, y, sugar_code)
        self.undo_stack.append(triangle)
        self.undo_stack.append(tri2)

    elif shape == 'rectangle':
        rectangle = self.canvas.create_rectangle(
            x - 2 * radius, y - 1.2 * radius, x + 2 * radius, y + 1.2 * radius,
            fill=color, outline="black", width=5, tags=sugar_code
        )
        self.circles[rectangle] = (x, y, sugar_code)
        self.undo_stack.append(rectangle)

    elif shape == 'star':
        points = []
        for i in range(10):
            angle = math.pi / 5 * i
            r = 2 * radius if i % 2 == 0 else radius
            points.extend([x + r * math.sin(angle), y - r * math.cos(angle)])
        star = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.circles[star] = (x, y, sugar_code)
        self.undo_stack.append(star)

    elif shape == 'flat diamond':
        points = [x, y - 1.3 * radius, x + 2 * radius, y, x, y + 1.3 * radius, x - 2 * radius, y]
        flat_diamond = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.circles[flat_diamond] = (x, y, sugar_code)
        self.undo_stack.append(flat_diamond)

    elif shape == 'hexagon':
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            points.extend([x + 2 * radius * math.cos(angle), y + 1.5 * radius * math.sin(angle)])
        hexagon = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.circles[hexagon] = (x, y, sugar_code)
        self.undo_stack.append(hexagon)

    elif shape == 'pentagon':
        points = []
        for i in range(5):
            angle = math.radians(72 * i - 90)
            points.extend([x + 2 * radius * math.cos(angle), y + 2 * radius * math.sin(angle)])
        pentagon = self.canvas.create_polygon(points, fill=color, outline="black", width=5, tags=sugar_code)
        self.circles[pentagon] = (x, y, sugar_code)
        self.undo_stack.append(pentagon)


class PrintToText:
    """Redirects print() output to a Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.yview(tk.END)

    def flush(self):
        pass


class GridApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("GlycoAssessor")

        column_0 = tk.Frame(self.master)
        column_0.pack(side="left", padx=10, pady=10, anchor="n")

        self.undo_stack = []
        self.button_images = {}       # keeps PhotoImage refs alive (code/tag -> PhotoImage)
        self.sugar_buttons_dict = {}  # code -> Button, in case future features need to look one up

        # Sugar buttons ______________________________________________________
        tk.Label(column_0, text="Sugar Menu", font=("Arial", 10, "bold"), bg='lightgray').pack(anchor="w", padx=5)

        sugar_rows = [tk.Frame(column_0) for _ in range(3)]
        for row_frame in sugar_rows:
            row_frame.pack(pady=1, anchor="w")

        sugar_button_x = 38
        sugar_button_y = 25  # ~2/3 of the original 38px height, per TODO #1

        for code, info in sugar_dict.items():
            img = Image.open(resource_path(f"Assets/Sugars/{code}.png")).resize((sugar_button_x, sugar_button_y))
            photo = ImageTk.PhotoImage(img)
            self.button_images[code] = photo
            btn = tk.Button(
                sugar_rows[info["row"]], image=photo, borderwidth=0, highlightthickness=0,
                command=lambda c=code: self.select_add_mode(c)
            )
            btn.pack(side="left", padx=5)
            self.sugar_buttons_dict[code] = btn

        # Linkage buttons ______________________________________________________
        linkage_label_frame = tk.Frame(column_0)
        linkage_label_frame.pack(pady=1, anchor="w")
        tk.Label(linkage_label_frame, text="Linkage Menu", font=("Arial", 10, "bold"), bg='lightgray').pack()

        linkage_row_frame = tk.Frame(column_0)
        linkage_row_frame.pack(pady=1, anchor="w")

        linkage_button_size = (33, 24)
        for tag in LINKAGE_ORDER:
            label = linkage_label(tag)
            img = Image.open(resource_path(f"Assets/Button_imgs/{label}.png")).resize(linkage_button_size)
            photo = ImageTk.PhotoImage(img)
            self.button_images[tag] = photo
            btn = tk.Button(
                linkage_row_frame, image=photo, borderwidth=0, highlightthickness=0,
                command=lambda t=tag: self.select_add_linkage_mode(t)
            )
            btn.pack(side="left", padx=5)

        # TODO: Fix the delete buttons!
        tk.Button(linkage_row_frame, text="Remove Edge", command=self.select_rm_edge_mode).pack(side="left", padx=5)
        tk.Button(linkage_row_frame, text="Remove Edge Text", command=self.select_rm_edge_text_mode).pack(side="left", padx=5)
        tk.Button(linkage_row_frame, text="Remove Node", command=self.select_rm_circle_mode).pack(side="left", padx=5)

        # Analysis buttons _____________________________________________________
        analysis_label_frame = tk.Frame(column_0)
        analysis_label_frame.pack(pady=1, anchor="w")
        tk.Label(analysis_label_frame, text="Analysis Tools", font=("Arial", 10, "bold"), bg='lightgray').pack()

        tools_row_frame = tk.Frame(column_0)
        tools_row_frame.pack(pady=1, anchor="w")

        analysis_button_size = (70, 35)

        self.dci_img = Image.open(resource_path("Assets/Button_imgs/dci_img.png")).resize(analysis_button_size)
        self.dci_button_image = ImageTk.PhotoImage(self.dci_img)
        tk.Button(tools_row_frame, image=self.dci_button_image, borderwidth=0, highlightthickness=0,
                  command=self.select_calc_dci_mode).pack(side="left", padx=5)

        self.pci_img = Image.open(resource_path("Assets/Button_imgs/pci_img.png")).resize(analysis_button_size)
        self.pci_button_image = ImageTk.PhotoImage(self.pci_img)
        tk.Button(tools_row_frame, image=self.pci_button_image, borderwidth=0, highlightthickness=0,
                  command=self.select_calc_pci_mode).pack(side="left", padx=5)

        self.export_img = Image.open(resource_path("Assets/Button_imgs/exportImage.png")).resize(analysis_button_size)
        self.export_button_image = ImageTk.PhotoImage(self.export_img)
        tk.Button(tools_row_frame, image=self.export_button_image, borderwidth=0, highlightthickness=0,
                  command=self.select_export_image_mode).pack(side="left", padx=5)

        self.reset_img = Image.open(resource_path("Assets/Button_imgs/reset.png")).resize((35, 35))
        self.reset_button_image = ImageTk.PhotoImage(self.reset_img)
        tk.Button(tools_row_frame, image=self.reset_button_image, borderwidth=0, highlightthickness=0,
                  command=self.reset_app).pack(side="left", padx=5)

        # Canvas _______________________________________________________________
        canvas_frame = tk.Frame(column_0)
        canvas_frame.pack(pady=1, anchor="w")

        self.canvas = tk.Canvas(canvas_frame, width=1920, height=1080, bg='#2B2D30')
        self.canvas.pack()

        self.grid_size = 15
        self.vertices = []
        self.edges = {}
        self.circles = {}
        self.edge_text = {}

        self.first_circle_placed = False
        self.first_vertex = None

        self.mode = None
        self.start_x = None
        self.start_y = None
        self.current_line = None

        self.draw_grid()

        # Instructions and Log _________________________________________________
        tk.Label(tools_row_frame, text="Instructions and Log", font=("Arial", 10, "bold"), bg='lightgray').pack(side="left", padx=5)

        self.text_area = tk.Text(tools_row_frame, height=3, width=200)
        self.text_area.pack(side="left", padx=5)

        sys.stdout = PrintToText(self.text_area)

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

        self.canvas.bind("<Button-1>", self.handle_click)

    # -------------------------------------------------------------------------
    # App-level actions
    # -------------------------------------------------------------------------

    def reset_app(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.vertices = []
        self.edges = {}
        self.circles = {}
        self.edge_text = {}
        self.first_circle_placed = False
        self.first_vertex = None
        self.mode = None
        self.start_x = None
        self.start_y = None
        self.current_line = None
        print("Reset")

    def draw_grid(self):
        """Draw the grid lines on the canvas."""
        radius = 5
        for i in range(0, 1800, self.grid_size):
            self.canvas.create_line(i, 0, i, 1800, fill="#545557", tags="grid")
            self.canvas.create_line(0, i, 1800, i, fill="#545557", tags="grid")

            circle_spacing = 60
            for x in range(0, 1600, circle_spacing):
                for y in range(0, 1600, circle_spacing):
                    self.canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius,
                        fill="#545557", outline="", tags="grid_dot"
                    )
            start_radius = 15
            self.canvas.create_oval(
                circle_spacing - start_radius, 240 - start_radius,
                circle_spacing + start_radius, 240 + start_radius,
                fill="black", outline="", tags="grid_dot"
            )
            self.canvas.create_text(circle_spacing, 240, text="START", fill="white")

    # -------------------------------------------------------------------------
    # Mode selection — generic now: one method per *category* of action,
    # not one method per sugar/linkage.
    # -------------------------------------------------------------------------

    def select_add_mode(self, code):
        self.mode = f"sugar:{code}"

    def select_add_linkage_mode(self, tag):
        self.mode = f"linkage:{tag}"

    def select_rm_circle_mode(self):
        self.mode = "remove:circle"

    def select_rm_edge_mode(self):
        self.mode = "remove:edge"

    def select_rm_edge_text_mode(self):
        self.mode = "remove:edge_text"

    def select_calc_dci_mode(self):
        self.mode = "Calculate DCI"
        paths = self.find_paths_to_base(self.edges)
        self.calculate_dci(paths)

    def select_calc_pci_mode(self):
        self.mode = "Calculate PCI"
        self.calculate_pci(self.circles, self.edges)

    def select_export_image_mode(self):
        self.mode = "Export Image"
        image = ImageGrab.grab(bbox=(40, 500, 1880, 1080))
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image.save(file_path)

    def undo(self):
        if self.undo_stack:
            self.canvas.delete(self.undo_stack.pop())

    # -------------------------------------------------------------------------
    # Click dispatch — was a ~400-line elif chain (one branch per sugar/linkage).
    # Now it's a dispatch on the mode's prefix, with sugar/linkage-specific
    # data pulled from sugar_dict / linkage_label / linkage_color.
    # -------------------------------------------------------------------------

    def handle_click(self, event):
        mode = self.mode
        if not mode:
            return
        x, y = event.x, event.y

        if mode.startswith("sugar:"):
            code = mode.split(":", 1)[1]
            info = sugar_dict[code]
            # Base-node Fucosylation must be placed explicitly at the 2nd level.
            if code == "Fuc" and 60 <= x <= 90 and self.first_circle_placed:
                print("Base node Fucosylations MUST be placed at the 2nd level explicitly!")
                return
            add_vertex(self, x, y, lambda vx, vy: add_polygon_shape(self, vx, vy, info["shape"], info["color"], code))

        elif mode.startswith("linkage:"):
            tag = mode.split(":", 1)[1]
            add_edge(self, x, y, lambda v1, v2: add_linkage_type(self, v1, v2, tag))

        elif mode == "remove:circle":
            item = self.canvas.find_closest(x, y)[0]
            if item in self.circles:
                self.canvas.delete(item)
                self.vertices.remove(self.circles[item])
                del self.circles[item]

        elif mode == "remove:edge":
            item = self.canvas.find_closest(x, y)[0]
            if item in self.edges:
                self.canvas.delete(item)
                del self.edges[item]

        elif mode == "remove:edge_text":
            item = self.canvas.find_closest(x, y)[0]
            if item in self.edge_text:
                self.canvas.delete(item)
                del self.edge_text[item]

    # -------------------------------------------------------------------------
    # Graph analysis (DCI / PCI) — logic unchanged from the original;
    # only the DataFrame construction was changed to avoid O(n^2) pd.concat.
    # -------------------------------------------------------------------------

    def find_node_degrees(self, edges):
        """Computes the degree of each node in the graph."""
        graph = {}
        for edge in edges.values():
            a, b = edge[0], edge[1]
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)
        return {node: len(neighbors) for node, neighbors in graph.items()}

    def find_paths_to_base(self, edges):
        nodes = set()
        for edge in edges.values():
            for node in edge:
                if isinstance(node[0], (int, float)) and isinstance(node[1], (int, float)):
                    nodes.add((node[0], node[1]))

        base_node = min(nodes, key=lambda p: p[0])

        graph = {node: [] for node in nodes}
        for edge in edges.values():
            a, b = edge[0], edge[1]
            graph[a].append(b)
            graph[b].append(a)

        paths = {"A": {"path": [], "steps to base node": 0,
                       "degree_counts": {"2nd": 0, "3rd": 0, "4th": 0}}}
        queue = deque([(base_node, [base_node])])
        visited = {base_node}

        key_label = iter("BCDEFGHIJKLMNOPQRSTUVWXYZ")
        key_map = {}
        node_degrees = self.find_node_degrees(edges)

        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]

                    second_degree_counter = 0
                    third_degree_counter = 0
                    fourth_degree_counter = 0
                    for key, degree_for_node in node_degrees.items():
                        if key in new_path[:-1]:
                            if degree_for_node == 2:
                                second_degree_counter += 1
                            elif degree_for_node == 3:
                                third_degree_counter += 1
                            elif degree_for_node == 4:
                                fourth_degree_counter += 1

                    key = next(key_label)
                    key_map[key] = {
                        "path": new_path,
                        "steps to base node": len(new_path) - 1,
                        "degree_counts": {
                            "2nd": second_degree_counter,
                            "3rd": third_degree_counter,
                            "4th": fourth_degree_counter,
                        },
                    }
                    queue.append((neighbor, new_path))

        paths.update(key_map)
        return paths

    def calculate_dci(self, paths):
        node_table = PrettyTable()
        node_table.field_names = [
            "Node", "Steps to Base Node",
            "2ndDeg Nodes⹋ * 2", "3rdDeg Nodes⹋ * 3", "4thDeg Nodes⹋ * 4",
            "Node Score",
        ]

        rows = []
        dci_score = 0
        for path in paths:
            steps_to_base = paths[path]["steps to base node"]
            num_2nd_weighted = paths[path]["degree_counts"]["2nd"] * 2
            num_3rd_weighted = paths[path]["degree_counts"]["3rd"] * 3
            num_4th_weighted = paths[path]["degree_counts"]["4th"] * 4
            node_score = steps_to_base + num_2nd_weighted + num_3rd_weighted + num_4th_weighted
            dci_score += node_score

            node_table.add_row([path, steps_to_base, num_2nd_weighted, num_3rd_weighted, num_4th_weighted, node_score])
            rows.append({
                'Node': path,
                'Steps to Base Node': steps_to_base,
                '2ndDeg Nodes*2': num_2nd_weighted,
                '3rdDeg Nodes*3': num_3rd_weighted,
                '4thDeg Nodes*4': num_4th_weighted,
                'Node Score': node_score,
            })

        print("\nPrinting Distance & Connectivity Matrix for Structure:")
        print(node_table, "\n⹋Excluding the degree of the node in question. Weights equal node degree.")
        print("\nDistance & Connectivity Index"
              "\n(DCI Score): ", dci_score)

        df = pd.DataFrame(rows)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="DCI_Matrix.csv",
        )
        if file_path:
            df.to_csv(file_path, index=False)

    def calculate_pci(self, circles, edges):
        # Step 1: Sort nodes by x-coordinate to determine layers
        sorted_nodes = sorted(circles.items(), key=lambda x: x[1][0])
        layers = {}
        current_layer = 1
        last_x = None

        for node_id, (x, y, color) in sorted_nodes:
            if x != last_x:
                layers[current_layer] = [node_id]
                current_layer += 1
                last_x = x
            else:
                layers[current_layer - 1].append(node_id)

        results = defaultdict(dict)

        for layer_num, node_ids in layers.items():
            results[layer_num]['Layer'] = 'L' + str(layer_num)

            # NMT: number of distinct monosaccharide types (by sugar code, not color)
            node_types = {circles[node_id][2] for node_id in node_ids}
            NMT = len(node_types)
            results[layer_num]['NMT'] = NMT

            # TNU: total number of nodes in the layer
            TNU = len(node_ids)
            results[layer_num]['TNU'] = TNU

            # NEL / NLT: inter-layer linkages touching this layer, and distinct edge types
            NEL = 0
            edge_types = set()
            for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
                for node_id in node_ids:
                    if (x1 == circles[node_id][0] and y1 == circles[node_id][1]) or \
                       (x2 == circles[node_id][0] and y2 == circles[node_id][1]):
                        NEL += 1
                        edge_types.add(edge_type)

            results[layer_num]['NEL'] = NEL
            results[layer_num]['NLT'] = len(edge_types)

            # NCDSPL: nodes connecting to a different-typed node in the previous layer
            NCDSPL = 0
            if layer_num > 1:
                previous_layer_nodes = layers[layer_num - 1]
                for node_id in node_ids:
                    for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
                        for previous_node_id in previous_layer_nodes:
                            prev_xy = (circles[previous_node_id][0], circles[previous_node_id][1])
                            cur_xy = (circles[node_id][0], circles[node_id][1])
                            if (prev_xy == (x1, y1) and cur_xy == (x2, y2)) or \
                               (prev_xy == (x2, y2) and cur_xy == (x1, y1)):
                                if circles[previous_node_id][2] != circles[node_id][2]:
                                    NCDSPL += 1

            results[layer_num]['NCDSPL'] = NCDSPL
            results[layer_num]['Layer Score'] = NMT + TNU + NEL + len(edge_types) + NCDSPL

        pci_score = 0
        table = PrettyTable()
        table.field_names = ["Layer", "NMT", "TNU", "NEL", "NLT", "NCDSPL", "Layer Score"]

        for layer, values in sorted(results.items()):
            layer_score_value = values.get("Layer Score", 0)
            pci_score += layer_score_value
            table.add_row([
                layer, values.get("NMT", ""), values.get("TNU", ""), values.get("NEL", ""),
                values.get("NLT", ""), values.get("NCDSPL", ""), layer_score_value,
            ])

        print("\n\nPrinting Position & Composition Matrix for Structure:")
        print(table)
        print("NMT: Number of Monosaccharide Types; TNU: Total Number of Units; "
              "NEL: Number of Inter-layer Linkages; NLT: Number of Linkage Types (NLT); "
              "NCDSPL: Number of Monomers Connected to a Different Species in the Previous Layer")
        print("\nPosition & Composition Index "
              "\n(PCI Score): ", pci_score)

        df = pd.DataFrame.from_dict(results, orient='index')
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="PCI_Matrix.csv",
        )
        if file_path:
            df.to_csv(file_path, index=False)

        return results


def main():
    root = tk.Tk()
    app = GridApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# =============================================================================
# What changed and why
# =============================================================================
# 1. TODO #1 (button height): sugar_button_y dropped from 38 -> 25 (~2/3).
#
# 3. TODO #3 (streamlined sugar types) — this was the main rewrite:
#    - `sugar_dict` now drives button creation, mode selection, click
#      handling, and shape/color lookup. Adding a sugar is one dict entry +
#      one PNG named to match the code. Previously it required editing 4
#      separate places (a button block, a select_add_X_mode method, an
#      elif branch in handle_click, and an add_X_node method) — about 60
#      sugars x 4 places = ~240 hand-written blocks, several thousand lines.
#    - Linkages got the same treatment via LINKAGE_ORDER + linkage_label()/
#      linkage_color(), replacing another ~20 buttons x same pattern, plus
#      the long if/elif tag-list checks inside the old add_linkage_type.
#    - self.mode is now a small tagged string ("sugar:Glc", "linkage:a1to2",
#      "remove:circle") instead of ~90 distinct literal strings, so
#      handle_click dispatches on a prefix instead of enumerating every case.
#
# Performance fix (not in the original TODOs, but a real issue):
#    - calculate_dci() built its export DataFrame with pd.concat() inside a
#      per-row loop, which is O(n^2) and explicitly discouraged by pandas.
#      Replaced with collecting plain dict rows and building the DataFrame
#      once at the end.
#
# Not touched (need a design decision, not just cleanup):
#    - TODO #2 (bigger canvas / smaller structure) is a sizing/UX call —
#      happy to do it, just tell me the target canvas size and shape scale.
#    - TODO #4 (colors) explicitly marked low priority.
#    - TODO #5 (encode PCI/DCI index in filename) needs you to decide what
#      value goes in the filename and where it comes from at save time.
