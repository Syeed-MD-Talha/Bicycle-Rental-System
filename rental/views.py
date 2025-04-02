from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Bicycle, Rental
from .patterns import RentalFacade, BicycleUnlockProxy, UserObserver, AdminObserver
from .forms import FeedbackForm


def home(request):
    return render(request, "rental/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("bicycle_list")
    else:
        form = UserCreationForm()
    return render(request, "rental/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("bicycle_list")
    else:
        form = AuthenticationForm()
    return render(request, "rental/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def bicycle_list(request):
    bicycles = Bicycle.objects.all()
    for bicycle in bicycles:
        bicycle.avg_rating = bicycle.average_rating()
        bicycle.feedback_count = bicycle.feedback_count()
    if request.method == "POST":
        bicycle_id = request.POST.get("bicycle_id")
        duration = int(request.POST.get("duration"))
        bicycle = Bicycle.objects.get(id=bicycle_id)
        return redirect("payment_confirm", bicycle_id=bicycle.id, duration=duration)
    return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


@login_required
def payment_confirm(request, bicycle_id, duration):
    bicycle = Bicycle.objects.get(id=bicycle_id)
    cost = duration * bicycle.price_per_hour  # Use bicycle-specific price
    if request.method == "POST":
        return redirect("rent_bicycle", bicycle_id=bicycle.id)
    return render(
        request,
        "rental/payment_confirm.html",
        {
            "bicycle": bicycle,
            "duration": duration,
            "cost": cost,
            "price_per_hour": bicycle.price_per_hour,
        },
    )


@login_required
def rent_bicycle(request, bicycle_id):
    if request.method == "POST":
        bicycle = Bicycle.objects.get(id=bicycle_id)
        duration = int(request.POST.get("duration"))
        user = request.user

        facade = RentalFacade()
        facade.subject.attach(UserObserver(user))
        facade.subject.attach(AdminObserver())
        rental = facade.rent_bicycle(user, bicycle, duration)
        proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
        if proxy.unlock():
            return redirect("bicycle_list")
        else:
            return HttpResponse("Unlock failed", status=400)
    return HttpResponse("Method not allowed", status=405)


@login_required
def dashboard(request):
    user = request.user
    rentals = Rental.objects.filter(user=user).order_by("-start_time")
    return render(request, "rental/dashboard.html", {"rentals": rentals})


@login_required
def return_bicycle(request, rental_id):
    if request.method == "POST":
        rental = Rental.objects.get(id=rental_id, user=request.user)
        if rental.end_time is None:
            facade = RentalFacade()
            facade.subject.attach(UserObserver(request.user))
            facade.subject.attach(AdminObserver())
            facade.return_bicycle(rental)
            return redirect("dashboard")
        else:
            return HttpResponse("Bicycle already returned", status=400)
    return HttpResponse("Method not allowed", status=405)


@login_required
def submit_feedback(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    if rental.end_time is None:
        return HttpResponse(
            "Please return the bicycle before leaving feedback", status=400
        )

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = FeedbackForm(instance=rental)
    return render(request, "rental/feedback.html", {"form": form, "rental": rental})
