from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect


from baham.enum_types import VehicleType
from baham.models import VehicleModel
from .models import Vehicle


# Create your views here.
def view_home(request):
    template = loader.get_template('home.html')
    context = {
        'navbar': 'home',
    }
    return HttpResponse(template.render(context, request))


def view_aboutus(request):
    template = loader.get_template('aboutus.html')
    context = {
        'navbar': 'aboutus',
    }
    return HttpResponse(template.render(context, request))


def view_vehicles(request):
    template = loader.get_template('vehicles.html')
    vehicles = VehicleModel.objects.all().order_by('vendor')
    context = {
        'navbar': 'vehicles',
        'vehicles': vehicles
    }
    return HttpResponse(template.render(context, request))


def create_vehicle(request):
    template = loader.get_template('createvehicle.html')
    context = {
        'navbar': 'vehicles',
        'vehicle_types': [(t.name, t.value) for t in VehicleType]
    }
    return HttpResponse(template.render(context, request))


def save_vehicle(request):
    _vendor = request.POST.get('vendor')
    _model = request.POST.get('model')
    _type = request.POST.get('type')
    _capacity = int(request.POST.get('capacity'))
    if not _vendor or not _model:
        return HttpResponseBadRequest('Manufacturer and Model name fields are mandatory!')
    if not _capacity or _capacity < 2:
        _capacity = 2 if _type == VehicleType.MOTORCYCLE else 4
    vehicleModel = VehicleModel(vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    vehicleModel.save()
    return HttpResponseRedirect(reverse('vehicles'))

def vehicle_void(request, vehicle_id):
    vehicle = get_object_or_404(VehicleModel, pk=vehicle_id)
    print("inside")
    if request.method == 'POST':
        void_reason = request.POST.get('void_reason')
        vehicle.voided = True
        vehicle.date_voided = timezone.now()
        vehicle.void_reason = void_reason
        vehicle.save()
    return redirect('vehicles')


def vehicle_unvoid(request, vehicle_id):
    vehicle = get_object_or_404(VehicleModel, pk=vehicle_id)
    vehicle.voided = False
    vehicle.date_voided = None
    vehicle.void_reason = None
    vehicle.save()
    return redirect('vehicles')
