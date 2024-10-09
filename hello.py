from flask import Flask, render_template, url_for, request
from markupsafe import escape
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Filtros personalizados
@app.add_template_filter
def today(date):
    return date.strftime('%d-%m-%Y')

#app.add_template_filter('today', today)

# Funciones personalizadas
@app.add_template_global
def repeat(text, n):
    return text * n

#app.add_template_global('repeat', repeat)

@app.route('/')
@app.route('/index')
def index():
    name = 'Seba'
    friends = ['Maria', 'Juan', 'Luis']
    date = datetime.now()
    return render_template(
        'index.html',
        name = name,
        friends = friends,
        date = date
        )

@app.route('/hello')
@app.route('/hello/<name>')
@app.route('/hello/<name>/<int:age>')
@app.route('/hello/<name>/<int:age>/<email>')
def hello(name = None, age = None, email = None):
    my_data = {
        'name': name,
        'age': age,
        'email': email
    }
    return render_template('hello.html', data = my_data)
    
# Escapar html para evitar ataques de inyección de código
@app.route('/code/<path:code>')
def code(code):
    return f'<code>{escape(code)}</code>'

# Crear formulario con wtforms
class RegistrationForm(FlaskForm):
    name = StringField('Nombre: ', validators=[
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    email = StringField('Correo electrónico: ', validators=[
        validators.Length(min=6, max=25),
        validators.DataRequired()
    ])
    password = PasswordField('Contraseña: ', validators=[
        validators.Length(min=6, max=40),
        validators.DataRequired()
    ])
    submit = SubmitField('Registrar')

# Registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        return f'Tu nombre es {name}, tu correo es {email} y tu contraseña es {password}'
    # if request.method == 'POST':
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password']
    #     if len(name) > 3 and len(name) <= 25 and len(password) >= 6 and len(password) <= 40:
    #         return f'Tu nombre es {name}, tu correo es {email} y tu contraseña es {password}'
    #     else:
    #         error = 'Tu nombre debe tener entre 4 y 25 caracteres y tu contraseña debe tener entre 6 y 40 caracteres'
    #         return render_template('auth/register.html', error = error, form = form)
    return render_template('auth/register.html', form = form)