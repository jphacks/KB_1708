from django.conf.urls import url
from .views import IndexView, LectureView, LectureDetailView, LectureCreateView, LectureQuestionView, TaskView, CameraCalibration


urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r'^lectures/$', LectureView.as_view(), name='lectures'),
    url(r'^lectures/create$', LectureCreateView.as_view(), name='create_lecture'),
    url(r'^lectures/(?P<id>\d+)/$', LectureDetailView.as_view(), name='lecture'),
    url(r'^lectures/(?P<id>\d+)/question/$', LectureQuestionView.as_view(), name='question'),
    url(r'^tasks/$', TaskView.as_view(), name='tasks'),
    url(r'^calibrate/$', CameraCalibration.as_view(), name='calibration')
]
