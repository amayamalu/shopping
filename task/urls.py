"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegistrationView.as_view(), name='register'),
    path('product/add/',views.ProductCreateView.as_view(),name="product"),
    path('product/all/',views.ProductListView.as_view(),name="list"),
    path('product/detail/<int:pk>/',views.ProductDetailView.as_view(),name="detail"),
    path('product/edit/<int:pk>/',views.ProductEditView.as_view(),name="edit"),
    path('product/delete/<int:pk>/',views.ProductDeleteView.as_view(),name="delete"),




    path('login/',views.SignInView.as_view(), name='login'),
    path('cart/',views.CartView, name='cart_view'),
    path('products/',views.ManageProductsView, name='manage_products'),
    path('add_to_cart/<int:product_id>/',views.AddToCartView, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/',views.RemoveFromCartView, name='remove_from_cart'),
    path('update_cart_quantity/<int:cart_id>/<int:quantity>/',views.UpdateCartQuantityView, name='update_cart_quantity'),


] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


