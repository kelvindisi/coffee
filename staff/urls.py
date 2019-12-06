from django.urls import path, include
from . import views

# super admin routes
staff_patterns = ([
    path('', views.HomeView.as_view(), name="index"),
    path('factory/add/', views.CreateFactoryView.as_view(),
         name="add_factory"),
    path('factories/', views.FactoryListView.as_view(),
         name="factories"),
    path('factories/delete/<int:id>',
         views.FactoryDeleteView.as_view(), name="factory_delete"),
    path('factories/update/<int:pk>',
         views.FactoryUpdateView.as_view(), name="factory_update"),
    path('factory_admin/add/', views.CreateFactoryAdmin.as_view(),
         name="add_station_admin"),
    path('factory_admins/', views.FactoryAdminList.as_view(),
         name="factory_admins_list"),
    path('delete_factory_admin/<int:pk>/', views.DeleteFactoryStaff.as_view(),
         name="delete_factory_admin"),
    path('edit_factory_admin/<int:pk>/',
         views.EditFactoryStaff.as_view(), name="edit_factory_admin"),
    path('profile/',
         views.ProfileView.as_view(), name="profile")
], 'staff')

# factory admin routes
factory_admin = ([
    path('product', views.NewProduct.as_view(), name="products_schedule"),
    path('product_reject/', views.RejectProduct.as_view(), name="product_reject"),
    path('product_reject_accepted/',
         views.ReRejectProduct.as_view(), name="re_product_reject"),
    path('schedule_date/<int:pk>/',
         views.AddScheduleDate.as_view(), name="schedule_product"),
    path('products_scheduled/', views.ScheduledProduct.as_view(), name="scheduled"),
    path('products_collected/', views.CollectedProduct.as_view(), name="collected"),
    path('products_collect/<int:pk>/',
         views.CollectProductView.as_view(), name="product_collect"),
    path('accountant', views.CreateFactoryStaff.as_view(), name="add_accountant"),
    path('staff_list', views.FactoryStaffList.as_view(), name="staff_list"),
    path('staff/<int:pk>/delete',
         views.DeleteStaffMember.as_view(), name="delete_staff"),

], 'factory_admin')

# factort accountant routes
factory_accountant = ([
    path('transact/<int:product>', views.MakePayDeposit.as_view(), name="transact"),
    path('payment_history', views.PaymentHistory.as_view(), name="payment_history"),
    path('pending_balances', views.PendingBalances.as_view(), name="balances")
], 'accountant')
urlpatterns = [
    path('', include(staff_patterns)),
    path('', include(factory_admin)),
    path('', include(factory_accountant))
]
