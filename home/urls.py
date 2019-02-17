from django.urls import path, re_path

from home import views
from home.views import HomeView, UpdateChildView, DeleteChildView, AddFullTermChildView, \
    AddPreemieView, AddNotBornView, UpdateSizeSystemView, UpdateSizesView, UpdateShoeSizesView, \
    AddSectionView, AddCategoryView, UpdateCategoryView, UpdateSectionView, DeleteSectionView, \
    DeleteCategoryView, AddItemsView, ItemsView, \
    UpdateItemView, DeleteItemView, PhotoView, UpdateShoeFilterSizesView, UpdateClothingFilterSizesView, \
    AllItemsView, ShareChildView, SharedWithMe, \
    SharedHomeView, UpdateSharedClothingFilterSizesView, UpdateSharedShoeFilterSizesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>/', HomeView.as_view(), name='home'),
    path('shared-child/<int:pk>/<slug:slug>/', SharedHomeView.as_view(), name='shared-home-view'),
    path('add_child/', AddFullTermChildView.as_view(), name='add_child'),
    path('add_preemie/', AddPreemieView.as_view(), name='add_preemie'),
    path('add_not_born/', AddNotBornView.as_view(), name='add_not_born'),
    path('details_child/<int:pk>/', UpdateChildView.as_view(), name='update_child'),
    path('share/<int:pk>/', ShareChildView.as_view(), name='update_share'),
    path('share_child_with/', views.share_child_with, name='share_child_with'),
    path('share_privileges/', views.change_share_privileges, name='change_share_privileges'),
    path('shared_with_me/', SharedWithMe.as_view(), name='shared_with_me'),
    path('size_system/<int:pk>/', UpdateSizeSystemView.as_view(), name='update_size_system'),
    path('sizes_update/<int:pk>/', UpdateSizesView.as_view(), name='update_sizes'),
    path('shoe_sizes_update/<int:pk>/', UpdateShoeSizesView.as_view(), name='update_shoe_sizes'),
    re_path(r'del_child/(?P<pk>\d+)/$', DeleteChildView.as_view(), name='del_child'),
    path('add_section/<int:pk>/', AddSectionView.as_view(), name='add_section'),
    path('add_category/<int:pk>/', AddCategoryView.as_view(), name='add_category'),
    path('update_category/<int:pk>/', UpdateCategoryView.as_view(), name='update_category'),
    path('update_section/<int:pk>/', UpdateSectionView.as_view(), name='update_section'),
    re_path(r'delete_section/(?P<pk>\d+)/$', DeleteSectionView.as_view(), name='delete_section'),
    re_path(r'delete_category/(?P<pk>\d+)/$', DeleteCategoryView.as_view(), name='delete_category'),
    path('add_items/<int:pk>/', AddItemsView.as_view(), name='add_items'),
    path('delete-items/', views.delete_items, name='delete_items'),
    path('move-items/', views.move_items, name='move_items'),
    path('move-items-to/', views.move_items_to_another_child, name='move_items_to_another_child'),
    # path('delete_items/<int:pk>/', DeleteItemsView.as_view(), name='delete_items'),
    path('list_items/<int:pk>/', ItemsView.as_view(), name='items_list'),
    path('list_items/<int:pk>/<slug:slug>/', ItemsView.as_view(), name='items_list'),
    path('list_all_items/<int:pk>/', AllItemsView.as_view(), name='all_items_list'),
    path('update_item/<int:pk>/', UpdateItemView.as_view(), name='update_item'),
    path('update_item/<int:pk>/<slug:slug>/', UpdateItemView.as_view(), name='update_item_from_all_items'),
    re_path(r'del_item/(?P<pk>\d+)/$', DeleteItemView.as_view(), name='del_item'),
    path('del_item/<int:pk>/<slug:slug>/', DeleteItemView.as_view(), name='del_item_from_all_items'),
    path('crop/<int:pk>/', PhotoView.as_view(), name='crop-photo'),
    path('update_shoe_filter_size/<int:pk>/', UpdateShoeFilterSizesView.as_view(),
         name='update_shoe_filter_size'),
    path('update_shared_shoe_filter_size/<int:pk>/', UpdateSharedShoeFilterSizesView.as_view(),
         name='update_shared_shoe_filter_size'),
    path('update_shoe_filter_size/<int:pk>/<int:category_pk>/', UpdateShoeFilterSizesView.as_view(),
         name='update_shoe_filter_size'),
    path('update_shared_shoe_filter_size/<int:pk>/<int:category_pk>/', UpdateSharedShoeFilterSizesView.as_view(),
         name='update_shared_shoe_filter_size'),
    path('update_clothing_filter_size/<int:pk>/', UpdateClothingFilterSizesView.as_view(),
         name='update_clothing_filter_size'),
    path('update_clothing_filter_size/<int:pk>/<int:category_pk>/', UpdateClothingFilterSizesView.as_view(),
         name='update_clothing_filter_size'),
    path('update_shared_clothing_filter_size/<int:pk>/', UpdateSharedClothingFilterSizesView.as_view(),
         name='update_shared_clothing_filter_size'),
    path('update_shared_clothing_filter_size/<int:pk>/<int:category_pk>/', UpdateSharedClothingFilterSizesView.as_view(),
         name='update_shared_clothing_filter_size'),
    # path('update_shoe_filter_size_second/<int:pk>/<int:category_pk>/', UpdateShoeFilterSizesSecondView.as_view(),
    #      name='update_shoe_filter_size_second'),
    # path('update_clothing_filter_size_second/<int:pk>/<int:category_pk>/', UpdateClothingFilterSizesSecondView.as_view(),
    #      name='update_clothing_filter_size_second'),

]
