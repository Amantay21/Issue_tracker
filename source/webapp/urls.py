from django.urls import path
from webapp.views import IssueCreateView, \
    IndexView, IssueView, IssueUpdateView, IssueDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/add/', IssueCreateView.as_view(), name='issue_create'),
    path('task/<int:pk>', IssueView.as_view(), name='issue_view'),
    path('task/<int:pk>/update', IssueUpdateView.as_view(), name='issue_update'),
    path('task/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete')
]