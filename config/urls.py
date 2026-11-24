
from django.contrib import admin
from django.urls import path, include
from EntrepriseApp.health_check import health_check_view
from EntrepriseApp.views import home
from django.contrib.auth.views import LoginView, LogoutView
from EntrepriseApp.views import inscription_view
class TransConnectAdminSite(admin.AdminSite):

    def get_urls(self):
        urls_personnalisees = [
            path(
                'health-check/',
                self.admin_view(health_check_view),
                name='health_check'
            ),
        ]
        return urls_personnalisees + super().get_urls()


admin_site = TransConnectAdminSite(name='admin')
admin_site.site_header = "TransConnect — Administration"
admin_site.site_title = "TransConnect Admin"
admin_site.index_title = "Tableau de bord des opérations"
from django.contrib.auth.views import LoginView
for model, model_admin in admin.site._registry.items():
    admin_site.register(model, type(model_admin))


urlpatterns = [
    path('', home, name='accueil'),
    path('admin/', admin_site.urls),
    path('home/', home, name='home'),
    path('expedition/', include('ExpeditionApp.urls')),
    path('vehicules/', include('VehiculeApp.urls')),
    path('offres/', include('OffreApp.urls')),
    path('entreprises/', include('EntrepriseApp.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('inscription/', inscription_view, name='inscription'),
]
