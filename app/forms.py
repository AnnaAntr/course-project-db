from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, SelectField, validators

class AdminRegForm(FlaskForm):
    username = StringField('Имя', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Пароль', [validators.InputRequired(), validators.Length(min=6, max=100)])
    submit = SubmitField('Зарегистрироваться')


class AdminLoginForm(FlaskForm):
    username = StringField('Логин', [validators.InputRequired()])
    password = PasswordField('Пароль', [validators.InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ScheduleForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    teacher = SelectField('Преподаватель', coerce=int, default=0)
    corp = SelectField('Корпус', coerce=int, default=0)
    aud = SelectField('Аудитория', coerce=int, default=0)
    submit = SubmitField('Показать')


class InsertStreamForm(FlaskForm):
    dir = SelectField('Направление', coerce=int, default=0)
    year = IntegerField('Год поступления', [validators.InputRequired(), validators.NumberRange(min=2000, max=2100)])
    submit = SubmitField('Добавить')


class DeleteStreamForm(FlaskForm):
    stream = SelectField('Поток', coerce=int, default=0)
    submit = SubmitField('Удалить')


class UpdateGroupForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    curr_term = IntegerField('Изменить текущий семестр на', [validators.InputRequired(),
                                                             validators.NumberRange(min=1, max=12)])
    submit = SubmitField('Сохранить')


class InsertGroupForm(FlaskForm):
    group = StringField('Номер группы', [validators.InputRequired()])
    curr_term = IntegerField('Текущий семестр', [validators.InputRequired(),
                                                 validators.NumberRange(min=1, max=12)])
    dir = SelectField('Направление', coerce=int, default=0)
    year = IntegerField('Год поступления', [validators.InputRequired(),
                                            validators.NumberRange(min=2000, max=2100)])
    submit = SubmitField('Добавить')


class DeleteGroupForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    submit = SubmitField('Удалить')


class UpdateTeacherForm(FlaskForm):
    name = SelectField('Преподаватель', coerce=int, default=0)
    new_name = StringField('Новые ФИО')
    position = StringField('Изменить должность на')
    dep_ch = SelectField('Изменить кафедру', coerce=int, choices=[(0, 'не выбрано'), (1, 'изменить'), (2, 'добавить'), (3, 'удалить')], default=0)
    dep = SelectField('Номер кафедры', coerce=int, default=0)
    submit = SubmitField('Сохранить')


class InsertTeacherForm(FlaskForm):
    name = StringField('ФИО', [validators.InputRequired()])
    position = StringField('Должность')
    rec_num = StringField('Номер трудовой книжки', [validators.InputRequired()])
    dep = SelectField('Номер кафедры', coerce=int, default=0)
    submit = SubmitField('Добавить')


class DeleteTeacherForm(FlaskForm):
    name = SelectField('Преподаватель', coerce=int, default=0)
    submit = SubmitField('Удалить')


class ChooseGroupForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    submit = SubmitField('Далее')


class UpdateScheduleForm(FlaskForm):
    pare = SelectField('Пара', coerce=int, default=0)
    wtype = SelectField('Тип недели', coerce=int, choices=[(0, 'не выбрано'), (1, 'Четная'), (2, 'Нечетная')], default=0)
    wday = SelectField('День недели', coerce=int, choices=[(0, 'не выбрано'), (1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], default=0)
    num = IntegerField('Номер пары', [validators.NumberRange(min=1, max=6)])
    corp = SelectField('Корпус', coerce=int, default=0)
    aud = SelectField('Аудитория', coerce=int, default=0)
    course = SelectField('Предмет', coerce=int, default=0)
    teacher = SelectField('Преподаватель', coerce=int, default=0)
    submit = SubmitField('Сохранить')


class InsertScheduleForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    wtype = SelectField('Тип недели', coerce=int, choices=[(0, 'не выбрано'), (1, 'Четная'), (2, 'Нечетная')], default=0)
    wday = SelectField('День недели', coerce=int, choices=[(0, 'не выбрано'), (1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], default=0)
    num = IntegerField('Номер пары', [validators.NumberRange(min=1, max=6), validators.InputRequired()])
    corp = SelectField('Корпус', coerce=int, default=0)
    aud = SelectField('Аудитория', coerce=int, default=0)
    course = SelectField('Предмет', coerce=int, default=0)
    teacher = SelectField('Преподаватель', coerce=int, default=0)
    submit = SubmitField('Добавить')


class DeleteScheduleForm(FlaskForm):
    group = SelectField('Группа', coerce=int, default=0)
    submit = SubmitField('Удалить')


class UpdatePlanForm(FlaskForm):
    course = SelectField('Предмет', coerce=int, default=0)
    term = IntegerField('Семестр', [validators.NumberRange(min=1, max=12)])
    lec = IntegerField('Количество лекционных часов', [validators.NumberRange(min=0, max=100), validators.optional()])
    lab = IntegerField('Количество лабораторных часов', [validators.NumberRange(min=0, max=100), validators.optional()])
    att = SelectField('Тип аттестации', coerce=int, choices=[(0, 'не выбрано'), (1, 'Экзамен'), (2, 'Зачет'), (3, 'Диф.зачет'), (4, 'Курсовая работа')], default=0)
    submit = SubmitField('Сохранить')


class InsertPlanForm(FlaskForm):
    stream = SelectField('Поток', coerce=int, default=0)
    term = IntegerField('Номер семестра', [validators.NumberRange(min=1, max=12), validators.InputRequired()])
    course = SelectField('Предмет', coerce=int, default=0)
    att = SelectField('Тип аттестации', coerce=int, choices=[(0, 'не выбрано'), (1, 'Экзамен'), (2, 'Зачет'), (3, 'Диф.зачет'), (4, 'Курсовая работа')], default=0)
    lec = IntegerField('Лекционные часы', [validators.NumberRange(min=0, max=100), validators.optional()])
    lab = IntegerField('Лабораторные часы', [validators.NumberRange(min=0, max=100), validators.optional()])
    submit = SubmitField('Добавить')


class DeletePlanForm(FlaskForm):
    course = SelectField('Предмет', coerce=int, default=0)
    submit = SubmitField('Удалить')


class InsertCourseForm(FlaskForm):
    course = StringField('Название предмета', [validators.InputRequired()])
    submit = SubmitField('Добавить')


class UpdateCourseForm(FlaskForm):
    course = SelectField('Название предмета', coerce=int, default=0)
    new_name = StringField('Новое название', [validators.InputRequired()])
    submit = SubmitField('Сохранить')


class DeleteCourseForm(FlaskForm):
    course = SelectField('Название предмета', coerce=int, default=0)
    submit = SubmitField('Удалить')