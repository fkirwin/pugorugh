from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from pugorugh.views import UserRegisterView, UserPreferenceSaveView, NextLikedDog, NextDislikedDog, AllDogs, NextUndecidedDog, ChangeUndecidedDog

router = routers.SimpleRouter()
router.register(r'dogs', AllDogs)
# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    path('api/user/preferences/', UserPreferenceSaveView.as_view()),
    path('api/', include(router.urls)), ##use this with the dogs namespace.
    path('api/dog/<int:pk>/liked/next/', NextLikedDog.as_view()),
    path('api/dog/<int:pk>/disliked/next/', NextDislikedDog.as_view()),
    path('api/dog/<int:pk>/undecided/next/', NextUndecidedDog.as_view()),
    path('api/dog/<int:pk>/undecided/', ChangeUndecidedDog.as_view()),
])
