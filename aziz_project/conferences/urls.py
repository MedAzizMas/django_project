from django.urls import path
from .views import *
urlpatterns = [
    path("list/",conferencelist,name ="listeconf"),
    path("listviewconference/",ConferenceListView.as_view(),name ="listeconfview"),
    path("listdetailconference/<int:pk>/",DetailViewConference.as_view(),name ="listeconfdetail")
]
