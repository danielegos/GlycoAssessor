import tkinter as tk
import math
import os
import sys
from collections import deque, defaultdict
from PIL import ImageGrab, Image, ImageTk
from prettytable import PrettyTable
from tkinter import filedialog
import pandas as pd
from sympy.codegen.ast import continue_


from Code.Shapes.Edge import add_edge
from Code.Shapes.Linkage import add_linkage_type
from Code.Shapes.Vertex import add_vertex
from Code.Shapes.Polygon import add_polygon_shape
# from Code.Buttons.SugarButton import sugar_module


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


    # Sugar buttons ______________________________________________________________
        self.sugar_buttons_dict = {}

        # Add "Sugar Menu" text to row 1
        tk.Label(button_r0_c0, text="Sugar Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        button_r1_c0 = tk.Frame(column_0)
        button_r1_c0.pack(pady=1, anchor="w")  # Aligns row to the left


        # Add individual sugars in this order:      --------NOTE: About 20 buttons fit horizontally --------
        # Glc - Blue circle

        # GlcNAc - Blue square
        self.glcnac_img = Image.open("../Assets/Sugars/GlcNAc.png").resize((50, 50))
        self.glcnac_button_image = ImageTk.PhotoImage(self.glcnac_img)
        self.add_glcnac_button = tk.Button(button_r1_c0, image=self.glcnac_button_image, borderwidth=0,
                                           highlightthickness=0, command=self.select_add_glcnac_mode)
        self.add_glcnac_button.pack(side="left", padx=5)

        # GlcN - Blue crossed square

        # GlcA - Blue divided diamond

        # Qui - Blue triangle

        # QuiNAc - Blue divided triangle

        # Oli - Blue rectangle

        # Bac - Blue hexagon

        # Api - Blue pentagon

        # Man - Green circle
        self.man_img = Image.open("../Assets/Sugars/Man.png").resize((50, 50))
        self.man_button_image = ImageTk.PhotoImage(self.man_img)
        self.add_man_button = tk.Button(button_r1_c0, image=self.man_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_man_mode)
        self.add_man_button.pack(side="left", padx=5)

        # ManNAc - Green square

        # ManN - Green crossed square

        # ManA - Green divided diamond

        # Rha - Green triangle

        # RhaNAc - Green divided triangle

        # Tyv - Green rectangle

        # Ara - Green star

        # Kdn - Green diamond

        # Pse - Green flat diamond

        # LDManHep - Green hexagon

        # Fruc - Green pentagon

        # Gal - Yellow circle
        self.gal_img = Image.open("../Assets/Sugars/Gal.png").resize((50, 50))
        self.gal_button_image = ImageTk.PhotoImage(self.gal_img)
        self.add_gal_button = tk.Button(button_r1_c0, image=self.gal_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_gal_mode)
        self.add_gal_button.pack(side="left", padx=5)

        # GalNAc - Yellow square

        # GalN - Yellow crossed square

        # GalA - Yellow divided diamond

        # Lyx - Yellow star

        # Leg - Yellow flat diamond

        # Kdo - Yellow hexagon

        # Tag - Yellow pentagon

        # Gul - Orange circle

        # GulNAc - Orange square

        # GulN - Orange crossed square

        # GulA - Orange divided diamond

        # 6dGul - Orange triangle

        # Abe - Orange rectangle

        # Xyl - Orange star

        # Dha - Orange hexagon

        # Sor - Orange pentagon

        # Alt - Pink circle

        # AltNAc - Pink square

        # AltN - Pink crossed square

        # AltA - Pink divided diamond

        # 6dAlt - Pink triangle

        # 6dAltNAc - Pink divided triangle

        # Par - Pink rectangle

        # Rib - Pink star

        # Aci - Pink flat diamond

        # DDManHep - Pink hexagon

        # Psi - Pink pentagon

        # All - Purple circle

        # AllNAc - Purple square

        # AllN - Purple crossed square

        # AllA - Purple divided diamond

        # Dig - Purple rectangle

        # Neu5Ac - Purple diamond
        self.neu5ac_img = Image.open("../Assets/Sugars/Neu5Ac.png").resize((50, 50))
        self.neu5ac_button_image = ImageTk.PhotoImage(self.neu5ac_img)
        self.add_neu5ac_button = tk.Button(button_r1_c0, image=self.neu5ac_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_neu5ac_mode)
        self.add_neu5ac_button.pack(side="left", padx=5)

        # MurNAc - Purple hexagon

        # Tal - Light Blue circle

        # TalNAc - Light Blue square
        self.talnac_img = Image.open("../Assets/Sugars/TalNAc.png").resize((50, 50))
        self.talnac_button_image = ImageTk.PhotoImage(self.talnac_img)
        self.add_talnac_button = tk.Button(button_r1_c0, image=self.talnac_button_image,
                                           borderwidth=0, highlightthickness=0, command=self.select_add_talnac_mode)
        self.add_talnac_button.pack(side="left", padx=5)

        # TalN - Light Blue crossed square

        # TalA - Light Blue divided diamond

        # 6dTal - Light Blue triangle

        # 6dTalNAc - Light Blue diided triangle

        # Col - Light Blue rectangle

        # Neu5Gc - Light Blue diamond

        # 4eLeg - Light Blue flat diamond

        # MurNGc - Light Blue hexagon

        # Ido - Brown circle

        # IdoNAc - Brown square

        # IdoN - Brown crossed square

        # IdoA - Brown divided diamond

        # Neu - Brown diamond

        # Mur - Brown hexagon

        # Fuc - Red triangle
        self.fuc_img = Image.open("../Assets/Sugars/Fuc.png").resize((50, 50))
        self.fuc_button_image = ImageTk.PhotoImage(self.fuc_img)
        self.add_fuc_button = tk.Button(button_r1_c0, image=self.fuc_button_image,
                                        borderwidth=0, highlightthickness=0, command=self.select_add_fuc_mode)
        self.add_fuc_button.pack(side="left", padx=5)

        # FucNAc - Red divided triangle

        # Sia - Red diamond



    # Linkage buttons ____________________________________________________________

        button_r2_0_c0 = tk.Frame(column_0)
        button_r2_0_c0.pack(pady=1, anchor="w")

        tk.Label(button_r2_0_c0, text="Linkage Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        button_r2_1_c0 = tk.Frame(column_0)
        button_r2_1_c0.pack(pady=1, anchor="w")
        self.add_a1to2_button = tk.Button(button_r2_1_c0, text="Add α1,2", command=self.select_add_a1to2_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to2_button.pack(side="left", padx=5)

        self.add_a1to3_button = tk.Button(button_r2_1_c0, text="Add α1,3", command=self.select_add_a1to3_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to3_button.pack(side="left", padx=5)

        self.add_a1to4_button = tk.Button(button_r2_1_c0, text="Add α1,4", command=self.select_add_a1to4_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to4_button.pack(side="left", padx=5)

        self.add_a1to6_button = tk.Button(button_r2_1_c0, text="Add α1,6", command=self.select_add_a1to6_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_a1to6_button.pack(side="left", padx=5)

        self.add_b1to2_button = tk.Button(button_r2_1_c0, text="Add ß1,2", command=self.select_add_b1to2_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to2_button.pack(side="left", padx=5)

        self.add_b1to3_button = tk.Button(button_r2_1_c0, text="Add ß1,3", command=self.select_add_b1to3_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to3_button.pack(side="left", padx=5)

        self.add_b1to4_button = tk.Button(button_r2_1_c0, text="Add ß1,4", command=self.select_add_b1to4_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to4_button.pack(side="left", padx=5)

        self.add_b1to6_button = tk.Button(button_r2_1_c0, text="Add ß1,6", command=self.select_add_b1to6_mode,
                                          background="#2B2D30", foreground="#DFE1E5")
        self.add_b1to6_button.pack(side="left", padx=5)

        # self.rm_edge_button = tk.Button(button_r2_1_c0, text="Remove Edge", command=self.select_rm_edge_mode,
        #                                 background="#2B2D30", foreground="#DFE1E5")
        # self.rm_edge_button.pack(side="left", padx=5)
        #
        # self.rm_edge_text_button = tk.Button(button_r2_1_c0, text="Remove Edge Text",
        #                                      command=self.select_rm_edge_text_mode,
        #                                      background="#2B2D30", foreground="#DFE1E5")
        # self.rm_edge_text_button.pack(side="left", padx=5)
        #
        #
        # self.rm_circle_button = tk.Button(button_r2_1_c0, text="Remove Node", command=self.select_rm_circle_mode,
        #                                   background="#2B2D30", foreground="#DFE1E5")
        # self.rm_circle_button.pack(side="left", padx=5)


    # Analysis buttons ___________________________________________________________

        button_r3_1_c0 = tk.Frame(column_0)
        button_r3_1_c0.pack(pady=1, anchor="w")

        tk.Label(button_r3_1_c0, text="Analysis Tools", font=("Arial", 12, "bold"), bg='lightgray').pack()

        button_r3_c0 = tk.Frame(column_0)
        button_r3_c0.pack(pady=1, anchor="w")


        # Export image
        self.dci_calc_button = tk.Button(button_r3_c0, text="Export Image", command=self.select_export_image_mode,
                                         background="#2B2D30", foreground="#DFE1E5", height = 3)
        self.dci_calc_button.pack(side="left", padx=5)

        # Button to calculate DCI
        self.dci_calc_button = tk.Button(button_r3_c0, text="Calculate DCI", command=self.select_calc_dci_mode,
                                         background="#639F52", foreground="#1E1F22", height = 3)
        self.dci_calc_button.pack(side="left", padx=5)

        # Button to calculate PCI
        self.pci_calc_button = tk.Button(button_r3_c0, text="Calculate PCI", command=self.select_calc_pci_mode,
                                         background="#639F52", foreground="#1E1F22", height = 3)
        self.pci_calc_button.pack(side="left", padx=5)

        # Button to reset the program
        self.reset_button = tk.Button(button_r3_c0, text="Reset", command=self.reset_app,
                                         background="#EC1B25", foreground="black", height = 3)
        self.reset_button.pack(side="left", padx=25)

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

        tk.Label(button_r3_c0, text="Instructions and Log", font=("Arial", 12, "bold"), bg='lightgray').pack()

        # Create a Text widget for printing output
        self.text_area = tk.Text(button_r3_c0, height=5, width=200)
        self.text_area.pack(side="left",padx=5)

        # Redirect print() to the Text widget
        printer = PrintToText(self.text_area)
        sys.stdout = printer

        print("Instructions:"
              "\nSelect a sugar type. Click the left side of the grid to place the base node."
              "\n\nPlacement of subsequent nodes is restricted to specific points."
              "\n\nSelect a linkage type. Click on two sugar nodes to connect them with the linkage."
              "\n\nOrient the N-glycan with the base node at the left and the furthest node on the right.")

        print("\n\nSee video tutorial at this link: https://youtu.be/TVWvqSvYwtQ")

        print("\nAssumptions:"
              "\n1) The leftmost node you add is the base node of the N-glycan. "
              "\n2) You will not attempt to duplicate edges."
              "\n3) You will only draw edges between two adjacent nodes."
              "\n4) You must place base-node Fucosylations at the 2nd level explicitly.\n")


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
    def select_add_6dAltNac_mode(self):
        self.mode = "Add 6dAltNac Node"

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
            add_vertex(self, x, y, self.add_6dAltNAc_node)

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




        elif self.mode == "Add Neu5Ac Node":
            add_vertex(self, x, y, self.add_neu5ac_node)

        elif self.mode == "Add TalNAc Node":
            add_vertex(self, x, y, self.add_talnac_node)

        elif self.mode == "Add Gal Node":
            add_vertex(self, x, y, self.add_gal_node)




    # Check for linkage modes
        elif self.mode == "Add A1to2":
            add_edge(self, x, y, self.add_a1to2)

        elif self.mode == "Add A1to3":
            add_edge(self, x, y, self.add_a1to3)

        elif self.mode == "Add A1to4":
            add_edge(self, x, y, self.add_a1to4)

        elif self.mode == "Add A1to6":
            add_edge(self, x, y, self.add_a1to6)

        elif self.mode == "Add B1to2":
            add_edge(self, x, y, self.add_b1to2)

        elif self.mode == "Add B1to3":
            add_edge(self, x, y, self.add_b1to3)

        elif self.mode == "Add B1to4":
            add_edge(self, x, y, self.add_b1to4)

        elif self.mode == "Add B1to6":
            add_edge(self, x, y, self.add_b1to6)

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

    # GlcA - Blue divided diamond

    # Qui - Blue triangle
    def add_qui_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'blue', 'Qui')

    # QuiNAc - Blue divided triangle

    # Oli - Blue rectangle

    # Bac - Blue hexagon

    # Api - Blue pentagon

    # Man - Green circle
    def add_man_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'green', 'Man')

    # ManNAc - Green square
    def add_mannac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'green', 'ManNAc')

    # ManN - Green crossed square

    # ManA - Green divided diamond

    # Rha - Green triangle
    def add_rha_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'green', 'Rha')

    # RhaNAc - Green divided triangle

    # Tyv - Green rectangle

    # Ara - Green star

    # Kdn - Green diamond
    def add_kdn_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'green', 'Kdn')

    # Pse - Green flat diamond

    # LDManHep - Green hexagon

    # Fruc - Green pentagon

    # Gal - Yellow circle
    def add_gal_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'yellow', 'Gal')

    # GalNAc - Yellow square
    def add_galnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'yellow', 'GalNAc')

    # GalN - Yellow crossed square

    # GalA - Yellow divided diamond

    # Lyx - Yellow star

    # Leg - Yellow flat diamond

    # Kdo - Yellow hexagon

    # Tag - Yellow pentagon

    # Gul - Orange circle
    def add_gul_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'orange', 'Gul')

    # GulNAc - Orange square
    def add_gulnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'orange', 'GulNAc')

    # GulN - Orange crossed square

    # GulA - Orange divided diamond

    # 6dGul - Orange triangle
    def add_6dgul_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'orange', '6dGul')

    # Abe - Orange rectangle

    # Xyl - Orange star

    # Dha - Orange hexagon

    # Sor - Orange pentagon

    # Alt - Pink circle
    def add_alt_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'pink', 'Alt')

    # AltNAc - Pink square
    def add_altnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'pink', 'AltNAc')

    # AltN - Pink crossed square

    # AltA - Pink divided diamond

    # 6dAlt - Pink triangle
    def add_6dalt_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'pink', '6dAlt')

    # 6dAltNAc - Pink divided triangle

    # Par - Pink rectangle

    # Rib - Pink star

    # Aci - Pink flat diamond

    # DDManHep - Pink hexagon

    # Psi - Pink pentagon

    # All - Purple circle
    def add_all_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'purple', 'All')

    # AllNAc - Purple square
    def add_allnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'purple', 'AllNAc')

    # AllN - Purple crossed square

    # AllA - Purple divided diamond

    # Dig - Purple rectangle

    # Neu5Ac - Purple diamond
    def add_neu5ac_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'purple', 'Neu5Ac')

    # MurNAc - Purple hexagon

    # Tal - Light Blue circle
    def add_tal_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'skyblue', 'Tal')

    # TalNAc - Light Blue square
    def add_talnac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'skyblue', 'TalNAc')

    # TalN - Light Blue crossed square

    # TalA - Light Blue divided diamond

    # 6dTal - Light Blue triangle
    def add_6dtal_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'skyblue', '6dTal')

    # 6dTalNAc - Light Blue divided triangle

    # Col - Light Blue rectangle

    # Neu5Gc - Light Blue diamond
    def add_neu5gc_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'skyblue', 'Neu5Gc')

    # 4eLeg - Light Blue flat diamond

    # MurNGc - Light Blue hexagon

    # Ido - Brown circle
    def add_ido_node(self, x, y):
        add_polygon_shape(self, x, y, 'circle', 'brown', 'Ido')

    # IdoNAc - Brown square
    def add_idonac_node(self, x, y):
        add_polygon_shape(self, x, y, 'square', 'brown', 'IdoNAc')

    # IdoN - Brown crossed square

    # IdoA - Brown divided diamond

    # Neu - Brown diamond
    def add_neu_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'brown', 'Neu')

    # Mur - Brown hexagon

    # Fuc - Red triangle
    def add_fuc_node(self, x, y):
        add_polygon_shape(self, x, y, 'triangle', 'red', 'Fuc')

    # FucNAc - Red divided triangle

    # Sia - Red diamond
    def add_sia_node(self, x, y):
        add_polygon_shape(self, x, y, 'diamond', 'red', 'Sia')




    # Linkages _______________________________________________________________

    # Add α1,2
    def add_a1to2(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,2", "a1to2")

    # Add α1,3
    def add_a1to3(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,3", "a1to3")

    # Add α1,4
    def add_a1to4(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,4", "a1to4")

    # Add α1,6
    def add_a1to6(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "α1,6", "a1to6")

    # Add ß1,2
    def add_b1to2(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,2", "b1to2")

    # Add ß1,3
    def add_b1to3(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,3", "b1to3")

    # Add ß1,4
    def add_b1to4(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,4", "b1to4")

    # Add ß1,6
    def add_b1to6(self, vertex1, vertex2):
        add_linkage_type(self, vertex1, vertex2, "ß1,6", "b1to6")


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
        print("\nPrinting Weighted Matrix for Structure:")
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



        print("\n\nPrinting PCI Matrix for Structure:")
        print(table)

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

    def select_export_image_mode(self):
        """Switch to Export Image mode."""
        self.mode = "Export Image"
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        # image = ImageGrab.grab(bbox=(x, y, x1, y1))
        image = ImageGrab.grab(bbox=(40, 420, 1880, 1080))

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