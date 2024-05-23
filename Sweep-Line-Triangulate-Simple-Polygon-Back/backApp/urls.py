from django.urls import path

from .views import getName, main, triangulate_polygon_view

urlpatterns = [
    path("", main),
    path("name", getName),
    path("triangulate-polygon/", triangulate_polygon_view),
]
