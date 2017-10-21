from django.conf.urls import url
from .views import IndexView, LectureView,LectureDetailView


urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r'^lectures/$', LectureView.as_view(), name='lectures'),
    url(r'^lectures/(?P<id>\d+)/$', LectureDetailView.as_view(), name='lecture'),
]
