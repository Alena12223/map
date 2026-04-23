from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeLocalField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):

    job = StringField('Название работы', validators=[DataRequired()])

    work_size = IntegerField('Размер работы')

    collaborators = TextAreaField('Список участников')

    start_date = DateTimeLocalField('Дата начала', format='%Y-%m-%dT%H:%M')

    end_date = DateTimeLocalField('Дата окончания', format='%Y-%m-%dT%H:%M')

    is_finished = BooleanField('Работа завершена')

    is_private = BooleanField('Личная работа')

    submit = SubmitField('Сохранить')
