from django.conf.urls import url
from .views import IndexView, LectureView, LectureDetailView, LectureCreateView, LectureQuestionView


urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r'^lectures/$', LectureView.as_view(), name='lectures'),
    url(r'^lectures/create$', LectureCreateView.as_view(), name='create_lecture'),
    url(r'^lectures/(?P<id>\d+)/$', LectureDetailView.as_view(), name='lecture'),
    url(r'^lectures/(?P<id>\d+)/question/$', LectureQuestionView.as_view(), name='question')
]
