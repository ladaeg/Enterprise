# ДЗ №3
# Доработать разработанную во время урока, программу следующими методами:
# 1) addJournal(self,id, name, year, shelve, publisher,idauthor) – метод должен осуществлять добавление нового журнала
# в БД. Сделала метод hire_employee
# 2) updateAuthor(self, name, id) – метод должен осуществлять изменение имени автора.
# updateJournal(self, name, id) – метод должен осуществлять изменение имени журнала.
# Сделала change_employee_number
# 3) deleteBook(self,id) – метод должен удалять существующую книгу по номеру id.
# deleteJournal(self,id) – метод должен удалять существующий журнал по номеру id.
# Сделала fire_employee
# 4) searchBook(self, name) – метод должен осуществлять поиск книги в БД по названию и распечатывать информацию о новой
# книги, либо выводить сообщение о то, что такой книги не существует в БД
# сделала print_employees_with_surname

from Enterprise_peewee_model import Employee, User, enterprise_db
import peewee


def add_user(login, password):
    """Добавляет нового пользователя, если логин уникален"""
    try:
        User(login=login, password=password).save()
    except peewee.IntegrityError:
        print('Пользователь с этим логином уже существует')


def enter_to_app(login, password):
    """Дает доступ, если логин и пароль введены верно"""
    try:
        user = User.get(User.login == login)
        if password == user.password:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def hire_employee(surname, first_name, father_name, birth_date, contact_number, department_id, position, salary):
    """Добавляет сотрудника в БД"""
    Employee(surname=surname, first_name=first_name, father_name=father_name, birth_date=birth_date,
             contact_number=contact_number, department_id=department_id, position=position, salary=salary).save()


def fire_employee(employee_id):
    """Удаляет сотрудника из БД"""
    emp = find_employee(employee_id)
    if emp is not None:
        emp.delete_instance()
        return True
    else:
        return False


def find_employee(employee_id):
    """Возвращает сотрудника с искомым employee_id"""
    try:
        emp = Employee.get(Employee.employee_id == employee_id)
        return emp
    except Employee.DoesNotExist:
        return None


def update_employee_data(employee_id, surname, first_name, father_name, birth_date, contact_number, department_id,
                         position, salary):
    """Обновляет данные сотрудника сотрудника"""
    Employee.update(surname=surname, first_name=first_name, father_name=father_name, birth_date=birth_date,
                    contact_number=contact_number, department_id=department_id, position=position,
                    salary=salary).where(Employee.employee_id == employee_id).execute()


def find_employees_with_surname(surname):
    """Выводит информацию сотрудников с искомой фамилией"""
    try:
        emp_with_same_surname = Employee.select().where(Employee.surname == surname)
        return emp_with_same_surname
    except Employee.DoesNotExist:
        return None


if __name__ == "__main__":
    with enterprise_db:
        # enterprise_db.create_tables([Employee])
        #
        # hire_employee('Иванов', 'Иван', 'Иванович', '09.09.1999', '88005553535', 'Ц001', 'Токарь', 25000)
        # hire_employee('Петров', 'Юрий', 'Иванович', '10.09.1999', '89645154829', 'Ц001', 'Токарь', 20000)
        # hire_employee('Сидоров', 'Алексей', 'Алексеевич', '09.10.1998', '88885553535', 'Ц001', 'Инженер', 60000)
        # hire_employee('Иванов', 'Петр', 'Никитич', '09.09.1999', '88005553535', 'Ц001', 'Фрезеровщик', 25000)
        #
        # print(find_employee(3))
        #
        # find_employees_with_surname('Иванов')  # я не знаю, почему выравнивание ломается
        # fire_employee(4)
        #
        # find_employees_with_surname('Иванов')
        enterprise_db.create_tables([User])
        add_user('admin', 'admin123')
        print(enter_to_app('admin1', 'admin123'))

    print('done')
