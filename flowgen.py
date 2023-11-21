from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

class FlowgenCompiler:
    def __init__(self, master):
        self.master = master
        self.master.title('FLOWGEN')
        self.file_path = ''

        self.create_menu()

        self.editor = Text(master)
        self.editor.pack()
        ##
        self.code_output = Text(master, height=10)
        self.code_output.pack()

    def create_menu(self):
        menu_bar = Menu(self.master)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save', command=self.save)
        file_menu.add_command(label='Save As', command=self.save_as)
        file_menu.add_command(label='Exit', command=self.exit_program)
        menu_bar.add_cascade(label='File', menu=file_menu)

        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label='Run', command=self.run)
        menu_bar.add_cascade(label='Run', menu=run_menu)

        self.master.config(menu=menu_bar)

    def set_file_path(self, path):
        self.file_path = path

    def open_file(self):
        path = askopenfilename(filetypes=[('Python Files', '*.py')])
        with open(path, 'r') as file:
            code = file.read()
            self.editor.delete('1.0', END)
            self.editor.insert('1.0', code)
            self.set_file_path(path)

    def save_as(self):
        if self.file_path == '':
            path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
        else:
            path = self.file_path
        with open(path, 'w') as file:
            code = self.editor.get('1.0', END)
            file.write(code)
            self.set_file_path(path)

    def save(self):
        if self.file_path == '':
            self.save_as()
        else:
            with open(self.file_path, 'w') as file:
                code = self.editor.get('1.0', END)
                file.write(code)

    def run(self):
        if self.file_path == '':
            save_prompt = Toplevel()
            text = Label(save_prompt, text='Please save your code first!')
            text.pack()
            return

        command = f'python {self.file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.code_output.delete('1.0', END)
        self.code_output.insert('1.0', output)
        self.code_output.insert('1.0', error)

    def exit_program(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = FlowgenCompiler(root)
    root.mainloop()
