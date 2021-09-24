#urls de esta aplicacion
from django.urls import path
from . import views
from .views import ClientView
#solo licencia
urlpatterns = [
    path('confirm/',ClientView.as_view(),name='confirmClient'),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-cliente', views.createCliente, name='nuevocliente'),
    path('add-licence', views.createCodeLicence, name='generarLicence'),
    path('add-licence-exits', views.addLicence, name='addLicence'),
    path('rem-licence', views.eliminarLicence, name='removeLicence'),

]