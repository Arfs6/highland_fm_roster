from django.http import HttpRequest as HttpRequestBase
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic import ListView
from django_htmx.middleware import HtmxDetails

from .forms import StaffForm
from .models import Staff


class HttpRequest(HttpRequestBase):
    htmx: HtmxDetails


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
            return redirect(reverse("roster:staffsList"))


class StaffActionsView(View):
    """View for staff actions like editing and deleting."""

    def get(self, request, id):
        """Returns a form for editing a Staff."""
        staff = get_object_or_404(Staff, pk=id)
        form = StaffForm(
            initial=dict(
                firstName=staff.firstName,
                middleName=staff.middleName,
                lastName=staff.lastName,
            )
        )
        return render(
            request, "roster/staff_edit_modal.html", {"form": form, "staff": staff}
        )

    def put(self, request, id):
        """Edits a staff."""
        staff = get_object_or_404(Staff, pk=id)
        form = StaffForm(QueryDict(request.body.decode()), instance=staff)
        if not form.is_valid():
            return render(
                request,
                "roster/staff_edit_modal.html",
                {
                    "form": form,
                    "staff": staff,
                },
            )
        form.save()
        response = render(
            request,
            "roster/staff_list_item.html",
            {
                "staff": staff,
            },
        )
        response['HX-Retarget'] = f"#staff-{staff.id}"
        response['HX-Reswap'] = "outerHTML"
        return response

    def delete(self, request, id):
        """Deletes a staff."""
        staff = get_object_or_404(Staff, id=id)
        staff.delete()
        response = HttpResponse()
        response['hx-retarget'] = f"#staff-{id}"
        response['hx-reswap'] = 'delete'
        return response
