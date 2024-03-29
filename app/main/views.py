from flask import current_app, redirect, render_template, session, url_for

from . import main
from .forms import NameForm
from .. import db
from ..email import send_mail
from ..models import User


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        session["known"] = True
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            if current_app.config["FLASKY_ADMIN"]:
                send_mail(
                    to=current_app.config["FLASKY_ADMIN"],
                    subject="New User",
                    template="mail/new_user",
                    user=user,
                )
        session["name"] = form.name.data
        return redirect(url_for(".index"))
    return render_template(
        "index.html", form=form, name=session.get("name"), known=session.get("known")
    )
