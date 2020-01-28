import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    birthday = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    address = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name, self.birthday, self.address)


@app.route("/", methods=["GET", "POST"])
def home():
    users = None
    if request.form:
        try:
            user = User(name=request.form.get("name"), birthday=request.form.get("birthday"), address=request.form.get("address"))
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print("Failed to add user")
            print(e)
    users = User.query.all()
    return render_template("home.html", users=users)


@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")

        newbirthday = request.form.get("newbirthday")
        oldbirthday = request.form.get("oldbirthday")

        newaddress = request.form.get("newaddress")
        oldaddress = request.form.get("oldaddress")

        user = User.query.filter_by(name=oldname).first()
        user.name = newname
        user.birthday = newbirthday
        user.address = newaddress
        db.session.commit()
    except Exception as e:
        print("Couldn't update user name")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    user = User.query.filter_by(name=name).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8087, debug=True)
