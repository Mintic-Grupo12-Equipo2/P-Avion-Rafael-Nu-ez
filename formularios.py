from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class formularioMensaje(FlaskForm):
    para = StringField('Para:', validators=[DataRequired(message='Por favor llenar este campo.')])
    asunto = StringField('Asunto:', validators=[DataRequired(message='Por favor llenar este campo.')])
    mensaje = StringField('Mensaje:', validators=[DataRequired(message='Por favor llenar este campo.')])
    enviar = SubmitField('Enviar Mensaje')