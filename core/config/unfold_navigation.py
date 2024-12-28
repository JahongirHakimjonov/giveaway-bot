from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Foydalanuvchilar"),
        "items": [
            {
                "title": _("Guruhlar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Bot Foydalanuvchilari"),
        "items": [
            {
                "title": _("Bot Foydalanuvchilari"),
                "icon": "smart_toy",
                "link": reverse_lazy("admin:support_botusers_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_botusers"
                ),
            },
            {
                "title": _("Kanallar"),
                "icon": "star_half",
                "link": reverse_lazy("admin:support_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Yangilik"),
                "icon": "brand_awareness",
                "link": reverse_lazy("admin:support_news_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_news"
                ),
            },
        ],
    },
]
