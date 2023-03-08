from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired

class MovimientoForm(FlaskForm):
    id = HiddenField()
    fecha = DateField('Fecha', validators=[DataRequired(message="Debes introducir una fecha")])
    concepto = StringField('Concepto', validators=[DataRequired(message="Debes especificar un concepto")])
    tipo = RadioField(choices=[('I', 'Ingreso'), ('G', 'Gasto')], validators=[DataRequired(message="Indica si es un gasto o un ingreso")])
    cantidad = FloatField('Cantidad', validators=[DataRequired(message="Indica una cantidad")])

    submit = SubmitField('Guardar')