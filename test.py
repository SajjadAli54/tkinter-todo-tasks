 #!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

from task_model import Task


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.init_ui()

    def init_ui(self):

        self.pack(fill=tk.BOTH, expand=1)

        frame = ttk.Frame()

        ttk.Label(frame, text = "Listbox").pack()
        sb = tk.Scrollbar(frame,orient=tk.VERTICAL)

        self.lstItems = tk.Listbox(frame,
                       relief=tk.GROOVE,
                       selectmode=tk.BROWSE,
                       exportselection=0,
                       height=20,
                       width=50,
                       background = 'white',
                       font='TkFixedFont',
                       yscrollcommand=sb.set,)

        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)

        sb.config(command=self.lstItems.yview)

        self.lstItems.pack(side=tk.LEFT,fill=tk.BOTH, expand =1) 
        sb.pack(fill=tk.Y, expand=1)

        w = ttk.Frame()

        ttk.Button(w, text="Insert", command=self.on_create).pack()
        ttk.Button(w, text="Load", command=self.on_load).pack()
        ttk.Button(w, text="Close", command=self.on_close).pack()

        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        w.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def on_create(self,):
        title = simpledialog.askstring("Title", "Enter the title")
        if title:
            description = simpledialog.askstring("Description", "Enter the description")
            task = Task.create(title=title, description=description)
            task.save()
            self.on_load()

    def on_load(self,):
        titles = list(map(lambda x: x.title, Task.select()))
        index = 0
        self.dict_items={}

        self.lstItems.delete(0, tk.END)

        for title in titles:
            self.lstItems.insert(tk.END, title)
            self.dict_items[index] = title
            index += 1

    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            print("Double-Button-1 self.lstItems.curselection()[0]: {0}".format(index))


        else:
            messagebox.showwarning(self.parent.title(), "No item selected", parent=self)

    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            print("ListboxSelect self.dict_items.get(index) = {0}".format(pk))
            task = Task.get(Task.title == pk)
            print("ListboxSelect self.rs[index]: {0}".format(task))


    def on_close(self):
        self.parent.on_exit()

class App(tk.Tk):
    """Start here"""

    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.set_title()
        self.set_style()

        frame = Main(self,)
        frame.pack(fill=tk.BOTH, expand=1)

    def set_style(self):
        self.style = ttk.Style()
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.style.theme_use("clam")


    def set_title(self):
        s = "{0}".format('Simple App')
        self.title(s)

    def on_exit(self):
        """Close all"""
        if messagebox.askokcancel("Simple App", "Do you want to quit?", parent=self):
            self.destroy()               

if __name__ == '__main__':
    app = App()
    app.mainloop()