
from tkinter import BOTH, BROWSE, GROOVE, LEFT, RIGHT, Y, Button, Entry, Label, Listbox, Message, Scrollbar, StringVar, Text, Tk, messagebox, ttk

from task_model import Task

class MyApp(Tk):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_style()

        self.title(title)
        self.title = StringVar(value="")
        self.create_gui()  
    
    def create_gui(self):
        input_frame = ttk.Frame(self)
        Label(input_frame, text="Task Title").pack()
        Entry(input_frame, textvariable=self.title).pack()

        Label(input_frame, text="Task Description").pack()
        self.description = Text(input_frame)
        self.description.pack()
        Button(input_frame, text="Add Task", command=self.add_task).pack()

        input_frame.pack(side=LEFT, fill=BOTH, expand=1)

        view_frame = ttk.Frame(self)
        scroll = Scrollbar(view_frame, orient="vertical")
        self.mylist = Listbox(view_frame, yscrollcommand = scroll.set, relief=GROOVE,
                       selectmode=BROWSE, exportselection=0, background = 'white',
                       font='TkFixedFont',)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=1)
        scroll.config( command = self.mylist.yview )
        self.load_tasks()

        view_frame.pack(side=RIGHT, fill=BOTH, expand=1)
        
    def set_style(self):
        self.style = ttk.Style()
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.style.theme_use("clam")

    def add_task(self):
        title = self.title.get()
        description = self.description.get("1.0", "end-1c")
        if not title:
            messagebox.showinfo("Error", "Task title is required")
            return
        task = Task.create(title=title, description=description)
        task.save()

        self.mylist.insert(self.mylist.size(), title + "\n" + description)
        messagebox.showinfo("Task added", "Task added successfully")
    
    def load_tasks(self):
        titles = list(map(lambda x: x.title + "\n" + x.description, Task.select()))
        size = self.mylist.size()
        for title in titles:
            self.mylist.insert(size, title)
            size += 1

    def on_exit(self):
        """Close all"""
        if messagebox.askokcancel("Todo Tasks", "Do you want to quit?", parent=self):
            self.destroy()               

myapp = MyApp(title="Todo Tasks")

if __name__ == "__main__":
    myapp.mainloop()