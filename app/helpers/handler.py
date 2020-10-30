from flask import render_template, jsonify


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "Esta URL no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a esta URL",
    }
    return render_template("error.html", **kwargs), 401


def internal_server_error_api(e):
    return jsonify({"msg": "Internal server error"}), 500


def bad_request_error_api(e):
    return jsonify({"msg": "Bad Request"}), 400


# def not_found_error_api(e):
#    return jsonify({'msg': 'Not Found error'}), 404    # No activar, choca con el 404 original
