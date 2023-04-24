from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('SinhVien', views.SinhVienViewSet)
router.register('LopHoc', views.LopHocViewSet)
router.register('GiangVien', views.GiangVienViewSet)
router.register('MonHoc', views.MonHocViewSet)
router.register('User', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
