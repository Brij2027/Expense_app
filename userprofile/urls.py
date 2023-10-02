from django.urls import path

from .views import ProfileRegisterView, ProfileUpdateView
from utils import UrlUtils

urlpatterns = [
    path("create/", ProfileRegisterView.as_view(), name=UrlUtils.PROFILE_CREATE),
    path("get_or_update/<int:pk>/", ProfileUpdateView.as_view(), name=UrlUtils.PROFILE_GET_OR_UPDATE)
]