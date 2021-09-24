from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from licence.forms import ClientForm,CodeLicenceForm
from .models import Client, CodeLicence
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import requests


url_api = 'http://127.0.0.1:8000/'

#solo los uatentificado
@login_required
#rutas y vistas solo para licencia
def index(request):
    #capturar el filtro
    filtro = request.GET.get('filtro')
    all_Clients = Client.objects.all()
    all_Licences = CodeLicence.objects.order_by('type_licence') #obje de add
    
    if filtro:
        all_Clients = Client.objects.filter(
            Q(nci__icontains = filtro)|
            Q(name__icontains = filtro)|
            Q(last_name__icontains = filtro)|
            Q(url_client__icontains = filtro)
        ).distinct
    else:
        filtro = ''
    return render(request,'licence/home.html',{'all_Clients':all_Clients,'all_Licences':all_Licences,'filtro':filtro})


@login_required
def dashboard (request):
    return render(request,'licence/dashboard.html')

@login_required
def createCliente(request):
    #name = request.POST['name'];
    #last_name = request.POST['last_name'];
    #number_phone = request.POST['number_phone'];
    #nci = request.POST['nci'];
    #email = request.POST['email'];
    #url_client = request.POST['url_client'];
    if request.method == 'POST':
        form = ClientForm(request.POST)        
        if form.is_valid():
            try:
                form.save()
                return redirect('/licence/')
            except:
                pass
    else:
        form = ClientForm()
    return render(request,'licence/dashboard.html',{'form':form})    
    
@login_required
def createCodeLicence (request):
    #Los que se guardan, para hacer licences, hash_licence,type_licence,create_at,date_rem
    if request.method == 'POST':
        #buscar al cliente para hacer la relacion many to many
        client_id = request.POST['client_id']        
        client = Client.objects.get(pk=client_id)#es el obj de cliente o sea con este trabajomos para realizwr la relacion
        
        #creacion de code licence
        nci = client.nci
        url_client = client.url_client

        codelicence = 'ABB-155ASDA-66515ASD-ASD'
        #fin
        type_licence = request.POST['type_licence']
        create_at = request.POST['create_at']
        date_rem = request.POST['date_rem']

        form = CodeLicenceForm({'hash_licence':codelicence,'type_licence':type_licence,'create_at':create_at,'date_rem':date_rem})        
        if form.is_valid():            
            try:
                licencia = form.save()
                client.licences.add(licencia)
                actualizarLicenceAPI(client, licencia,2)
            except:
                pass

    else:
        form = ClientForm()
    
    return redirect('/licence/')

@login_required
def addLicence (request):
    client_id = request.POST['client_id']
    code_licence_id=request.POST['codelicence_id']
    client = Client.objects.get(pk=client_id)
    codelicence = CodeLicence.objects.get(pk=code_licence_id)
    client.licences.add(codelicence)
    #si deseio add... tengo que hacer un requets, post para ello....
    #requests.post(url=client.url_client,data={'request':True});
    actualizarLicenceAPI(client, codelicence,1)

    return redirect('/licence/')
    
@login_required
def eliminarLicence (request):
    #a4.publications.remove(p2)
    #>>> p2.article_set.all()
    #<QuerySet [<Article: Oxygen-free diet works wonders>]>
    #>>> a4.publications.all()
    #<QuerySet []>
    client_id = request.POST['client_id']
    code_licence_id=request.POST['codelicence_id']
    client = Client.objects.get(pk=client_id)

    if code_licence_id == '0':
        for licence in client.licences.all(): 
            actualizarLicenceAPI(client, licence,0)
        
        client.licences.clear() #limpiamos todo

    else: 
        codelicence = CodeLicence.objects.get(pk=code_licence_id)
        client.licences.remove(codelicence) #removemos especificamente
        actualizarLicenceAPI(client, codelicence,0)
    #si deseio eliminar... tengo que hacer un requets, post para ello....
    return redirect('/licence/')

def actualizarLicenceAPI (client, codelicence,action):
    form =  {'licence': codelicence.hash_licence, 'nci': client.nci,'url_api':url_api,'url_client':client.url_client,'action':action}    
    res = requests.post(client.url_client+'api/licence', json=form)
    print(res.text)
    print(res.status_code)
    print(res)




#SOLO LOS QUE NO NEVESITE  CSRF

class ClientView(View):

    @method_decorator(csrf_exempt)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #confirmar si el POST que nos envia LARAVEL ESTA OK...
    def post(self,request):
        response = False
        if request.method == 'POST':
            #print(request.body)
            jd = json.loads(request.body)
            #print(jd)
            nci = jd['nci']
            url = jd['url']
            licence = jd['code_licence']
            client = Client.objects.get(nci = nci)
            if client.url_client == url:        
                if client.licences:
                    for licences in client.licences.all():
                        if licences.hash_licence == licence:
                            response = True
        
        return HttpResponse(response)



