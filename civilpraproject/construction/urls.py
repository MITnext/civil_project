from django.urls import path
from . import views

urlpatterns = [

    path('createcustomer', views.createcustomer),
    path('searchcustomer', views.searchcustomer),
    path('updatecustomer/<int:id>', views.updatecustomer),
    path('deletecustomer/<int:id>', views.deletecustomer),

    path('createsite', views.createsite),
    path('searchsite', views.searchsite),
    path('updatesite/<int:id>', views.updatesite),
    path('deletesite/<int:id>', views.deletesite),

    path('creatematerial', views.creatematerial),
    path('searchmaterial', views.searchmaterial),
    path('updatematerial/<int:materialid>', views.updatematerial),
    path('deletematerial/<int:materialid>', views.deletematerial),


    path('createconstructionlevel', views.createconstructionlevel),
    path('searchconstructionlevel', views.searchconstructionlevel),
    path('updateconstructionlevel/<int:id>', views.updateconstructionlevel),
    path('deleteconstructionlevel/<int:id>', views.deleteconstructionlevel),

    path('createcategory', views.createcategory),
    path('searchcategory', views.searchcategory),
    path('updatecategory/<int:categoryid>', views.updatecategory),
    path('deletecategory/<int:categoryid>', views.deletecategory),

    path('createunit', views.createunitmeasurement),
    path('searchunit', views.searchunitmeasurement),
    path('updateunit/<int:unitmeasurementid>', views.updateunitmeasurement),
    path('deleteunit/<int:unitmeasurementid>', views.deleteunitmeasurement),

    path('createbrand', views.createbrand),
    path('searchbrand', views.searchbrand),
    path('updatebrand/<int:id>', views.updatebrand),
    path('deletebrand/<int:id>', views.deletebrand),

    path('createworktype', views.createworktype),
    path('searchworktype', views.searchworktype),
    path('updateworktype/<int:worktypeid>', views.updateworktype),
    path('deleteworktype/<int:worktypeid>', views.deleteworktype),


    path('construction_type/', views.constypeview),

    path('vendor-registration/', views.vendor_registration),
    path('rough_drawing/', views.roughdrawing),
    path('final_drawing/', views.finaldrawing),

    path('task_assignmenttran/', views.assign_view),
    path('get_sites/<int:customer_id>/', views.get_sites, name='get_sites'),

    path('search_masterdata', views.search_assignmasterdata),
    path('update_masterdata/<int:id>', views.update_masterdata),
    path('delete_masterdata/<int:id>', views.delete_masterdata),

    path('oooooo', views.work_progress_list, name='work_progress_list'),
    path('progress/', views.add_work_progress, name='add_work_progress'),

    path('tasks_search/', views.customer_site_task_list, name='customer_site_task_list'),
    path('assignee_tasks/', views.assignee_task_list, name='assignee_task_list'),

    # **************************************************************************


    path('createaddmaterial', views.createaddmaterial),

    path('createinternaltransfer/', views.createinternaltransfer, name='createinternaltransfer'),
    path('get_brands_by_material/', views.get_brands_by_material, name='get_brands_by_material'),
    path('searchinternaltransfer/',views.searchinternaltransfer),
    path('updateinternaltransfer/<int:id>', views.updateinternaltransfer),
    path('deleteinternaltransfer/<int:id>', views.deleteinternaltransfer),


    path('createempregistration', views.createempregistration),
    path('searchempregistration',views.searchempregistration),


    path('client_reg/', views.clientregview),
    path('search_clientreg', views.search_clientregs),
    path('update_clientreg/<int:id>', views.update_clientreg),
    path('delete_clientreg/<int:id>', views.delete_clientreg),


    path('client_inquiry/', views.clientinquirygview, name='client_inquiry_form'),
    path('get_representatives/', views.get_representatives, name='get_representatives'),
    path('search_clientinquiry', views.search_clientinq),
    path('update_clientinquiry/<int:id>', views.update_clientinq),
    path('delete_clientinquiry/<int:id>', views.delete_clientinq),

]