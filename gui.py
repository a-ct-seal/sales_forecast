from abc import ABC, abstractmethod
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import *
from tkinter.ttk import Combobox as Cb
import prediction_model as prm
import warnings

warnings.filterwarnings("ignore")

FONT = 'Calibri, 11'
LABEL_FONT = 'Calibri, 13'
COLOR = 'PaleGreen1'
INSTRUCTION_TEXT = "Instructions for using the program:\n" \
                   "1) Only a number(int/float) can be entered as the price of the product, the integer and " \
                   "fractional parts are separated by a dot;\n" \
                   "2) The program processes files with extensions .csv и .xlsx;\n" \
                   "3) When using file data entry, the program saves the file with the results in the same directory " \
                   "where the source file is located;\n" \
                   "4) The file is saved with the name <input_file_name>_predicted.xlsx"


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def return_predicted_file(model):
    file_name = fd.askopenfilename()
    exp = file_name[-4:]
    if exp != '.csv' and exp != '.xlsx' and file_name != '':
        mb.showerror('Invalid file format', '''Working with this type of files is not supported''')
        return
    try:
        res_name = model.predict_file(file_name, exp)
        mb.showinfo('Done', f'The forecast results were saved to a file {res_name}')
    except:
        mb.showerror('Invalid data', 'Data in file is invalid')


def show_help_info():
    mb.showinfo('Help', INSTRUCTION_TEXT)


class Window(ABC):
    def __init__(self, title='Sales forecast', geometry='550x450+175+125', resizable=(False, False)):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(resizable[0], resizable[1])
        self.price_entry = Entry(self.root)
        self.week_day_cb = Cb(self.root,
                              values=('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'),
                              state='readonly')
        self.category_cb = Cb(self.root,
                              values=('Bread', 'Pies', 'Milk and fermented milk products',
                                      'Cheese and cottage cheese', 'Other'),
                              state='readonly')
        self.lbl_ans = Label(self.root, font=LABEL_FONT)

    def greeting(self):
        greet_window = Toplevel(self.root)
        greet_window.title('Greeting')
        greet_window.geometry('450x300+200+150')
        greet_window.resizable(False, False)
        Label(greet_window,
              text='Trading company\nSales forecast',
              font=FONT) \
            .grid(column=0, row=0, padx=130, pady=40, sticky=W + E)
        Button(greet_window, text='Next', command=greet_window.destroy, padx=20, pady=10, font=FONT,
               bg=COLOR) \
            .grid(column=0, row=1, padx=5, pady=5)
        greet_window.grab_set()
        greet_window.focus_set()
        greet_window.wait_window()

    def draw_menu(self):
        menu_bar = Menu(self.root, tearoff=0)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Open', command=return_predicted_file)
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_command(label='Help', command=show_help_info)
        self.root.configure(menu=menu_bar)

    @abstractmethod
    def draw_widgets(self):
        pass

    def run(self):
        self.root.withdraw()
        self.greeting()
        self.root.deiconify()
        self.draw_widgets()
        self.root.mainloop()


class PredictionWindow(Window):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def draw_widgets(self):
        self.draw_menu()
        Label(self.root, text='Product price', font=FONT) \
            .grid(column=0, row=0, sticky=W, padx=5, pady=5)
        Label(self.root, text='Day of the week', font=FONT) \
            .grid(column=0, row=1, sticky=W, padx=5, pady=5)
        Label(self.root, text='Product category', font=FONT) \
            .grid(column=0, row=2, sticky=W, padx=5, pady=5)
        self.price_entry.grid(column=1, row=0, sticky=W, padx=5, pady=5)
        self.week_day_cb.grid(column=1, row=1, sticky=W, padx=5, pady=5)
        self.week_day_cb.configure(width=40)
        self.category_cb.grid(column=1, row=2, sticky=W, padx=5, pady=5)
        self.category_cb.configure(width=40)
        Button(self.root, text='Get forecast', command=self.output_prediction,
               padx=20, pady=10, font=FONT, bg=COLOR) \
            .grid(column=0, row=3, columnspan=3, pady=23)

    def output_prediction(self):
        price = self.price_entry.get()
        week_day = self.week_day_cb.current()
        category = self.category_cb.current()
        if week_day == -1 or category == -1 or price is None:
            mb.showwarning('There is not enough data', 'Please, input product data')
            return
        if not is_digit(price):
            mb.showerror('Invalid data', 'Input correct data')
            return
        res = model.predict_object(price, week_day, category)
        self.lbl_ans.configure(text=f'Necessary to order, items\t{res}')
        self.lbl_ans.grid(column=0, row=4, columnspan=10, sticky=W, padx=5, pady=23)


if __name__ == '__main__':
    model = prm.PredictionModel()
    window = PredictionWindow(model)
    window.run()
