from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView
from django.views import View

from .models import Staff
from .forms import StaffForm


class StaffListView(ListView):
    model = Staff
    context_object_name = "staffs"
    template_name = "roster/staff_list.html"


class CreateStaffView(View):
    """A view for creating staffs."""

    def get(self, request):
        """Get method for newStaff page."""
        form = StaffForm()
        return render(request, "roster/new_staff.html", {"form": form})

    def post(self, request):
        """Post method for new staff page."""
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('roster:staffsList'))
