from application import create_app
from hashids import Hashids
from application import Config
from flask import render_template

app = create_app()

hashids = Hashids(salt=Config.SECRET_URLSALT, min_length=16)


@app.template_filter('urlencrypt')
def urlencrypt(value):
    encrypt = hashids.encode(value)
    return encrypt


@app.errorhandler(404)
def resource_not_found(e):
    return render_template('page404.html', etype='404', message='Sorry Page Not Found')


if __name__ == "__main__":
    app.run(debug=True)
