from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Bicycle, Rental
from .patterns import RentalFacade, BicycleUnlockProxy, UserObserver, AdminObserver
from .forms import FeedbackForm


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
    return redirect("bicycle_list")


@login_required
def bicycle_list(request):
    bicycles = Bicycle.objects.all()
    for bicycle in bicycles:
        bicycle.temp_cost = 3 * 2  # Hardcoded for display
        bicycle.avg_rating = bicycle.average_rating()  # Add average rating
        bicycle.feedback_count = bicycle.feedback_count()  # Add feedback count
    if request.method == "POST":
        bicycle_id = request.POST.get("bicycle_id")
        duration = int(request.POST.get("duration", 3))
        bicycle = Bicycle.objects.get(id=bicycle_id)
        user = request.user

        facade = RentalFacade()
        facade.subject.attach(UserObserver(user))
        facade.subject.attach(AdminObserver())
        rental = facade.rent_bicycle(user, bicycle, duration)
        proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
        if proxy.unlock():
            return redirect("bicycle_list")
        else:
            return HttpResponse("Payment failed", status=400)

    return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


# @login_required
# def bicycle_list(request):
#     bicycles = Bicycle.objects.all()
#     for bicycle in bicycles:
#         bicycle.temp_cost = 3 * 2
#     if request.method == "POST":
#         bicycle_id = request.POST.get("bicycle_id")
#         duration = int(request.POST.get("duration", 3))
#         bicycle = Bicycle.objects.get(id=bicycle_id)
#         user = request.user

#         facade = RentalFacade()
#         facade.subject.attach(UserObserver(user))
#         facade.subject.attach(AdminObserver())
#         rental = facade.rent_bicycle(user, bicycle, duration)
#         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
#         if proxy.unlock():
#             return redirect("bicycle_list")
#         else:
#             return HttpResponse("Payment failed", status=400)

#     return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


@login_required
def rent_bicycle(request, bicycle_id):
    if request.method == "POST":
        bicycle = Bicycle.objects.get(id=bicycle_id)
        duration = int(request.POST.get("duration", 3))
        user = request.user

        facade = RentalFacade()
        facade.subject.attach(UserObserver(user))
        facade.subject.attach(AdminObserver())
        rental = facade.rent_bicycle(user, bicycle, duration)
        proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
        if proxy.unlock():
            return redirect("bicycle_list")
        else:
            return HttpResponse("Payment failed", status=400)
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
    rental = Rental.objects.get(id=rental_id, user=request.user)
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


# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from .models import Bicycle, Rental
# from .patterns import RentalFacade, BicycleUnlockProxy, UserObserver, AdminObserver


# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("bicycle_list")
#     else:
#         form = UserCreationForm()
#     return render(request, "rental/register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("bicycle_list")
#     else:
#         form = AuthenticationForm()
#     return render(request, "rental/login.html", {"form": form})


# def logout_view(request):
#     logout(request)
#     return redirect("bicycle_list")


# @login_required
# def bicycle_list(request):
#     bicycles = Bicycle.objects.all()
#     for bicycle in bicycles:
#         bicycle.temp_cost = 3 * 2
#     if request.method == "POST":
#         bicycle_id = request.POST.get("bicycle_id")
#         duration = int(request.POST.get("duration", 3))
#         bicycle = Bicycle.objects.get(id=bicycle_id)
#         user = request.user

#         facade = RentalFacade()
#         facade.subject.attach(UserObserver(user))
#         facade.subject.attach(AdminObserver())  # Notify admin too
#         rental = facade.rent_bicycle(user, bicycle, duration)
#         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
#         if proxy.unlock():
#             return redirect("bicycle_list")
#         else:
#             return HttpResponse("Payment failed", status=400)

#     return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


# @login_required
# def rent_bicycle(request, bicycle_id):
#     if request.method == "POST":
#         bicycle = Bicycle.objects.get(id=bicycle_id)
#         duration = int(request.POST.get("duration", 3))
#         user = request.user

#         facade = RentalFacade()
#         facade.subject.attach(UserObserver(user))
#         facade.subject.attach(AdminObserver())
#         rental = facade.rent_bicycle(user, bicycle, duration)
#         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
#         if proxy.unlock():
#             return redirect("bicycle_list")
#         else:
#             return HttpResponse("Payment failed", status=400)
#     return HttpResponse("Method not allowed", status=405)


# @login_required
# def dashboard(request):
#     user = request.user
#     rentals = Rental.objects.filter(user=user).order_by("-start_time")
#     return render(request, "rental/dashboard.html", {"rentals": rentals})


# @login_required
# def return_bicycle(request, rental_id):
#     if request.method == "POST":
#         rental = Rental.objects.get(id=rental_id, user=request.user)
#         if rental.end_time is None:  # Only allow return if not already returned
#             facade = RentalFacade()
#             facade.subject.attach(UserObserver(request.user))
#             facade.subject.attach(AdminObserver())
#             facade.return_bicycle(rental)
#             return redirect("dashboard")
#         else:
#             return HttpResponse("Bicycle already returned", status=400)
#     return HttpResponse("Method not allowed", status=405)


# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from .models import Bicycle, Rental
# from .patterns import RentalFacade, BicycleUnlockProxy, UserObserver


# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("bicycle_list")
#     else:
#         form = UserCreationForm()
#     return render(request, "rental/register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("bicycle_list")
#     else:
#         form = AuthenticationForm()
#     return render(request, "rental/login.html", {"form": form})


# def logout_view(request):
#     logout(request)
#     return redirect("bicycle_list")


# @login_required
# def bicycle_list(request):
#     bicycles = Bicycle.objects.all()
#     for bicycle in bicycles:
#         bicycle.temp_cost = 3 * 2  # Hardcoded 3 hours at $2/hour for display
#     if request.method == "POST":
#         bicycle_id = request.POST.get("bicycle_id")
#         duration = int(request.POST.get("duration", 3))
#         bicycle = Bicycle.objects.get(id=bicycle_id)
#         user = request.user

#         facade = RentalFacade()
#         facade.subject.attach(UserObserver(user))
#         rental = facade.rent_bicycle(user, bicycle, duration)
#         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
#         if proxy.unlock():
#             return redirect("bicycle_list")
#         else:
#             return HttpResponse("Payment failed", status=400)

#     return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


# @login_required
# def rent_bicycle(request, bicycle_id):
#     if request.method == "POST":
#         bicycle = Bicycle.objects.get(id=bicycle_id)
#         duration = int(request.POST.get("duration", 3))
#         user = request.user

#         facade = RentalFacade()
#         facade.subject.attach(UserObserver(user))
#         rental = facade.rent_bicycle(user, bicycle, duration)
#         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
#         if proxy.unlock():
#             return redirect("bicycle_list")
#         else:
#             return HttpResponse("Payment failed", status=400)
#     return HttpResponse("Method not allowed", status=405)


# @login_required
# def dashboard(request):
#     user = request.user
#     rentals = Rental.objects.filter(user=user).order_by("-start_time")
#     return render(request, "rental/dashboard.html", {"rentals": rentals})


# # from django.shortcuts import render, redirect
# # from django.contrib.auth import login, logout, authenticate
# # from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# # from django.contrib.auth.decorators import login_required
# # from django.http import HttpResponse
# # from .models import Bicycle, Rental
# # from .patterns import RentalFacade, BicycleUnlockProxy, UserObserver


# # def register(request):
# #     if request.method == "POST":
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect("bicycle_list")
# #     else:
# #         form = UserCreationForm()
# #     return render(request, "rental/register.html", {"form": form})


# # def login_view(request):
# #     if request.method == "POST":
# #         form = AuthenticationForm(request, data=request.POST)
# #         if form.is_valid():
# #             user = form.get_user()
# #             login(request, user)
# #             return redirect("bicycle_list")
# #     else:
# #         form = AuthenticationForm()
# #     return render(request, "rental/login.html", {"form": form})


# # def logout_view(request):
# #     logout(request)
# #     return redirect("bicycle_list")


# # # @login_required
# # # def bicycle_list(request):
# # #     bicycles = Bicycle.objects.all()
# # #     if request.method == "POST":
# # #         bicycle_id = request.POST.get("bicycle_id")
# # #         duration = int(request.POST.get("duration", 3))
# # #         bicycle = Bicycle.objects.get(id=bicycle_id)
# # #         user = request.user

# # #         facade = RentalFacade()
# # #         facade.subject.attach(UserObserver(user))
# # #         rental = facade.rent_bicycle(user, bicycle, duration)
# # #         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)  # Pass cost to proxy
# # #         if proxy.unlock():
# # #             return redirect("bicycle_list")
# # #         else:
# # #             return HttpResponse("Payment failed", status=400)

# # #     return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


# # @login_required
# # def bicycle_list(request):
# #     bicycles = Bicycle.objects.all()
# #     for bicycle in bicycles:
# #         bicycle.temp_cost = 3 * 2  # Hardcoded 3 hours at $2/hour for display
# #     if request.method == "POST":
# #         bicycle_id = request.POST.get("bicycle_id")
# #         duration = int(request.POST.get("duration", 3))
# #         bicycle = Bicycle.objects.get(id=bicycle_id)
# #         user = request.user

# #         facade = RentalFacade()
# #         facade.subject.attach(UserObserver(user))
# #         rental = facade.rent_bicycle(user, bicycle, duration)
# #         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)
# #         if proxy.unlock():
# #             return redirect("bicycle_list")
# #         else:
# #             return HttpResponse("Payment failed", status=400)

# #     return render(request, "rental/bicycle_list.html", {"bicycles": bicycles})


# # @login_required
# # def rent_bicycle(request, bicycle_id):
# #     if request.method == "POST":
# #         bicycle = Bicycle.objects.get(id=bicycle_id)
# #         duration = int(request.POST.get("duration", 3))
# #         user = request.user

# #         facade = RentalFacade()
# #         facade.subject.attach(UserObserver(user))
# #         rental = facade.rent_bicycle(user, bicycle, duration)
# #         proxy = BicycleUnlockProxy(bicycle, user, rental.cost)  # Pass cost to proxy
# #         if proxy.unlock():
# #             return redirect("bicycle_list")
# #         else:
# #             return HttpResponse("Payment failed", status=400)
# #     return HttpResponse("Method not allowed", status=405)
