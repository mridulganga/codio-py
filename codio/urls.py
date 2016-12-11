from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^view/single/$', RedirectView.as_view(url='/view/single/1')),
    url(r'^view/single/(?P<code_id>\w+)/$', views.code_single, name='code_single'),

    url(r'^view/search/$', views.search, name='search'),
    url(r'^view/search/tag/(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^view/search/lang/(?P<lang>\w+)/$', views.search_lang, name='search_lang'),
    url(r'^view/search/dev/(?P<dev>\w+)/$', views.search_dev, name='search_dev'),

    url(r'^view/$', RedirectView.as_view(url='/view/list')),
    url(r'^view/list/$', views.code_list, name='code_list'),

    url(r'^edit/code/(?P<code_id>\w+)/$', views.edit_code, name='edit_code'),
    url(r'^remove/code/(?P<code_id>\w+)/$', views.remove_code, name='remove_code'),

    url(r'^user/profile/$', views.user_profile, name='user_profile'),
    url(r'^user/submissions/$', views.user_codes, name='user_codes'),

    url(r'^user/(?P<user_id>\w+)/profile/$', views.user_profile, name='user_profile'),
    url(r'^user/(?P<user_id>\w+)/submissions/$', views.user_codes, name='user_codes'),

    url(r'^submit-code/$', views.submit_code, name='submit_code'),
]
