from flask_wtf import FlaskForm
# FlaskForm - основа для создания веб-форм в приложении
from wtforms import StringField, TextAreaField
# StringField - поле для ввода 1 строки
# TextAreaField - поле для многострочного ввода
from wtforms import BooleanField, SubmitField, IntegerField, DateTimeLocalField
# BooleanField - поле-чекбокс
# SubmitField - кнопка отправки формы
from wtforms.validators import DataRequired
# DataRequired - валидатор, проверяющий, что поле непустое


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Размер работ')
    collaborators = TextAreaField('Участники')
    end_date = DateTimeLocalField('Дата окончания', format='%Y-%m-%dT%H:%M')
    is_finished = BooleanField('Работа завершена')
    is_private = BooleanField('Личная работа')
    submit = SubmitField('Сохранить')
