# import tkinter as tk
# from PIL import ImageGrab, Image, ImageTk
#
# def sugar_module(self, sugar_name, button, sugar_buttons_dict, sugar_selection_command):
#     # Generic Sugar Button
#     self.sugar_img = Image.open(
#         f"../Assets/Sugars/{sugar_name}.png").resize((50, 50))
#     self.sugar_button_image = ImageTk.PhotoImage(self.sugar_img)
#
#     self.sugar_button = tk.Button(button,
#                                     image=self.sugar_button_image,
#                                     borderwidth=0, highlightthickness=0,
#                                     command=sugar_selection_command)
#
#     sugar_buttons_dict[sugar_name] = self.sugar_button
#
#     return self.sugar_button.pack(side="left", padx=5)
