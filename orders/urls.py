from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('<int:item_id>/review', views.review, name="review"),
    path("tree", views.tree, name="tree"),
    path("wreath", views.wreath, name="wreath"),
    path("garland", views.garland, name="garland"),
    path("centerpiece", views.centerpiece, name="centerpiece"),
    path("miniTree", views.miniTree, name="miniTree"),
    path("stand", views.stand, name="stand"),
    path("<str:size>/lights", views.lights, name="lights"),
    path("treeSkirt", views.treeSkirt, name="treeSkirt"),
    path("<str:size>/runner", views.runner, name="runner"),
    path("<str:size>/ribbon", views.ribbon, name="ribbon"),
    path("<str:size>/angel", views.angel, name="angel"),
    path("<str:size>/star", views.star, name="star"),
    path("<str:size>/bow", views.bow, name="bow"),
    path("bulb", views.bulb, name="bulb"),
    path("<str:size>/bells", views.bells, name="bells"),
    path("viewOrder", views.view_order, name="viewOrder"),
    path("viewCart", views.view_cart, name="viewCart"),
    path("placeOrder", views.place_order, name="placeOrder"),
    path('<int:order_id>/orderStatus', views.order_status, name="orderStatus"),
]
