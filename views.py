import functools
from formularios import formularioMensaje
from flask import Flask, render_template, blueprints, request, redirect, url_for,session, flash, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db



main= blueprints.Blueprint('main', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)

    return wrapped_view




@main.route( '/' )
def hello_world():
    """Función que maneja la raiz del sitio web.

        Parameters:
        Ninguno

        Returns:
        Plantilla inicio.html

    """

    return render_template('inicio.html')

@main.route('/DashboardCrearVuelos/')
@login_required
def DashboardCrearVuelos():

    return render_template('DashboardCrearVuelos.html')


@main.route('/DashboardPasajero/')
@login_required
def DashboardPasajero():

    return render_template('DashboardPasajero.html')

@main.route('/DashboardSuper/')
@login_required
def DashboardSuper():

    return render_template('DashboardSuper.html')


@main.route('/DashboardPiloto/')
@login_required
def DashboardPiloto():

    return render_template('DashboardPiloto.html')


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """Función que maneja la ruta login.Responde a los métodos GET y POST.

        Parameters:
        Ninguno

        Returns:
        login.html si es invocada con el método GET. 
        Redirecciona a  main.ajax si es invocada con POST y la validación es verdadera.

    """

    if request.method =='POST':

        usuario = request.form['username']
        clave = request.form['userPassword']
        db = get_db()
        #sql = "select * from usuario where usuario = '{0}' and clave= '{1}'".format(usuario, clave)

        user = db.execute('select * from usuario where username = ? ', (usuario,)).fetchone()
        db.commit()
        db.close()
        if user is not None:

            print(user[4])
            clave = clave + usuario
            
            sw = check_password_hash(user[4], clave)

            if(sw):

                session['nombre'] = user[1]
                session['usuario'] = user[2]
                if user[5] == 0:
                 return redirect(url_for('main.DashboardSuper'))
                elif  user[5] == 1:
                 return redirect(url_for('main.DashboardPiloto'))   
                elif  user[5] == 2:
                 return redirect(url_for('main.DashboardPasajero')) 

        flash('Usuario o clave incorrecto.')
    return render_template('login.html')


@main.route('/registro/', methods=['GET', 'POST'])
def registro():
    """Función que maneja la ruta Registro.Responde a los métodos GET y POST.

        Parameters:
        Ninguno

        Returns:
        registro.html si es invocada con el método GET. 
        Crea un usuario en la BD si es invocada con POST, no tiene válidaciones.

    """
   
    if request.method == 'POST' :

        nombre = request.form['nombre']
        usuario = request.form['username']
        correo = request.form['correo']
        clave = request.form['contraseña']
        t_user = "2"
        

        db = get_db()
        #agregar SLAT
        clave = clave + usuario
        clave = generate_password_hash(clave)
        db.execute("insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.registro'))

    elif  request.method == 'GET':       
        
       return render_template('registro.html')
   
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))





