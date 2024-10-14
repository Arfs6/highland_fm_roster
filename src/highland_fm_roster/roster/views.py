from django.shortcuts import render
from django.views.generic import ListView

from .models import Staff


class StaffListView(ListView):
    model = Staff
    context_object_name = "staffs"
    template_name = "roster/staff_list.html"
