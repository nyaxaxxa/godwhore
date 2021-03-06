from datetime import datetime

import requests
from flask import render_template, request

from database.vas3kru import vas3k_database, Story
from godmode.models import BaseAdminModel
from godmode.views.view import BaseView

DEFAULT_ANNOUNCE_TEXT = "В эфире программа «дратути»:"


class The365AdminModel(BaseAdminModel):
    db = vas3k_database
    table = Story
    name = "365"
    title = "365"
    place = "navbar"

    class IndexView(BaseView):
        url = "/"
        title = "365"
        template = "plugins/365.html"

        def get(self):
            return self.render()

        def post(self):
            file = request.files["photo"]
            if file.filename == "":
                return render_template("error.html", message="No file")

            title = request.form.get("title")
            announce_text = request.form.get("text")
            telegram_text = request.form.get("telegram_text") or announce_text
            post_to_channel = request.form.get("post_to_channel") or False
            post_to_chat = request.form.get("post_to_chat") or False

            saved_filename = "/tmp/365.{}".format(file.filename[file.filename.rfind(".") + 1:])
            file.save(saved_filename)

            response = requests.post(
                url="http://i.vas3k.ru/upload/",
                files={"image": open(saved_filename, "rb")}
            )

            uploaded_filename = response.json()["uploaded"][0]

            today_date = datetime.now().strftime("%Y-%m-%d")

            if not title:
                title = today_date

            self.model.create(
                slug=today_date,
                type="365",
                title=title,
                author="vas3k",
                image=uploaded_filename,
                text=announce_text or "",
                created_at=datetime.now(),
                views_count=0,
                comments_count=0,
                is_visible=True,
                is_commentable=True,
                is_featured=False,
                is_sexy_title=False
            )

            return render_template("success.html", message="Saved: <a href='http://vas3k.ru/365/{today}/'>http://vas3k.ru/365/{today}/</a>".format(today=today_date))

    list_view = IndexView
