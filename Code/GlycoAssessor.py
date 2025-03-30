import tkinter as tk
import math
import os
import sys
from collections import deque, defaultdict
from PIL import ImageGrab
from prettytable import PrettyTable
from tkinter import filedialog
import pandas as pd



# Define the class to redirect print() output to a Text widget
class PrintToText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # Insert text at the end of the widget
        self.text_widget.yview(tk.END)  # Scroll to the end to show the new text

    def flush(self):
        pass  # This is required to avoid errors, but we don’t need it for this purpose


# Define the main application class
class GridApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("GlycoAssessor")

        # # Original Canvas widget
        self.canvas = tk.Canvas(self.master, width=1800, height=550, bg='#2B2D30') # Uncomment for large UI
        # # self.canvas = tk.Canvas(self.master, width=600, height=600, bg='#1E1F22')  # Uncomment for small UI
        self.canvas.pack()



        # Grid size
        self.grid_size = 30
        self.vertices = []  # List to store the centers of circles

        # Dictionaries to store edges and circles
        self.edges = {}  # List to store edges
        self.circles = {}  # Dictionary to store circle items
        self.edge_text = {} # Dict to store edge text (linkage type labels)


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


        # Create frames for the three columns
        #   Column 1 has buttons for nodes and edges
        column_1 = tk.Frame(self.master)
        column_1.pack(side="left", padx=20, pady=10, anchor="n")

        #   Column 2 has buttons to calculate DCI, PCI, and Reset the program
        column_2 = tk.Frame(self.master)
        column_2.pack(side="left", padx=20, pady=10, anchor="n")

        #   Column 3 displays the text output
        column_3 = tk.Frame(self.master)
        column_3.pack(side="left", padx=20, pady=10, anchor="n")

        column_4 = tk.Frame(self.master)
        column_4.pack(side="left", padx=20, pady=10, anchor="n")

        # Buttons for mode selection
        # FIXME: Edit "Circle" Button to account for up to 6 different Node types
        # Initialize row 1 in column 1
        button_r1_c1 = tk.Frame(column_1)
        button_r1_c1.pack(pady=1, anchor="w")  # Aligns row to the left

        # Add "Sugar Menu" text to row 1
        tk.Label(button_r1_c1, text="Sugar Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        # Add buttons to row 2



        # Initialize row 2 in column 1
        button_r2_c1 = tk.Frame(column_1)
        button_r2_c1.pack(pady=1, anchor="w")

        # Blue square - #24A5A2
        self.add_blue_circle_button = tk.Button(button_r2_c1, text="Add Blue Square",
                                                command=self.select_add_blue_circle_mode, background="blue",
                                                foreground="#1E1F22")
        self.add_blue_circle_button.pack(side="left", padx=5)


        # Add buttons to row 3

        # Initialize Row 3 in column 1
        button_r3_c1 = tk.Frame(column_1)
        button_r3_c1.pack(pady=1, anchor="w")

        # Green circle - #7BB23C
        self.add_green_circle_button = tk.Button(button_r3_c1, text="Add Green Circle",
                                                 command=self.select_add_green_circle_mode, background="green",
                                                 foreground="#1E1F22")
        self.add_green_circle_button.pack(side="left", padx=5)


        # Add buttons to row 4

        # Initialize row 4 in column 1
        button_r4_c1 = tk.Frame(column_1)
        button_r4_c1.pack(pady=1, anchor="w")

        #  Yellow - #8B741A
        self.add_yellow_circle_button = tk.Button(button_r4_c1, text="Add Yellow Circle",
                                                  command=self.select_add_yellow_circle_mode, background="yellow",
                                                  foreground="#1E1F22")
        self.add_yellow_circle_button.pack(side="left", padx=5)

        # Add buttons to row 5
        button_r5_c1 = tk.Frame(column_1)
        button_r5_c1.pack(pady=1, anchor="w")
        # Red triangle - #AA4926
        # (treat as a circle; specific for Fucose/fucosylation)
        self.add_red_circle_button = tk.Button(button_r5_c1, text="Add Red Triangle",
                                               command=self.select_add_red_circle_mode, background="red",
                                               foreground="#1E1F22")
        self.add_red_circle_button.pack(side="left", padx=5)


        # Add buttons to row 6
        button_r6_c1 = tk.Frame(column_1)
        button_r6_c1.pack(pady=1, anchor="w")

        # Purple diamond - #92548A
        self.add_purple_circle_button = tk.Button(button_r6_c1, text="Add Purple Diamond",
                                                  command=self.select_add_purple_circle_mode, background="purple",
                                                  foreground="#1E1F22")
        self.add_purple_circle_button.pack(side="left", padx=5)


        # Add buttons to row 7
        button_r7_c1 = tk.Frame(column_1)
        button_r7_c1.pack(pady=1, anchor="w")

        # Skyblue circle - #CB8B6B
        self.add_skyblue_circle_button = tk.Button(button_r7_c1, text="Add Skyblue Square",
                                                  command=self.select_add_skyblue_circle_mode, background="skyblue",
                                                  foreground="#1E1F22")
        self.add_skyblue_circle_button.pack(side="left", padx=5)

        button_r8_c1 = tk.Frame(column_1)
        button_r8_c1.pack(pady=1, anchor="w")

        self.rm_circle_button = tk.Button(button_r8_c1, text="Remove Node", command=self.select_rm_circle_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.rm_circle_button.pack(side="left", padx=5)



        # Create Linkage Menu
        # Initialize row 1 in column 2
        button_r1_c2 = tk.Frame(column_2)
        button_r1_c2.pack(pady=1, anchor="w")

        # Add buttons to row 1, column 2
        tk.Label(button_r1_c2, text="Linkage Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        # Add buttons to row 2, column 2
        # Initialize row 2 in column 2
        button_r2_c2 = tk.Frame(column_2)
        button_r2_c2.pack(pady=1, anchor="w")
        self.add_a1to2_button = tk.Button(button_r2_c2, text="Add α1,2", command=self.select_add_a1to2_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to2_button.pack(side="left", padx=5)

        # FIXME: Add buttons for various types of inter-layer linkage edges
        #  (e.g., α1,2, α1,3, α1,4, α1,6, ß1,2, ß1,4)
        button_r3_c2 = tk.Frame(column_2)
        button_r3_c2.pack(pady=1, anchor="w")

        self.add_a1to3_button = tk.Button(button_r3_c2, text="Add α1,3", command=self.select_add_a1to3_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to3_button.pack(side="left", padx=5)

        button_r4_c2 = tk.Frame(column_2)
        button_r4_c2.pack(pady=1, anchor="w")

        self.add_a1to4_button = tk.Button(button_r4_c2, text="Add α1,4", command=self.select_add_a1to4_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to4_button.pack(side="left", padx=5)

        button_r5_c2 = tk.Frame(column_2)
        button_r5_c2.pack(pady=1, anchor="w")

        self.add_a1to6_button = tk.Button(button_r5_c2, text="Add α1,6", command=self.select_add_a1to6_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to6_button.pack(side="left", padx=5)

        button_r6_c2 = tk.Frame(column_2)
        button_r6_c2.pack(pady=1, anchor="w")

        # FIXME: add ß1,2, ß1,3, ß1,4, ß1,6
        self.add_b1to2_button = tk.Button(button_r6_c2, text="Add ß1,2", command=self.select_add_b1to2_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to2_button.pack(side="left", padx=5)

        button_r7_c2 = tk.Frame(column_2)
        button_r7_c2.pack(pady=1, anchor="w")

        self.add_b1to3_button = tk.Button(button_r7_c2, text="Add ß1,3", command=self.select_add_b1to3_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to3_button.pack(side="left", padx=5)

        button_r8_c2 = tk.Frame(column_2)
        button_r8_c2.pack(pady=1, anchor="w")


        self.add_b1to4_button = tk.Button(button_r8_c2, text="Add ß1,4", command=self.select_add_b1to4_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to4_button.pack(side="left", padx=5)

        button_r9_c2 = tk.Frame(column_2)
        button_r9_c2.pack(pady=1, anchor="w")

        self.add_b1to6_button = tk.Button(button_r9_c2, text="Add ß1,6", command=self.select_add_b1to6_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to6_button.pack(side="left", padx=5)



        button_r10_c2 = tk.Frame(column_2)
        button_r10_c2.pack(pady=1, anchor="w")

        self.rm_edge_button = tk.Button(button_r10_c2, text="Remove Edge", command=self.select_rm_edge_mode,
                                        background="#2B2D30", foreground="#DFE1E5")
        self.rm_edge_button.pack(side="left", padx=5)

        button_r11_c2 = tk.Frame(column_2)
        button_r11_c2.pack(pady=1, anchor="w")

        self.rm_edge_text_button = tk.Button(button_r11_c2, text="Remove Edge Text",
                                             command=self.select_rm_edge_text_mode,
                                             background="#2B2D30", foreground="#DFE1E5")
        self.rm_edge_text_button.pack(side="left", padx=5)


        # Initialize column 3
        # Initialize row 1, column 3


        button_r1_c3 = tk.Frame(column_3)
        button_r1_c3.pack(pady=1, anchor="w")

        tk.Label(button_r1_c3, text="Analysis Tools", font=("Arial", 12, "bold"), bg='lightgray').pack()

        button_r2_c3 = tk.Frame(column_3)
        button_r2_c3.pack(pady=1, anchor="w")
        # Export image
        self.dci_calc_button = tk.Button(button_r2_c3, text="Export Image", command=self.select_export_image_mode,
                                         background="#2B2D30", foreground="#DFE1E5")
        self.dci_calc_button.pack(side="left", padx=5)

        button_r3_c3 = tk.Frame(column_3)
        button_r3_c3.pack(pady=1, anchor="w")

        # Button to calculate DCI
        self.dci_calc_button = tk.Button(button_r3_c3, text="Calculate DCI", command=self.select_calc_dci_mode,
                                         background="#639F52", foreground="#1E1F22")
        self.dci_calc_button.pack(side="left", padx=5)

        button_r4_c3 = tk.Frame(column_3)
        button_r4_c3.pack(pady=1, anchor="w")

        # Button to calculate PCI
        self.pci_calc_button = tk.Button(button_r4_c3, text="Calculate PCI", command=self.select_calc_pci_mode,
                                         background="#639F52", foreground="#1E1F22")
        self.pci_calc_button.pack(side="left", padx=5)

        # button_r5_c3 = tk.Frame(column_3)
        # button_r5_c3.pack(pady=1, anchor="w")
        # # Button to reset program
        # self.reset_button = tk.Button(button_r5_c3, text="Reset Program", command=self.reset_program, background="#AA4926", foreground="#DFE1E5")
        # self.reset_button.pack(side="left", padx=5)





        # Initialize row 1 in column 4
        button_r1_c4 = tk.Frame(column_4)
        button_r1_c4.pack(pady=1, anchor="w")
        tk.Label(button_r1_c4, text="Instructions and Log", font=("Arial", 12, "bold"), bg='lightgray').pack()

        button_r2_c4 = tk.Frame(column_4)
        button_r2_c4.pack(pady=1, anchor="w")

        # Create a Text widget for printing output
        self.text_area = tk.Text(button_r2_c4, height=100, width=200)
        self.text_area.pack(side="right",padx=1, pady=0)


        # Redirect print() to the Text widget
        printer = PrintToText(self.text_area)
        sys.stdout = printer

        print("Instructions:"
              "\nSelect a sugar type from the Sugar Menu, "
              "then click on the left side of the grid to place the base node."
              "\nPlacement of subsequent nodes is restricted to specific points. "
              "\nSelect a linkage type from "
              "the Linkage Menu and then click on two sugar nodes to connect them with the linkage."
              "\nOrient the N-glycan with the base node at the left and the furthest node on the right.")

        print("\nSee video tutorial at this link: https://youtu.be/TVWvqSvYwtQ")

        print("\nAssumptions:"
              "\n1) The leftmost node you add is the base node of the N-glycan. "
              "\n2) You will not attempt to duplicate edges."
              "\n3) You will only draw edges between two adjacent nodes."
              "\n4) You must place base-node Fucosylations at the 2nd level explicitly.\n")


        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.handle_click)  # Left click to place vertices or start edge

    def draw_grid(self):
        """Draw the grid lines on the canvas."""
        for i in range(0, 1800, self.grid_size):
            self.canvas.create_line(i, 0, i, 1800, fill="#545557", tags="grid")
            self.canvas.create_line(0, i, 1800, i, fill="#545557", tags="grid")

    # Modes to add circles
    def select_add_circle_mode(self):
        """Switch to Add Circle mode."""
        self.mode = "Add Circle"

    def select_add_blue_circle_mode(self):
        """Switch to Add Blue Node mode."""
        self.mode = "Add Blue Node"

    def select_add_green_circle_mode(self):
        """Switch to Add Green Node mode."""
        self.mode = "Add Green Node"

    def select_add_purple_circle_mode(self):
        """Switch to Add purple Node mode."""
        self.mode = "Add Purple Node"

    def select_add_skyblue_circle_mode(self):
        """Switch to Add skyblue Node mode."""
        self.mode = "Add skyblue Node"

    def select_add_yellow_circle_mode(self):
        """Switch to Add yellow Node mode."""
        self.mode = "Add Yellow Node"

    def select_add_red_circle_mode(self):
        """Switch to Add red Node mode."""
        self.mode = "Add Red Node"

    def select_rm_circle_mode(self):
        """Switch to Remove Circle mode."""
        self.mode = "Remove Circle"

    def select_rm_edge_mode(self):
        """Switch to Remove Edge mode."""
        self.mode = "Remove Edge"

    def select_add_a1to2_mode(self):
        """Switch to Add A1to2 mode."""
        self.mode = "Add A1to2"

    def select_add_a1to3_mode(self):
        """Switch to Add A1to3 mode."""
        self.mode = "Add A1to3"

    def select_add_a1to4_mode(self):
        """Switch to Add A1to4 mode."""
        self.mode = "Add A1to4"

    def select_add_a1to6_mode(self):
        """Switch to Add A1to6 mode."""
        self.mode = "Add A1to6"

    def select_add_b1to2_mode(self):
        """Switch to Add B1to2 mode."""
        self.mode = "Add B1to2"

    def select_add_b1to3_mode(self):
        """Switch to Add B1to3 mode."""
        self.mode = "Add B1to3"

    def select_add_b1to4_mode(self):
        """Switch to Add B1to4 mode."""
        self.mode = "Add B1to4"

    def select_add_b1to6_mode(self):
        """Switch to Add B1to6 mode."""
        self.mode = "Add B1to6"

    def select_rm_edge_text_mode(self):
        """Switch to Remove Edge text mode."""
        self.mode = "Remove Edge Text"

    def handle_click(self, event):
        """Handle click events for adding vertices or starting edges."""
        x, y = event.x, event.y

        # Check the current mode
        if self.mode == "Add Circle":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_vertex(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_vertex(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click

        # FIXME: NOTE: This is experimental code to try integrating the existing circle/vertex code with colors
        elif self.mode == "Add Blue Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_blue_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_blue_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click

        elif self.mode == "Add Green Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_green_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_green_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click


        elif self.mode == "Add Purple Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_purple_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_purple_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click

        elif self.mode == "Add skyblue Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_skyblue_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_skyblue_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click


        elif self.mode == "Add Yellow Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_yellow_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_yellow_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click


        elif self.mode == "Add Red Node":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_red_node(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
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
                            self.add_red_node(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click


        elif self.mode == "Add A1to2":
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
                    self.add_a1to2(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add A1to3":
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
                    self.add_a1to3(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add A1to4":
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
                    self.add_a1to4(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add A1to6":
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
                    self.add_a1to6(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add B1to2":
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
                    self.add_b1to2(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")


        elif self.mode == "Add B1to3":
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
                    self.add_b1to3(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add B1to4":
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
                    self.add_b1to4(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Add B1to6":
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
                    self.add_b1to6(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Remove Circle":
            # Check if a circle exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.circles:
                self.canvas.delete(item)
                # print(self.circles[item])
                self.vertices.remove(self.circles[item])
                del self.circles[item]

                # print("\nPrinting vertices:",self.vertices)

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


    def add_vertex(self, x, y):
        """Add a vertex and draw a white node."""
        color = "#DFE1E5"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw blue circle with radius = 2 * vertex radius
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline=color, tags="circle" #, width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    # FIXME: add all colored nodes
    def add_blue_node(self, x, y):
        """Add a vertex and draw a blue node."""
        color = "blue"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw blue circle with radius = 2 * vertex radius
        circle = self.canvas.create_rectangle(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags="blue_node" #, width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    def add_green_node(self, x, y):
        """Add a vertex and draw a green node."""
        color = "green"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw green circle with radius = 2 * vertex radius
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags="green_node"  # , width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    def add_purple_node(self, x, y):
        """Add a vertex and draw a purple node."""
        color = "purple"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw purple circle with radius = 2 * vertex radius
        circle = self.canvas.create_polygon(
            x, y-40, x + 40, y, x, y + 40, x-40, y,
            fill=color, outline="black", width=5, tags="purple_node"  # , width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    def add_red_node(self, x, y):
        """Add a vertex and draw a red node."""
        color = "red"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw red circle with radius = 2 * vertex radius
        circle = self.canvas.create_polygon(
            x - 2*radius, y + 2*radius, x , y-2*radius, x + 2*radius, y + 2*radius,
            fill=color, outline="black", width=5, tags="red_node"  # , width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    def add_skyblue_node(self, x, y):
        """Add a vertex and draw a skyblue node."""
        color = "skyblue"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw skyblue circle with radius = 2 * vertex radius
        circle = self.canvas.create_rectangle(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags="skyblue_node"  # , width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)

    def add_yellow_node(self, x, y):
        """Add a vertex and draw a yellow node."""
        color = "yellow"
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw purple circle with radius = 2 * vertex radius
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill=color, outline="black", width=5, tags="purple_node"  # , width=10
        )
        self.circles[circle] = (x, y, color)
        # print(self.circles)



    # FIXME: experimental code to add an α1,2 edge
    def add_a1to2(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "α1,2"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="a1to2"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "a1to2")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    # FIXME: add code to add an α1,3 edge
    def add_a1to3(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "α1,3"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="a1to3"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "a1to3")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    # FIXME: experimental code to add an α1,4 edge
    def add_a1to4(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "α1,4"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="a1to4"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "a1to4")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    # FIXME: experimental code to add an α1,6 edge
    def add_a1to6(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "α1,6"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="a1to6"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "a1to6")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    # FIXME: experimental code to add an ß1,2 edge
    def add_b1to2(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "ß1,2"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="b1to2"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "b1to2")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)


    def add_b1to3(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "ß1,3"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="b1to3"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "b1to3")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    # FIXME: experimental code to add an ß1,4 edge
    def add_b1to4(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "ß1,4"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="b1to4"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "b1to4")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)

    def add_b1to6(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge_label = "ß1,6"
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="black", capstyle=tk.ROUND, tags="b1to6"
        )
        edge_text = self.canvas.create_text(
            (vertex1[0] + vertex2[0])/2, (vertex1[1] + vertex2[1])/2, text=edge_label, fill="#DFE1E5",anchor=tk.N,)
        self.edges[edge] = (vertex1, vertex2, "b1to6")
        self.edge_text[edge_text] = edge_label
        # print(self.edges)



    # def reset_program(self):
    #     self.master.destroy()  # Destroy the current Tkinter root
    #     python = sys.executable  # Get the Python executable path
    #     os.execl(sys.executable, sys.executable, *sys.argv)

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
        print("\nPrinting Weighted Matrix for Structure:")
        print(node_table,
              "\n\u2E4BExcluding the degree of the node in question. Weights equal node degree.")

        # Calculate dci_score by summing all node scores in node_table
        print("Distance & Connectivity Index (DCI Score): ", dci_score)

        # print("Printing circles: ", self.circles)
        # print("Printing edges: ", self.edges)

        # FIXME: export dci matrix as csv

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                 initialfile="DCI_Matrix.csv",)
        if file_path:
            df.to_csv(file_path, index=False)

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



        print("\nPrinting PCI Matrix for Structure:")
        print(table)

        print("Position & Composition Index (PCI Score): ", pci_score)

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

    def select_export_image_mode(self):
        """Switch to Export Image mode."""
        self.mode = "Export Image"
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab(bbox=(x, y, x1, y1))
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
