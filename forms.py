from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LevelForm(FlaskForm):
    title = StringField('Название уровня', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание')
    order = IntegerField('Порядок', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Сохранить')


class SectionForm(FlaskForm):
    title = StringField('Название раздела', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание')
    order = IntegerField('Порядок', validators=[DataRequired(), NumberRange(min=1)])
    level_id = SelectField('Уровень', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class LessonForm(FlaskForm):
    title = StringField('Название урока', validators=[DataRequired(), Length(max=200)])
    theory_content = TextAreaField('Теоретический материал')
    order = IntegerField('Порядок', validators=[DataRequired(), NumberRange(min=1)])
    section_id = SelectField('Раздел', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class QuestionForm(FlaskForm):
    text = TextAreaField('Вопрос', validators=[DataRequired()])
    option_a = StringField('Вариант A', validators=[DataRequired(), Length(max=500)])
    option_b = StringField('Вариант B', validators=[DataRequired(), Length(max=500)])
    option_c = StringField('Вариант C', validators=[DataRequired(), Length(max=500)])
    option_d = StringField('Вариант D', validators=[DataRequired(), Length(max=500)])
    correct_answer = SelectField('Правильный ответ', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], validators=[DataRequired()])
    order = IntegerField('Порядок', validators=[DataRequired(), NumberRange(min=1)])


class ExerciseForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    solution = TextAreaField('Решение')
    order = IntegerField('Порядок', validators=[DataRequired(), NumberRange(min=1)])
