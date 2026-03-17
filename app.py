from flask import Flask, render_template, request, redirect, url_for
#from flask_wtf.csrf import CSRFProtect
#from config import DevelopmentConfig
#from models import db
#from flask_migrate import Migrate


app = Flask(__name__)
#app.config.from_object(DevelopmentConfig)


@app.route("/")
def index():
    return render_template("index.html")




if __name__ == '__main__':
# csrf.init_app(app)
#with app.app_context():
#db.create_all()

    app.run(debug=True)