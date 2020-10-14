from flask import render_template

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "Esta URL no existe"
    }
    return render_template('error.html', **kwargs), 404

def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a esta URL"
    }
    return render_template('error.html', **kwargs), 401