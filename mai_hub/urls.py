from django.urls import path, register_converter
from mai_hub import views
from mai_hub import converters


urlpatterns = [
    path('', views.MaiHubHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.MaiHubCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),

]