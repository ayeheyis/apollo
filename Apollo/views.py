from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,Http404
from Apollo.forms import *
from Apollo.models import *
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from mimetypes import guess_type
from django.db.models import Q

#######################################################################################################################
#####################Actions that do not require authentication########################################################
#######################################################################################################################

#Displays the project info
def index(request):
    context = {}
    return render(request, 'index.html', context)

#Displays the identify page
def identify(request):
    context = {}
    context['patients'] = Patient.objects.all()
    return render(request, 'identify.html', context)

#Displays the statistics page
def statistics(request):
    context = {}
    context['statistic'] = Statistic.objects.all()[0]
    return render(request, 'statistics.html', context)

#Ids a person by assigning them a name
def id_person(request):
    if(request.method == 'GET'):
        return redirect('identify')
    if not ('name' in request.POST and request.POST['name']):
        raise Http404
    if not ('id' in request.POST and request.POST['id']):
        raise Http404
    (name, id) = (request.POST['name'], request.POST['id'])
    patient = get_object_or_404(Patient, pk=id)
    # Invalid attribute ID, raise 404
    if not patient:
        raise Http404
    patient.name = name
    patient.identified = True
    patient.save()
    return redirect('identify')

#Register a user
@transaction.atomic
def register(request):
    context = {}
    #User requested the register page
    if request.method == 'GET':
        context['register_user_form'] = RegisterUserForm()
        return render(request, 'register.html', context)

    #Build form from requests and validate
    form = RegisterUserForm(request.POST)
    if not form.is_valid():
        context['register_user_form'] = form
        return render(request, 'register.html', context)

    #Create new user with the valid inputs and save
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                      password=form.cleaned_data['password'])
    new_user.first_name = form.cleaned_data['first_name']
    new_user.last_name = form.cleaned_data['last_name']
    new_user.save()

    tents = list(Tent.objects.all())
    low = tents[0]
    for tent in tents:
        if(tent.assignedPatients > low.assignedPatients):
            low = tent
    new_doctor = Doctor(user = new_user, tent=low)
    new_doctor.save()

    #Login new user
    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    login(request, new_user)

    return redirect('home')

def patient_media(request, id):
  # Get attribute with this ID
  patient = get_object_or_404(Patient, pk=id)

  # Invalid attribute ID, raise 404
  if not patient:
    raise Http404

  # Guess content type of attribute image
  content_type = guess_type(patient.image.name)
  return HttpResponse(patient.image, content_type)

#######################################################################################################################
#####################Actions that do require authentication############################################################
#######################################################################################################################

#Displays all the tents
@login_required
def tent(request):
    context = {}
    context['tents'] = Tent.objects.all()
    return render(request, 'tent.html', context)

#Displays the home page with the patients that need to be prioritized
@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
def patient(request):
    patients = Patient.objects.all()
    return render(request, 'patient.json', {"patients":patients}, content_type="application/json")

@login_required
def priority(request):
    patients = Patient.objects.filter(priority=-1, alive=True).order_by('-emergency')
    return render(request, 'patient.json', {"patients":patients}, content_type="application/json")

@login_required
def prioritize(request):
    if request.method == 'GET':
        return HttpResponse(0)
    if not ("id" in request.POST and request.POST["id"]):
        return HttpResponse(0)
    if not ("priority" in request.POST and request.POST["priority"]):
        return HttpResponse(0)
    patient = get_object_or_404(Patient, pk=request.POST["id"])
    if not patient or int(request.POST["priority"]) > 10 or int(request.POST["priority"]) < 0:
       return  HttpResponse(0)

    patient.priority = int(request.POST["priority"])
    patient.save()
    return HttpResponse(1)

@login_required
def check(request):
    phase = Patient.objects.filter(treated=False, alive=True).order_by('priority')
    patients = []
    doctor = Doctor.objects.get(user=request.user)
    tent = doctor.tent
    for i in xrange(len(phase)):
        patient = phase[i]
        if patient.priority != -1 and tent == patient.tent:
            patients += [patient]
    return render(request, 'patient.json', {"patients":patients}, content_type="application/json")

@login_required
def checkin(request):
    if request.method == 'GET':
        return HttpResponse(0)
    if not ("id" in request.POST and request.POST["id"]):
        return HttpResponse(0)
    patient = get_object_or_404(Patient, pk=request.POST["id"])
    if not patient:
       return  HttpResponse(0)

    patient.treated = True
    patient.save()
    return HttpResponse(1)

@login_required
def injury_media(request, id):
  # Get attribute with this ID
  injury = get_object_or_404(Injury, pk=id)

  # Invalid attribute ID, raise 404
  if not injury:
    raise Http404

  # Guess content type of attribute image
  content_type = guess_type(injury.image.name)
  return HttpResponse(injury.image, content_type)


#######################################################################################################################
#####################Actions come from the the device##################################################################
#######################################################################################################################

def handle_injury(request, injured, p):
    print request.FILES
    if injured == "Yes":
        category = request.POST["Injury Type"]
        injury = Injury(category=category, patient=p, image=request.FILES["injury"])
        injury.save()
    else:
        injury = Injury(category="None", patient=p)
        injury.save()

def assign_tent(patient, injured):
    if not patient.alive:
        return Tent.objects.get(name="Tent 5")
    if patient.emergency:
        return Tent.objects.get(name="Tent 3")
    if not patient.conscious:
        return Tent.objects.get(name="Tent 2")
    if injured == "Yes":
        return Tent.objects.get(name="Tent 4")
    return Tent.objects.get(name="Tent 1")

def get_tent_id(tent):
    value = tent.name
    value = value.split(" ")
    return value[1] + ","

def dead(request):
    patient = Patient(alive=False, image=request.FILES["face"])
    patient.save()
    tent = assign_tent(patient, "No")
    patient.tent = tent
    patient.save()
    handle_injury(request, "No", patient)
    return HttpResponse(get_tent_id(tent) + str(patient.pk))

def emergency(request, conscious):
    e = 1
    patient = Patient(alive=True, emergency=e, conscious=conscious, image=request.FILES["face"])
    patient.save()
    tent = assign_tent(patient, "No")
    handle_injury(request, "No", patient)
    return HttpResponse(get_tent_id(tent) + str(patient.pk))

@csrf_exempt
def create(request):
    #Check if patient is alive or not
    pulse = request.POST["Pulse"]
    if(pulse == "No"):
        return dead(request)
    #Determine if conscious or not
    conscious = request.POST["Conscious"]
    if conscious == "Yes":
        conscious = 1
    else:
        conscious = 0
    #Determine if patient needs immediate attention
    emergency = request.POST["Emergency"]
    if emergency == "Yes":
        e = 1
        patient = Patient(alive=True, priority=1, emergency=e, conscious=conscious, image=request.FILES["face"])
        patient.save()
        tent = assign_tent(patient, "No")
        handle_injury(request, "No", patient)
        patient.tent = tent
        patient.save()
        return HttpResponse(get_tent_id(tent) + str(patient.pk))
    else:
        emergency = 0
    #Get the rest of information on the patient and save the patient
    age = int(request.POST["Age"])
    sex = request.POST["Gender"]
    patient = Patient(alive=True, age=age, sex=sex, conscious=conscious, emergency=emergency, image=request.FILES["face"])
    #Take care of the injury
    injured = request.POST["Injured"]
    handle_injury(request, injured, patient)
    tent = assign_tent(patient, injured)
    patient.tent = tent
    patient.save()
    return HttpResponse(get_tent_id(tent) + str(patient.pk))