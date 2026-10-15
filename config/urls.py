
from django.contrib import admin
from django.urls import path

from EntrepriseApp.health_check import health_check_view


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

for model, model_admin in admin.site._registry.items():
    admin_site.register(model, type(model_admin))

urlpatterns = [
    path('admin/', admin_site.urls),
]
