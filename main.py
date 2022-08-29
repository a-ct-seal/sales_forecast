from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import *
from tkinter.ttk import Combobox as Cb
import prediction_model as prm
import warnings

warnings.filterwarnings("ignore")


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


FONT = 'Calibri, 11'


def write_help():
    text = '''Инструкции по использованию программы:
    1) В качестве цены товара может быть введено только число, целая и дробная части разделяются точкой
    2) Программа обрабатывает файлы с расширениями .csv и .xlsx
    3) При использовании файлового ввода данных программа сохраняет файл с результатами в той же директории, где лежит исходный файл;
    4) Файл сохраняется с расширением .xlsx, с названием <имя_входного файла>_predicted.xlsx'''
    mb.showinfo('Помощь', text)


def return_predicted_file():
    file_name = fd.askopenfilename()
    exp = file_name[-4:]
    if exp != '.csv' and exp != '.xlsx' and file_name != '':
        mb.showerror('Неверный формат файла', '''Работа с данным типом файлов не поддерживается''')
        return
    try:
        res_name = prm.predict_file(file_name, exp)
        mb.showinfo('Готово', f'Результаты прогноза были сохранены в файл {res_name}')
    except FileNotFoundError:
        pass
    except:
        mb.showerror('Некорректные данные', 'Данные в файле некорректны')


class Window:
    def __init__(self, title='Прогноз продаж', geometry='550x450+175+125', resizable=(False, False)):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(resizable[0], resizable[1])
        self.price_entry = Entry(self.root)
        self.week_day_cb = Cb(self.root,
                              values=('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'),
                              state='readonly')
        self.category_cb = Cb(self.root,
                              values=('Хлеб', 'Пирожки', 'Молоко и кисломолочная продукция', 'Сыр и творог', 'Другое'),
                              state='readonly')
        self.lbl_ans = Label(self.root, font='Calibri, 13')

    def greeting(self):
        greet_window = Toplevel(self.root)
        greet_window.title('Приветствие')
        greet_window.geometry('450x300+200+150')
        greet_window.resizable(False, False)
        Label(greet_window,
              text='''Торговое предприятие\nПрогноз продаж''',
              font=FONT) \
            .grid(column=0, row=0, padx=130, pady=40, sticky=W + E)
        Button(greet_window, text='Далее', command=greet_window.destroy, padx=20, pady=10, font=FONT,
               bg='PaleGreen1') \
            .grid(column=0, row=1, padx=5, pady=5)
        greet_window.grab_set()
        greet_window.focus_set()
        greet_window.wait_window()

    def draw_menu(self):
        menu_bar = Menu(self.root, tearoff=0)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Открыть', command=return_predicted_file)
        menu_bar.add_cascade(label='Файл', menu=file_menu)

        menu_bar.add_command(label='Помощь', command=write_help)

        self.root.configure(menu=menu_bar)

    def draw_widgets(self):
        self.draw_menu()
        Label(self.root, text='Введите стоимость товара', font=FONT) \
            .grid(column=0, row=0, sticky=W, padx=5, pady=5)
        Label(self.root, text='Выберите день недели', font=FONT) \
            .grid(column=0, row=1, sticky=W, padx=5, pady=5)
        Label(self.root, text='Выберите категорию товара', font=FONT) \
            .grid(column=0, row=2, sticky=W, padx=5, pady=5)

        self.price_entry.grid(column=1, row=0, sticky=W, padx=5, pady=5)
        self.week_day_cb.grid(column=1, row=1, sticky=W, padx=5, pady=5)
        self.week_day_cb.configure(width=40)
        self.category_cb.grid(column=1, row=2, sticky=W, padx=5, pady=5)
        self.category_cb.configure(width=40)

        Button(self.root, text='Получить прогноз', command=self.output_prediction,
               padx=20, pady=10, font=FONT, bg='PaleGreen1') \
            .grid(column=0, row=3, columnspan=3, pady=23)

    def output_prediction(self):
        price = self.price_entry.get()
        week_day = self.week_day_cb.current()
        category = self.category_cb.current()

        if week_day == -1 or category == -1 or price is None:
            mb.showwarning('Данные не были введены', 'Пожалуйста, введите данные')
            return

        if not is_digit(price):
            mb.showerror('Некорректные данные', 'Введите корректные данные')
            return

        res = prm.predict_object(price, week_day, category)

        self.lbl_ans.configure(text=f'Необходимо заказать, единиц товара\t{res}')
        self.lbl_ans.grid(column=0, row=4, columnspan=10, sticky=W, padx=5, pady=23)

    def run(self):
        self.root.withdraw()
        self.greeting()
        self.root.deiconify()
        self.draw_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    window = Window()
    window.run()
