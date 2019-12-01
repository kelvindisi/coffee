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
    path('station_admin/add/', views.CreateFactoryAdmin.as_view(),
         name="add_station_admin"),
    path('station_admins/', views.FactoryAdminList.as_view(),
         name="factory_admins_list"),
    path('delete_factory_admin/<int:pk>/', views.DeleteFactoryStaff.as_view(),
         name="delete_factory_admin"),
     path('edit_factory_admin/<int:pk>/', views.EditFactoryStaff.as_view(), name="edit_factory_admin")
], 'staff')

# factory admin routes
factory_admin = ([
    path('product', views.NewProduct.as_view(), name="products_schedule"),
    path('product_reject/', views.RejectProduct.as_view(), name="product_reject"),
    path('schedule_date/<int:pk>/', views.AddScheduleDate.as_view(), name="schedule_product"),
    path('products_scheduled/', views.ScheduledProduct.as_view(), name="scheduled"),
    path('accountant', views.CreateFactoryStaff.as_view(), name="add_accountant"),
    path('staff_list', views.FactoryStaffList.as_view(), name="staff_list"),
    
], 'factory_admin')

# factort accountant routes

urlpatterns = [
    path('', include(staff_patterns)),
    path('', include(factory_admin))
]
