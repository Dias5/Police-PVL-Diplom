from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class PeriodForm(FlaskForm):
    start_date = DateField('Дата начала', validators=[DataRequired()], render_kw={"data-mask": "99-99-9999"})
    end_date = DateField('Дата конца', validators=[DataRequired()], render_kw={"data-mask": "99-99-9999"})
    submit = SubmitField('Показать статистику')
    submit2 = SubmitField('За весь период', render_kw={"formaction": "http://127.0.0.1:5000/statistic"})
