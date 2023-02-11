from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import WitnessForm
from .models import Witness

# Create your views here.


def create_witness(request):
    if(request.method == 'POST'):
        form = WitnessForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = WitnessForm()
        return redirect("/")


def update_witness(request, wk):
    witness = Witness.objects.get(wk=wk)
    if request.method == 'POST':
        form = WitnessForm(request.POST, request.FILES, instance=witness)
        if form.is_valid():
            form.save()
            return "OK"
    else:
        form = WitnessForm(instance=witness)
    return "Try_Again"


def delete_witness(request, full_name):
    Witness.objects.get(full_name=full_name).delete()
    return "deleted"

def download_picture(request, name):
    picture = get_object_or_404(Witness, full_name=name)
    with open(picture.profile_picture.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment; filename=' + picture.profile_picture.name
    return response


def get_profile_picture_by_full_name(full_name):
    witness = get_object_or_404(witness, full_name)
    return witness.profile_picture
