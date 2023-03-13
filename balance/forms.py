from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, RadioField, StringField, SubmitField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired

class MovimientoForm(FlaskForm):
    id = IntegerField(default=0, widget=HiddenInput())
    
    fecha = DateField('Fecha', validators=[DataRequired(message="Debes introducir una fecha")])
    concepto = StringField('Concepto', validators=[DataRequired(message="Debes especificar un concepto")])
    tipo = RadioField(choices=[('I', 'Ingreso'), ('G', 'Gasto')], validators=[DataRequired(message="Indica si es un gasto o un ingreso")])
    cantidad = FloatField('Cantidad', validators=[DataRequired(message="Indica una cantidad")])

    submit = SubmitField('Guardar')