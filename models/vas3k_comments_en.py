from database.vas3kru import CommentEN, vas3k_database
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
from godmode.widgets.base import BaseWidget
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class AvatarWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        return """<div style="display: inline-block; width: 40px; height: 40px; background-repeat: no-repeat; background-size: cover; border-radius: 50%%; background-image: url('http://vas3k.ru/static/images/avatars/%s');"></div>""" % item.avatar


class CommentENAdminModel(BaseAdminModel):
    db = vas3k_database
    table = CommentEN
    name = "comments_en"
    title = "Комментарии EN"
    icon = "icon-post"
    group = Vas3kGroup
    index = 800
    ordering = CommentEN.created_at.desc()
    widgets = {
        "avatar": AvatarWidget,
        "text": LongTextWidget
    }

    class CommentListView(BaseListView):
        fields = [
            "id", "avatar", "author", "text", "ip", "rating", "is_visible"
        ]

    list_view = CommentListView

    details_view = None
