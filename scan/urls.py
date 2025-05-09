from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    scanning_and_dividing,
    success, homepage,
    profile,
    local_check,
    session
)

app_name = "scan"

urlpatterns = [
    path('', homepage, name='homepage'),
    path('scaner/<pk>', scanning_and_dividing, name='image_upload'),
    path('success', success, name='success'),
    path('profile/', profile, name="profile"),
    path('localcheck/', local_check, name="local_check"),
    path('session/', session, name="session"),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
