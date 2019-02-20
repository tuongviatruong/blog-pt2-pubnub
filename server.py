# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

from flaskblog import app


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
