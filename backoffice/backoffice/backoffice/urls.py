"""
Definition of urls for backoffice.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [ 
    url(r'^$', app.views.home, name='home'),
    url(r'^manage_key$', app.views.manage_key, name='manage_key'),
    url(r'^manage_key/delete/$', app.views.delete_key, name='delete_key'),
    url(r'^manage_gym$', app.views.manage_gym, name='manage_gym'),
    url(r'^manage_gym/edit_field/$', app.views.edit_field, name='edit_field'),
    url(r'^manage_gym/update_field/$', app.views.update_field, name='update_field'),

    url(r'^support$', app.views.support, name="support"),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Connexion',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
