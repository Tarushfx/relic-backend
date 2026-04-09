from django.urls import path

from logs.serializers.serializers import LogTableSerializer
from logs.views import (
    LogEntryDetailUpdateDeleteView,
    LogDefinitionCreateDeleteView,
    LogTableView,
    ActivityView,
)

urlpatterns = [
    path("entries/", LogEntryDetailUpdateDeleteView.as_view(), name="get-log-entry"),
    path(
        "entries/<int:id>/",
        LogEntryDetailUpdateDeleteView.as_view(),
        name="get-post-patch-delete-log-entry-detail",
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
