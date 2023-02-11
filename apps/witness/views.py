from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import WitnessForm
from .models import Witness
import csv
import os

# Create your views here.
def get_filenames_without_extension(folder):
    filenames = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            filenames.append(os.path.splitext(file)[0])
    return filenames

def get_images(request):
   with open("apps/witness/images.csv", 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)
        image_list = get_filenames_without_extension("apps/static/assets/testimony_photos")
        print(list_of_csv)
        return JsonResponse({"status":"success", "data":image_list})



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
    data_list = get_data_from_file("apps/witness/images.csv")
    print(data_list)
    #Witness.objects.get(full_name=full_name).delete()
    return JsonResponse({"status":"success", "keyword":data_list})

def download_picture(request, name):
    picture = get_object_or_404(Witness, full_name=name)
    with open(picture.profile_picture.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment; filename=' + picture.profile_picture.name
    return response


def get_profile_picture_by_full_name(full_name):
    witness = get_object_or_404(witness, full_name)
    return witness.profile_picture
