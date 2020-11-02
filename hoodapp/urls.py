from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [


    url(r'^$', views.homepage, name='home'),
    url(r'^add/hood$', views.add_hood, name='add_hood'),
    url(r'^join_hood/(\d+)', views.join_hood, name='join_hood'),
    url(r'^exit_hood/(\d+)', views.leave_hood, name='leave_hood'),
    url(r'^add/business$', views.add_biz, name='add_business'),
    url(r'^add/post$', views.add_post, name='add_post'),

    # url(r'^hood/(?P<biz_hood>\d+)', views.view_biz, name='businesses'),

    # url(r'^accounts/profile/(?P<username>\w+)', views.profile, name='my_profile'),
    url(r'^search_results/', views.search_results, name='search_results'),
    # url(r'^like/(?P<operation>.+)/(?P<pk>\d+)',views.like, name='like'),
    url(r'^user/(?P<username>\w+)', views.user_profile, name='user_profile'),
    # url(r'^comment/(?P<pk>\d+)',views.add_comment,name='comment'),
    url(r'^new/profile$', views.add_profile, name='add_profile'),
    # url(r'^follow/(?P<operation>.+)/(?P<id>\d+)', views.follow, name='follow'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)