from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField, SqliteDatabase, Model

enterprise_db = SqliteDatabase('enterprise_database.db')


class Employee(Model):
    """Класс для записи данных сотрудников"""
    employee_id = PrimaryKeyField(unique=True)
    surname = CharField()
    first_name = CharField()
    father_name = CharField()
    birth_date = DateTimeField()
    contact_number = CharField()
    department_id = CharField()
    position = CharField()
    salary = IntegerField()

    class Meta:
        database = enterprise_db
        order_by = 'employee_id'
        table_name = 'employees'

    def __str__(self):
        return f'{self.employee_id}\t{self.surname}\t\t{self.first_name}\t\t{self.father_name}\t\t' \
               f'{self.birth_date}\t\t{self.contact_number}\t\t{self.department_id}\t{self.position}\t\t{self.salary}'


class User(Model):
    """Класс для записи данных пользователей"""
    login = CharField(unique=True)
    password = CharField()

    class Meta:
        database = enterprise_db
        order_by = 'login'
        table_name = 'users'
