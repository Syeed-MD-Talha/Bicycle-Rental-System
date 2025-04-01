from abc import ABC, abstractmethod
from django.utils import timezone


# Observer Pattern
class BicycleObserver(ABC):
    @abstractmethod
    def update(self, bicycle):
        pass


class UserObserver(BicycleObserver):
    def __init__(self, user):
        self.user = user

    def update(self, bicycle):
        print(
            f"{self.user.username} notified: Bicycle {bicycle.bicycle_id} is {bicycle.status}"
        )


class AdminObserver(BicycleObserver):
    def update(self, bicycle):
        print(f"Admin notified: Bicycle {bicycle.bicycle_id} is {bicycle.status}")


class BicycleSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, bicycle):
        for observer in self.observers:
            observer.update(bicycle)


# Strategy Pattern (unchanged)
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, duration):
        pass


class HourlyPricing(PricingStrategy):
    def calculate_cost(self, duration):
        return duration * 2  # $2/hour


class FlatPricing(PricingStrategy):
    def calculate_cost(self, duration):
        return 10  # Flat $10


# Singleton Pattern (unchanged)
class AdminManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminManager, cls).__new__(cls)
        return cls._instance

    def approve_rental(self, bicycle):
        print(f"Admin approved rental for {bicycle}")

    def confirm_return(self, bicycle):
        print(f"Admin confirmed return of {bicycle}")

    def manage_bicycle(self, action, bicycle):
        print(f"Admin {action} bicycle {bicycle}")


# class AdminManager:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(AdminManager, cls).__new__(cls)
#         return cls._instance

#     def approve_rental(self, bicycle):
#         print(f"Admin approved rental for {bicycle}")

#     def confirm_return(self, bicycle):
#         print(f"Admin confirmed return of {bicycle}")


# Factory Pattern (unchanged)
class BicycleFactory:
    @staticmethod
    def create_bicycle(bicycle_type, bicycle_id):
        from .models import Bicycle

        return Bicycle.objects.create(bicycle_id=bicycle_id, type=bicycle_type)


# Mock Payment System (unchanged)
class PaymentProcessor:
    @staticmethod
    def process_payment(user, amount):
        print(f"Processing payment of ${amount} for {user.username}")
        return True


# Facade Pattern (updated with return)
class RentalFacade:
    def __init__(self):
        self.pricing = HourlyPricing()
        self.admin = AdminManager()
        self.subject = BicycleSubject()

    def rent_bicycle(self, user, bicycle, duration):
        bicycle.status = "booked"
        bicycle.save()
        self.admin.approve_rental(bicycle)
        cost = self.pricing.calculate_cost(duration)
        from .models import Rental

        rental = Rental.objects.create(
            user=user, bicycle=bicycle, duration=duration, cost=cost
        )
        self.subject.notify(bicycle)
        return rental

    def return_bicycle(self, rental):
        rental.bicycle.status = "available"
        rental.bicycle.save()
        rental.end_time = timezone.now()  # Mark return time
        rental.save()
        self.admin.confirm_return(rental.bicycle)
        self.subject.notify(rental.bicycle)


# Proxy Pattern (unchanged)
class BicycleUnlockProxy:
    def __init__(self, bicycle, user, amount):
        self.bicycle = bicycle
        self.user = user
        self.amount = amount
        self.payment_processor = PaymentProcessor()

    def unlock(self):
        if self.payment_processor.process_payment(self.user, self.amount):
            print(f"Unlocking {self.bicycle}")
            return True
        else:
            print("Payment failed. Cannot unlock bicycle.")
            return False


# # rental/patterns.py
# from abc import ABC, abstractmethod


# # Observer Pattern
# class BicycleObserver(ABC):
#     @abstractmethod
#     def update(self, bicycle):
#         pass


# class UserObserver(BicycleObserver):
#     def __init__(self, user):
#         self.user = user

#     def update(self, bicycle):
#         print(
#             f"{self.user.username} notified: Bicycle {bicycle.bicycle_id} is {bicycle.status}"
#         )


# class BicycleSubject:
#     def __init__(self):
#         self.observers = []

#     def attach(self, observer):
#         self.observers.append(observer)

#     def detach(self, observer):
#         self.observers.remove(observer)

#     def notify(self, bicycle):
#         for observer in self.observers:
#             observer.update(bicycle)


# # Strategy Pattern
# class PricingStrategy(ABC):
#     @abstractmethod
#     def calculate_cost(self, duration):
#         pass


# class HourlyPricing(PricingStrategy):
#     def calculate_cost(self, duration):
#         return duration * 2  # $2/hour


# class FlatPricing(PricingStrategy):
#     def calculate_cost(self, duration):
#         return 10  # Flat $10


# # Singleton Pattern
# class AdminManager:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(AdminManager, cls).__new__(cls)
#         return cls._instance

#     def approve_rental(self, bicycle):
#         print(f"Admin approved rental for {bicycle}")


# # Factory Pattern
# class BicycleFactory:
#     @staticmethod
#     def create_bicycle(bicycle_type, bicycle_id):
#         from .models import Bicycle

#         return Bicycle.objects.create(bicycle_id=bicycle_id, type=bicycle_type)


# # Facade Pattern
# class RentalFacade:
#     def __init__(self):
#         self.pricing = HourlyPricing()
#         self.admin = AdminManager()
#         self.subject = BicycleSubject()

#     def rent_bicycle(self, user, bicycle, duration):
#         bicycle.status = "booked"
#         bicycle.save()
#         self.admin.approve_rental(bicycle)
#         cost = self.pricing.calculate_cost(duration)
#         from .models import Rental

#         rental = Rental.objects.create(
#             user=user, bicycle=bicycle, duration=duration, cost=cost
#         )
#         self.subject.notify(bicycle)
#         return rental


# # Mock Payment System
# class PaymentProcessor:
#     @staticmethod
#     def process_payment(user, amount):
#         # Simulate payment processing (in a real app, this would call an API)
#         print(f"Processing payment of ${amount} for {user.username}")
#         return True  # Simulate successful payment


# # Proxy Pattern (updated)
# class BicycleUnlockProxy:
#     def __init__(self, bicycle, user, amount):
#         self.bicycle = bicycle
#         self.user = user
#         self.amount = amount
#         self.payment_processor = PaymentProcessor()

#     def unlock(self):
#         # Check payment before unlocking
#         if self.payment_processor.process_payment(self.user, self.amount):
#             print(f"Unlocking {self.bicycle}")
#             return True
#         else:
#             print("Payment failed. Cannot unlock bicycle.")
#             return False
