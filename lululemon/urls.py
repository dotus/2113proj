from django.urls import path
from lululemon import views
from lululemon.models import LogMessage
from lululemon.views import profile, RegisterView
from lululemon.forms import LoginForm
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import ItemListCreateView, ItemUpdateView

home_list_view = views.HomeListView.as_view (
    queryset=LogMessage.objects.order_by("-log_date") [:5], 
    context_object_name="message_list",
    template_name="lululemon/home.html",
)
urlpatterns = [
    path("", home_list_view, name="home"),
    path("log/", views.log_message, name="log"),
    path("about/", views.about, name="about"), 
    path("contact/", views.contact, name="contact"),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='lululemon/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="lululemon/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='lululemon/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('items/', views.item_list, name='item_list'),
    path('item/<uuid:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_new, name='item_new'),
    path('item/<uuid:pk>/edit/', views.item_edit, name='item_edit'),
    path('item/<uuid:pk>/delete/', views.item_delete, name='item_delete'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    # path('items/inventory_management/', InventoryManagementView.as_view(), name='inventory_management')
    path('inventory_management/', views.inventory_management, name='inventory_management'),
    #path('items/<int:pk>/check-in/', views.check_in_item, name='check-in_item'),
    #path('items/<int:pk>/check-out/', views.check_out_item, name='check-out_item'),
    path('api/items/', views.create_item, name='create_item'),
    path('api/items/<uuid:pk>/', ItemUpdateView.as_view(), name='item-update'),
    path('api/items/update_quantity/<uuid:pk>/', views.update_product_quantity, name='update_product_quantity'),
]

