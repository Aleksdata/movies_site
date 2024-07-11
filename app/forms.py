from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, regexp


class ReviewForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message="Поле не должно быть пустым"),
                                                Length(max=255, message='Введите имя длиной до 255 символов')])
    text = TextAreaField('Текст отзыва', validators=[DataRequired(message="Поле не должно быть пустым")])
    score = SelectField('Оценка',
                        choices=[(str(i), str(i)) for i in range(1, 11)],
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    submit = SubmitField('Добавить отзыв')


class MovieForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(message="Поле не должно быть пустым"),
                                                Length(max=255, message='Введите имя длиной до 255 символов')])
    description = TextAreaField('Описание', validators=[DataRequired(message="Поле не должно быть пустым")])
    image = FileField('Изображение', [
        DataRequired(message="Поле не должно быть пустым"),])
    submit = SubmitField('Добавить фильм')
