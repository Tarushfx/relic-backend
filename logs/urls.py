from django.urls import path

from logs.serializers.serializers import LogTableSerializer
from logs.views import (
    LogEntryDetailUpdateDeleteView,
    LogTableView,
    ActivityView,
)

urlpatterns = [
    path(
        "entries/", LogEntryDetailUpdateDeleteView.as_view(), name="get-log-list-entry"
    ),
    path(
        "entries/<int:id>/",
        LogEntryDetailUpdateDeleteView.as_view(),
        name="get-patch-delete-log-entry-detail",
    ),
    path(
        "table/<int:id>/entries/",
        LogEntryDetailUpdateDeleteView.as_view(),
        name="post-entry",
    ),
    path("activity/", ActivityView.as_view(), name="activity-list"),
    path(
        "table/",
        LogTableView.as_view(),
        name="get-table-list",
    ),
    path(
        "table/<int:id>/",
        LogTableView.as_view(),
        name="get-post-patch-delete-table-detail",
    ),
]
