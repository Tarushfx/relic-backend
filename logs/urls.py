from django.urls import path

from logs.serializers.serializers import LogTableSerializer
from logs.views import (
    LogEntryDetailUpdateDeleteView,
    LogDefinitionCreateDeleteView,
    LogTableView,
    ActivityView,
)

urlpatterns = [
    path(
        "entries/", LogEntryDetailUpdateDeleteView.as_view(), name="log-get-post-list"
    ),
    path(
        "entries/<int:id>/",
        LogEntryDetailUpdateDeleteView.as_view(),
        name="log-patch-detail",
    ),
    path("activity/<int:user_id>/", ActivityView.as_view(), name="activity-list"),
    path(
        "table/",
        LogDefinitionCreateDeleteView.as_view(),
        name="log-entry-definition-list",
    ),
    path(
        "table/<int:id>/",
        LogTableView.as_view(),
        name="log-entry-definition-detail",
    ),
]
