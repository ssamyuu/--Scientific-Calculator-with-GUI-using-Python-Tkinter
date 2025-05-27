import tkinter as tk
from tkinter import messagebox, filedialog
from simpleeval import simple_eval
import math

# ========== Calculator Application ========== #
class ScientificCalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Samyuktha's Scientific Calculator")
        self.dark_mode = True
        self.last_results = []
        self.last_result_value = None

        self.setup_ui()
        self.toggle_theme()  # Apply initial theme with colors

    def setup_ui(self):
        self.input_box = tk.Entry(self.master, font=("Arial", 18), justify="right", bd=5, width=40)
        self.input_box.grid(row=0, column=0, columnspan=6, padx=14, pady=20, ipady=10)

        self.master.bind("<Return>", self.get_result)
        self.master.bind("<BackSpace>", lambda e: self.del_entry())

        buttons = [
            ['7', '8', '9', '/', 'sqrt', 'log'],
            ['4', '5', '6', '*', 'sin', 'cos'],
            ['1', '2', '3', '-', 'tan', 'Del'],
            ['0', '.', '=', '+', 'Clear', '⟳'],
            ['Ans', 'π', 'x²', 'Theme', 'Save', 'History']
        ]

        self.all_buttons = []
        for row_index, row in enumerate(buttons, start=1):
            for col_index, label in enumerate(row):
                action = self.get_action(label)
                btn = tk.Button(self.master, text=label, width=6, height=2, command=action,
                                font=("Arial", 12))
                btn.grid(row=row_index, column=col_index, padx=3, pady=3)
                self.all_buttons.append(btn)

    def get_action(self, label):
        scientific_funcs = {
            'sqrt': lambda: self.apply_scientific('sqrt'),
            'log': lambda: self.apply_scientific('log'),
            'sin': lambda: self.apply_scientific('sin'),
            'cos': lambda: self.apply_scientific('cos'),
            'tan': lambda: self.apply_scientific('tan'),
            'x²': lambda: self.apply_scientific('square'),
            '=': self.get_result,
            'Clear': self.clear_entry,
            'Del': self.del_entry,
            '⟳': self.show_history,
            'History': self.show_history,
            'Save': self.save_history,
            'Theme': self.toggle_theme,
            'π': self.insert_pi,
            'Ans': self.insert_last_result
        }
        return scientific_funcs.get(label, lambda l=label: self.insert_entry(l))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            bg_color = "#2d4053"
            fg_color = "#dce1e6"
            input_bg = "#cfd6dd"
            btn_bg = "#648181"
        else:
            bg_color = "#ffffff"
            fg_color = "#000000"
            input_bg = "#f5f5f5"
            btn_bg = "#dddddd"

        self.master.config(bg=bg_color)
        self.input_box.config(bg=input_bg, fg=fg_color)

        for btn in self.all_buttons:
            btn.config(bg=btn_bg, fg=fg_color, activebackground="#4e6d6d")

    def insert_entry(self, val):
        self.input_box.insert(tk.END, val)

    def clear_entry(self):
        self.input_box.delete(0, tk.END)

    def del_entry(self):
        current = self.input_box.get()
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, current[:-1])

    def get_result(self, event=None):
        expression = self.input_box.get()
        try:
            result = simple_eval(expression)
            self.last_result_value = result
            self.last_results.append(f"{expression} = {result}")
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, str(result))
        except Exception:
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, "Error")

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Calculation History")
        history_text = tk.Text(history_window, height=15, width=40)
        history_text.pack(padx=10, pady=10)
        for entry in self.last_results:
            history_text.insert(tk.END, entry + "\n")

    def save_history(self):
        if not self.last_results:
            messagebox.showinfo("Info", "No history to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(self.last_results))
            messagebox.showinfo("Success", "History saved successfully.")

    def insert_last_result(self):
        if self.last_result_value is not None:
            self.input_box.insert(tk.END, str(self.last_result_value))

    def insert_pi(self):
        self.input_box.insert(tk.END, str(round(math.pi, 8)))

    def apply_scientific(self, func):
        try:
            val = float(self.input_box.get())
            if func == 'sqrt':
                result = math.sqrt(val)
            elif func == 'log':
                result = math.log10(val)
            elif func == 'sin':
                result = math.sin(math.radians(val))
            elif func == 'cos':
                result = math.cos(math.radians(val))
            elif func == 'tan':
                result = math.tan(math.radians(val))
            elif func == 'square':
                result = val ** 2
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, str(result))
        except Exception:
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, "Error")

# ========== Launch Application ========== #
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculatorApp(root)
    root.mainloop()
