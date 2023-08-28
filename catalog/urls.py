from django.urls import path
from catalog.views import HomeView, ContactsView, ProductsView, CategoryProductsView, ProductDetailsView, \
    CreateProductView, BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/', ProductsView.as_view(), name='products'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/create/', CreateProductView.as_view(), name='product_create'),

    path('blog/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blog/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blog/view/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_view'),
    path('blog/edit/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('blog/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),

]
