from django.urls import path, include
from rest_framework.routers import DefaultRouter

from messagerie.views.notification import NotificationViewSet

from messagerie.views.notification_target import NotificationTargetViewSet

from messagerie.views.classe import ClasseViewSet

from messagerie.views.eleve import EleveViewSet

router = DefaultRouter()

router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notifications-targets', NotificationTargetViewSet, basename='notification-target')
router.register(r'classes', ClasseViewSet, basename='classe')
router.register(r'eleves', EleveViewSet, basename='eleve')

urlpatterns = [

    path('', include(router.urls)),
]