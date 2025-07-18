from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from library import views

router = routers.DefaultRouter()
router.register(r"authors", views.AuthorViewSet)
router.register(r"books", views.BookViewSet)
router.register(r"members", views.MemberViewSet)
router.register(r"loans", views.LoanViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/top-active-members/",
        views.TopActiveMembersView.as_view(),
        name="top-active-members",
    ),
]
