from tkinter.ttk import Combobox

import network
import copy
import tkinter as tk
from tkinter import ttk


class PMApp(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.items = network.get_items()
        self.create_widgets()
        self.criteria = copy.deepcopy(network.BLANK_QUERY)

    def create_widgets(self):
        self.combo = ttk.Combobox(self.master, values=list(self.items.keys()), width=50)
        self.combo.grid(row=0, column=1)
        self.quit = tk.Button(self.master, text="X", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=0, column=0)
        self.find = tk.Button(self.master, text="Search",
                              command=self.print_list)
        self.find.grid(row=0, column=2)

    def print_list(self):
        self.clear_query()
        self.criteria['query'][self.items[self.combo.get()]] = self.combo.get()
        urls = network.look_up(self.criteria)
        for url in urls:
            print(url)

    def clear_query(self):
        self.criteria = copy.deepcopy(network.BLANK_QUERY)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PoE Market")
    app = PMApp(master=root)
    app.mainloop()
