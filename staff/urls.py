from django.urls import path, include
from . import views

# super admin routes
staff_patterns = ([
    path('', views.index, name="index"),
    path('factory/add/', views.CreateFactoryView.as_view(),
         name="add_factory"),
    path('factories/', views.FactoryListView.as_view(),
         name="factories"),
    path('factories/delete/<int:id>',
         views.FactoryDeleteView.as_view(), name="factory_delete"),
    path('factories/update/<int:pk>',
         views.FactoryUpdateView.as_view(), name="factory_update"),
    path('station_admin/add', views.CreateFactoryAdmin.as_view(),
         name="add_station_admin"),
    path('station_admins/', views.FactoryAdminList.as_view(),
         name="factory_admins_list")
], 'staff')

# factory admin routes
factory_admin = ([
    path('product', views.NewProduct.as_view(), name="add_product"),
    path('products', views.ProductList.as_view(), name="products")
], 'factory_admin')

# factort accountant routes

urlpatterns = [
    path('', include(staff_patterns)),
    path('', include(factory_admin))
]
