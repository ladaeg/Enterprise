from tkinter import Tk, Toplevel, scrolledtext, messagebox, Label, Button, Entry, END, INSERT
import Enterprise_peewee as logic
import re
import time


# Для теста: логин - admin, пароль - admin123
class LoginWindow(Toplevel):
    """Окно авторизации"""
    def __init__(self):
        super().__init__(main_window)
        self.title('Авторизация')
        self.minsize(180, 200)
        self.resizable(width=False, height=False)

        Label(self, text='Введите логин').grid(row=0, column=0)
        self.input_login = Entry(self, width=17, font='Arial')
        self.input_login.grid(row=1, column=0, padx=(10, 0))

        Label(self, text='Введите пароль').grid(row=2, column=0)
        self.input_password = Entry(self, width=17, font='Arial')
        self.input_password.grid(row=3, column=0, padx=(10, 0))

        self.but_enter = Button(self, text='Войти', bg='yellow', fg='black', font='Arial', width=10,
                                height=1, command=self.enter_to_app)
        self.but_enter.grid(row=4, column=0, pady=(10, 0))

        # при закрытии окна авторизации, закрывает недоступное окно приложения
        self.protocol("WM_DELETE_WINDOW", main_window.destroy)

    def enter_to_app(self):
        """В случае успеха делает основное окно видимым"""
        login = self.input_login.get()
        password = self.input_password.get()
        if logic.enter_to_app(login, password):
            main_window.deiconify()
            self.destroy()
        else:
            Label(self, text='Неверное имя пользователя\nили пароль!', fg='red').grid(row=5, column=0)


class MainWindow(Tk):
    """Класс для создания главного окна приложения"""
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title('Работа с enterprise_database.db')
        self.minsize(900, 450)
        self.resizable(width=False, height=False)

        self.but_hire = Button(self, text='Нанять сотрудника', bg='yellow', fg='black', font='Arial', width=30,
                               height=1, command=self.hire_emp).grid(row=0, column=0)

        self.but_fire = Button(self, text='Уволить сотрудника', bg='yellow', fg='black', font='Arial', width=30,
                               height=1, command=self.fire_emp).grid(row=1, column=0)
        Label(self, text='Введите\nID сотрудника').grid(row=1, column=1)
        self.input_fire_ID = Entry(self, width=15, font='Arial')
        self.input_fire_ID.grid(row=1, column=2)

        self.but_update = Button(self, text='Изменить данные сорудника', bg='yellow', fg='black', font='Arial',
                                 width=30, height=1, command=self.update_information).grid(row=2, column=0)
        Label(self, text='Введите\nID сотрудника').grid(row=2, column=1)
        self.input_update_ID = Entry(self, width=15, font='Arial')
        self.input_update_ID.grid(row=2, column=2)

        self.but_print = Button(self, text='Вывести сотрудников с фамилией', bg='yellow', fg='black',
                                font='Arial', width=30, height=1, command=self.print_emp).grid(row=3, column=0)
        Label(self, text='Введите фамилию\nсотрудников').grid(row=3, column=1)
        self.input_print_surname = Entry(self, width=15, font='Arial')
        self.input_print_surname.grid(row=3, column=2)

        self.scroll_bar = scrolledtext.ScrolledText(self, width=130, height=20, )
        self.scroll_bar.grid(row=4, column=0, columnspan=5, pady=(10, 0))

    @staticmethod
    def hire_emp():
        """Создает окно для ввода данных нового сотрудника"""
        HireWindow()

    @staticmethod
    def is_id_in_db(emp_id):
        """Проверяет сотрудника с ID в БД. Если он не найден выводит оповещения,
        если найден возвращает True, чтобы другая функция могла работать с ним далее"""
        if emp_id == '':
            messagebox.showinfo('Предупреждение', 'Введите ID сотрудника!')
        else:
            emp = logic.find_employee(emp_id)
            if emp is None:
                messagebox.showinfo('Предупреждение', f'Нет сотрудника с ID: {emp_id}!')
                return False
            else:
                return True

    def fire_emp(self):
        """Удаляет сотрудника из БД, если он существует"""
        emp_id = self.input_fire_ID.get()
        self.input_fire_ID.delete(0, END)

        if self.is_id_in_db(emp_id):
            res = messagebox.askquestion('Предупреждение',
                                         f'Вы уверены, что хотите уволить сотрудника ID: {emp_id}?')
            if res == 'yes':
                logic.fire_employee(emp_id)
                messagebox.showinfo('Предупреждение', f'Сотрудник с ID: {emp_id} успешно уволен!')

    def update_information(self):
        """Если сотрудник существует, выводятся поля с его текущими данными, в них можно ввести новые данные"""
        emp_id = self.input_update_ID.get()
        self.input_update_ID.delete(0, END)

        if self.is_id_in_db(emp_id):
            emp = logic.find_employee(emp_id)
            # Открывает окно обновления данных сотрудника
            UpdateWindow(emp)

    def print_emp(self):
        """Выводит данные сотрудников с требуемой фамилией в скроллбар"""
        surname = self.input_print_surname.get()
        self.input_print_surname.delete(0, END)

        if surname == '':
            messagebox.showinfo('Предупреждение', 'Введите фамилию сотрудников!')
        else:
            employees = logic.find_employees_with_surname(surname)
            if not employees:       # если список пуст
                messagebox.showinfo('Предупреждение', f'Нет сотрудников с фамилией {surname}!')
            else:
                self.scroll_bar.insert(INSERT, 'ID\tФамилия\t\tИмя\t\tОтчество\t\tДата рождения\t\tТелефон\t\tОтдел'
                                               '\tДолжность\t\tЗарплата\n')
                for emp in employees:
                    self.scroll_bar.insert(INSERT, f'{emp}\n')

                self.scroll_bar.insert(INSERT, '***********************************************************************'
                                               '***************************************************\n')


class InputWindow:
    """Базовое окно для ввода данных о сотруднике и их проверки"""
    def __init__(self):
        self.input_window = Toplevel(main_window)
        self.input_window.minsize(500, 200)
        self.input_window.resizable(width=False, height=False)
        self.input_window.wm_attributes('-topmost', 1)

        self.help_label = Label(self.input_window, text='Поле для подсказок', font='Arial', fg='green')
        self.help_label.grid(row=0, column=0, columnspan=5)

        # Идея на будущее: сделать класс EntryString(Entry) и определить там метод check, таким образом
        # избавится от повторения строк с bind (так соответственно можно сделать для полей ввода даты, номеров и тд)
        Label(self.input_window, text='Фамилия', font='Arial').grid(row=1, column=0)
        self.input_surname = Entry(self.input_window, width=15, font='Arial')
        self.input_surname.grid(row=2, column=0)
        self.input_surname.bind('<KeyRelease>', self.check_only_char)

        Label(self.input_window, text='Имя', font='Arial').grid(row=1, column=1)
        self.input_first_name = Entry(self.input_window, width=15, font='Arial')
        self.input_first_name.grid(row=2, column=1)
        self.input_first_name.bind('<KeyRelease>', self.check_only_char)

        Label(self.input_window, text='Отчество', font='Arial').grid(row=1, column=2)
        self.input_father_name = Entry(self.input_window, width=15, font='Arial')
        self.input_father_name.grid(row=2, column=2)
        self.input_father_name.bind('<KeyRelease>', self.check_only_char)

        Label(self.input_window, text='Дата рождения', font='Arial').grid(row=1, column=3)
        self.input_birth_date = Entry(self.input_window, width=15, font='Arial')
        self.input_birth_date.grid(row=2, column=3)
        self.input_birth_date.bind('<KeyRelease>', self.check_date)

        Label(self.input_window, text='Контактный номер', font='Arial').grid(row=1, column=4)
        self.input_number = Entry(self.input_window, width=15, font='Arial')
        self.input_number.grid(row=2, column=4)
        self.input_number.bind('<KeyRelease>', self.check_number)

        Label(self.input_window, text='Шифр отдела', font='Arial').grid(row=3, column=0)
        self.input_department_id = Entry(self.input_window, width=15, font='Arial')
        self.input_department_id.grid(row=4, column=0)
        self.input_department_id.bind('<KeyRelease>', self.check_only_digit)

        Label(self.input_window, text='Должность', font='Arial').grid(row=3, column=1)
        self.input_position = Entry(self.input_window, width=15, font='Arial')
        self.input_position.grid(row=4, column=1)
        self.input_position.bind('<KeyRelease>', self.check_only_char)

        Label(self.input_window, text='Зарплата', font='Arial').grid(row=3, column=2)
        self.input_salary = Entry(self.input_window, width=15, font='Arial')
        self.input_salary.grid(row=4, column=2)
        self.input_salary.bind('<KeyRelease>', self.check_only_digit)

        # система флагов для гарантии верного заполнения полей ввода перед отправкой данных из них в БД
        self.flags = {self.input_surname: False,
                      self.input_first_name: False,
                      self.input_father_name: False,
                      self.input_birth_date: False,
                      self.input_number: False,
                      self.input_department_id: False,
                      self.input_position: False,
                      self.input_salary: False}

    def check_only_char(self, event):
        """Проверяет условие, что поле содержит только буквы, в случае чего меняет флаг"""
        self.help_label.configure(text='Поле должно содержать только буквы')
        char_set = event.widget.get()
        if char_set.isalpha():
            char_set = char_set.capitalize()
            event.widget.delete(0, END)
            event.widget.insert(0, char_set)
            event.widget.configure(bg="#90EE90")
            self.flags[event.widget] = True
        else:
            event.widget.configure(bg="#FFB6C1")
            self.flags[event.widget] = False

    def check_date(self, event):
        """Проверяет условие, что поле содержит дату в верном формате, в случае чего меняет флаг"""
        self.help_label.configure(text='Поле должно содержать дату в формате дд.мм.гггг')
        date = event.widget.get()
        match = re.fullmatch(r'\d\d\.\d\d\.\d{4}', date)
        if match:
            try:
                time.strptime(date, '%d.%m.%Y')
                event.widget.configure(bg="#90EE90")
                self.flags[event.widget] = True
            except ValueError:
                event.widget.configure(bg="#FFB6C1")
                self.flags[event.widget] = False
        else:
            event.widget.configure(bg="#FFB6C1")
            self.flags[event.widget] = False

    def check_number(self, event):
        """Проверяет условие, что поле содержит номер телефона в верном формате, в случае чего меняет флаг"""
        self.help_label.configure(text='Поле должно содержать номер в формате +76665554433')
        number = event.widget.get()
        match = re.fullmatch(r'\+7\d{10}', number)
        if match:
            event.widget.configure(bg="#90EE90")
            self.flags[event.widget] = True
        else:
            event.widget.configure(bg="#FFB6C1")
            self.flags[event.widget] = False

    def check_only_digit(self, event):
        """Проверяет условие, что поле содержит только цифры, в случае чего меняет флаг"""
        self.help_label.configure(text='Поле должно содержать только числа')
        digit_set = event.widget.get()
        if digit_set.isdigit():
            event.widget.configure(bg="#90EE90")
            self.flags[event.widget] = True
        else:
            event.widget.configure(bg="#FFB6C1")
            self.flags[event.widget] = False

    def all_flags_is_true(self):
        """Проверяет флаг каждого поля, если хоть одно заполнено неверно возращает False"""
        for flag in self.flags.values():
            if flag is False:
                self.help_label.configure(text='Проверьте правильность заполнения полей!')
                messagebox.showinfo('Предупреждение', 'Некоторые поля пусты или заполнены неверно!')
                return False
        return True


class HireWindow(InputWindow):
    """Окно позволяет внести данные о новом сотруднике в БД"""
    def __init__(self):
        super().__init__()

        self.input_window.title('Нанять сотрудника')

        self.input_number.insert(0, '+7')

        Label(self.input_window, text='Нажмите, когда все\nполя будут заполнены').grid(row=5, column=0)
        but_send = Button(self.input_window, text='Нанять сотрудника', bg='yellow',
                          fg='black', font='Arial', width=30, height=1, command=self.send_data)
        but_send.grid(row=5, column=1, columnspan=2, pady=(10, 0))

    def send_data(self):
        """Если все поля заполнены верно, отправляет информацию о сотруднике в БД"""
        if self.all_flags_is_true():
            logic.hire_employee(self.input_surname.get(),
                                self.input_first_name.get(),
                                self.input_father_name.get(),
                                self.input_birth_date.get(),
                                self.input_number.get(),
                                self.input_department_id.get(),
                                self.input_position.get(),
                                self.input_salary.get())
            messagebox.showinfo('Предупреждение', 'Работник успешно добавлен!')

            # после отправки удаляет текущее окно и создает новое - удобно,
            # если нужно добавить несколько сотрудников подряд
            self.input_window.destroy()
            HireWindow()


class UpdateWindow(InputWindow):
    """Окно обновления данных о существующем сотруднике, поля ввода содержат его текущие данные"""
    def __init__(self, emp):
        self.emp_id = emp.employee_id
        super().__init__()
        self.input_surname.insert(END, emp.surname)
        self.input_first_name.insert(END, emp.first_name)
        self.input_father_name.insert(END, emp.father_name)
        self.input_birth_date.insert(END, emp.birth_date)
        self.input_number.insert(END, emp.contact_number)
        self.input_department_id.insert(END, emp.department_id)
        self.input_position.insert(END, emp.position)
        self.input_salary.insert(END, emp.salary)
        # Информация уже имеющаеся в БД признается верной по умолчанию
        self.flags = {self.input_surname: True,
                      self.input_first_name: True,
                      self.input_father_name: True,
                      self.input_birth_date: True,
                      self.input_number: True,
                      self.input_department_id: True,
                      self.input_position: True,
                      self.input_salary: True}

        Label(self.input_window, text='Нажмите, когда все\nполя будут заполнены').grid(row=5, column=0)
        but_send = Button(self.input_window, text='Изменить данные', bg='yellow',
                          fg='black', font='Arial', width=30, height=1, command=self.send_data)
        but_send.grid(row=5, column=1, columnspan=2, pady=(10, 0))

    def send_data(self):
        """Если все поля заполнены верно, обновляет информацию о сотруднике в БД"""
        if self.all_flags_is_true():
            res = messagebox.askquestion('Предупреждение', f'Вы уверены, что хотите изменить данные'
                                                           f'сотрудника с ID: {self.emp_id}?')
            if res == 'yes':
                logic.update_employee_data(self.emp_id,
                                           self.input_surname.get(),
                                           self.input_first_name.get(),
                                           self.input_father_name.get(),
                                           self.input_birth_date.get(),
                                           self.input_number.get(),
                                           self.input_department_id.get(),
                                           self.input_position.get(),
                                           self.input_salary.get())
                messagebox.showinfo('Предупреждение', f'Данные сотрудника с ID: {self.emp_id} успешно обновлены!')
                self.input_window.destroy()


if __name__ == "__main__":
    main_window = MainWindow()
    login_window = LoginWindow()
    main_window.mainloop()
