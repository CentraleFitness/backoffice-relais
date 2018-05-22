"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.utils import timezone
from datetime import timedelta, date
from django.shortcuts import redirect
from datetime import datetime
from .models import apiKey
from .forms import apiKeyForm, GymForm
from django.contrib.auth.decorators import login_required

from app.models import MongoCollection

import bson
import logging

logger = logging.getLogger(__name__)



@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    logger.debug('home')
    return render(
        request,
        'app/index.html',
        {
            'title':'Accueil',
            'year':datetime.now().year
        }
    )

@login_required
def add_gym(request, methods=["POST"]):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)

    return redirect('manage_gym')

@login_required
def update_field(request, methods=["POST"]):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    ret = db.collection.update_one(
        {
            "_id": bson.ObjectId(request.POST['id'])
        },
        {
            "$set": {
                request.POST['field']: request.POST['new_value']
            }
        })
    return redirect('manage_gym')

@login_required
def edit_field(request, methods=["POST"]):
    object_id = request.POST['id']
    field_name = request.POST['field']
    value = request.POST['value']
    return render(
        request, 
        'app/edit_field.html',
        {
            'id': object_id,
            'field': field_name,
            'value': value
        })

@login_required
def manage_gym(request):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    items = db.collection.find()
    gyms = list()
    for gym in items:
        gym['id'] = gym.pop('_id')
        gyms.append(gym)
    gym_form = GymForm()
    return render(
        request,
        'app/manage_gym.html',
        {
            'gyms': gyms,
            'year': datetime.now().year,
            'form': gym_form
        })

@login_required
def manage_key(request):
    if request.method == "POST":
        form = apiKeyForm(request.POST)
        if form.is_valid():
            apiKey.objects.all().delete()
            key = form.save(commit=False)
            key.date_creation = datetime.now()
            current_year = datetime.now().year
            now = datetime.now()
            key.date_expiration = datetime(current_year + 1, now.month, now.day, now.hour, now.minute, now.second)
            key.save()
            return redirect('manage_key')
    else:
        form = apiKeyForm()
    keys = apiKey.objects.all()
    return render(
        request,
        'app/manage_key.html',
        {
            'keys': keys,
            'form': form,
            'year':datetime.now().year,
        }
    )

def delete_key(request):
    if request.method == "POST":
        key_value = request.POST.get('api_key')
        nb_del, _ = apiKey.objects.get(api_key=key_value).delete()
    return redirect('manage_key')

@login_required
def support(request):
    """Render the Support page."""
    assert isinstance(request, HttpRequest)
    logger.debug('support')
    return render(
        request,
        'app/support.html',
        {
            'title': 'Support',
            'message': '',
        }
    )
