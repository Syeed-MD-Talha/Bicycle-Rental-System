from abc import ABC, abstractmethod
from django.utils import timezone
import random
import string


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

    def payment_notification(self, rental):
        print(
            f"Payment notification for {self.user.username}: Transaction {rental.transaction_id} for ${rental.cost} confirmed."
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

    def notify_payment(self, rental):
        for observer in self.observers:
            if hasattr(observer, "payment_notification"):
                observer.payment_notification(rental)


# Strategy Pattern (updated)
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, bicycle, duration):
        pass


class HourlyPricing(PricingStrategy):
    def calculate_cost(self, bicycle, duration):
        return bicycle.price_per_hour * duration  # Use bicycle-specific price


class FlatPricing(PricingStrategy):
    def calculate_cost(self, bicycle, duration):
        return 10  # Flat $10 (could also be made configurable)


# Singleton Pattern
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


# Factory Pattern
class BicycleFactory:
    @staticmethod
    def create_bicycle(bicycle_type, bicycle_id):
        from .models import Bicycle

        return Bicycle.objects.create(bicycle_id=bicycle_id, type=bicycle_type)


# Dummy Payment System
class DummyPaymentProcessor:
    @staticmethod
    def generate_transaction_id():
        return "TXN" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=9)
        )

    @staticmethod
    def process_payment(user, amount):
        transaction_id = DummyPaymentProcessor.generate_transaction_id()
        print(
            f"Simulated payment of ${amount} by {user.username} completed. Transaction ID: {transaction_id}"
        )
        return transaction_id


# Facade Pattern (updated)
class RentalFacade:
    def __init__(self):
        self.pricing = HourlyPricing()
        self.admin = AdminManager()
        self.subject = BicycleSubject()
        self.payment_processor = DummyPaymentProcessor()

    def rent_bicycle(self, user, bicycle, duration):
        # Set a reasonable maximum duration of 24 hours
        MAX_DURATION = 24
        if duration > MAX_DURATION:
            raise ValueError(f"Duration exceeds max allowed ({MAX_DURATION} hours)")
        bicycle.status = "booked"
        bicycle.save()
        cost = self.pricing.calculate_cost(bicycle, duration)
        transaction_id = self.payment_processor.process_payment(user, cost)
        self.admin.approve_rental(bicycle)
        from .models import Rental

        rental = Rental.objects.create(
            user=user,
            bicycle=bicycle,
            duration=duration,
            cost=cost,
            transaction_id=transaction_id,
        )
        self.subject.notify(bicycle)
        self.subject.notify_payment(rental)
        return rental

    def return_bicycle(self, rental):
        rental.bicycle.status = "available"
        rental.bicycle.save()
        rental.end_time = timezone.now()
        rental.save()
        self.admin.confirm_return(rental.bicycle)
        self.subject.notify(rental.bicycle)


# Proxy Pattern
class BicycleUnlockProxy:
    def __init__(self, bicycle, user, amount):
        self.bicycle = bicycle
        self.user = user
        self.amount = amount

    def unlock(self):
        print(f"Unlocking {self.bicycle} for {self.user.username}")
        return True
