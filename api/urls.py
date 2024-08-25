from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import NoteViewsSet, NoteAccessView

router_v1 = DefaultRouter()
router_v1.register(r'notes', NoteViewsSet, basename='note')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
    path(
        'v1/note-access/', NoteAccessView.as_view(), name='noteaccess'
    )
]
