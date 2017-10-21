from django.conf.urls import url
from .views import IndexView, LectureView,LectureDetailView


urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r'^lecture/(?P<id>\d+)/$', LectureDetailView.as_view(), name='lecture'),
    url(r'^lectures/$', LectureView.as_view(), name='lectures'),
]
