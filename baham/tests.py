from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from baham.models import Vehicle, VehicleModel, Contract, UserProfile
from django.core.exceptions import ValidationError

class TestCases_of_Baham_Constraints(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='newuser', password='newpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, birthdate='1995-05-15', gender='F', type='Driver',
                                                       primary_contact='9876543210', landmark='gilgit baltistan',
                                                       town='SAWAt')
        self.vehicle_model = VehicleModel.objects.create(
            vendor='Honda', model='Civic')
        self.vehicle = Vehicle.objects.create(registration_number='BAH987', model=self.vehicle_model,
                                              colour='red', owner=self.user, status='Active')

    # Test 1: One vehicle per owner
    def test_one_vehicle_per_owner(self):
        with self.assertRaises(IntegrityError):
            Vehicle.objects.create(registration_number='XYZ987', model=self.vehicle_model,
                                   colour='blue', owner=self.user, status='Active')

    # Test 2: No more companions than the vehicle’s seating capacity
    def test_no_more_companions_than_seating_capacity(self):
        contract = Contract.objects.create(vehicle=self.vehicle, companion=self.user_profile,
                                           effective_start_date='2023-05-03', expiry_date='2023-12-24',
                                           is_active=True, fuel_share=50, maintenance_share=50,
                                           schedule='Daily', created_by=self.user)
        vehicle_capacity = self.vehicle.model.capacity
        for i in range(vehicle_capacity):
           
            Contract.objects.create(vehicle=self.vehicle, companion=self.user_profile,
                                    effective_start_date='2023-05-03', expiry_date='2023-12-24',
                                    is_active=True, fuel_share=50, maintenance_share=50,
                                    schedule='Daily', created_by=self.user)
        num_companions = Contract.objects.filter(vehicle=self.vehicle).count()
        print("no of companions: ",num_companions)
        try:
            print("new companion add")
            Contract.objects.create(vehicle=self.vehicle, companion=self.user_profile,
                                    effective_start_date='2023-05-03', expiry_date='2023-12-24'
                                    is_active=True, fuel_share=50, maintenance_share=50,
                                    schedule='Daily', created_by=self.user)
        except ValueError as e:
            print("Exception value error",e)
            raise
        num_companions_after = Contract.objects.filter(
            vehicle=self.vehicle).count()
        print("no. of companions after this attempt", num_companions_after)

   
    #Test 3: Total share cannot exceed 100.

    def test_total_share_cannot_exceed_100(self):
        try:
            Contract.objects.create(
                vehicle=self.vehicle,
                companion=self.user_profile,
                effective_start_date='2023-05-05',
                expiry_date='2023-12-20',
                is_active=True,
                fuel_share=0,
                maintenance_share=40,
                schedule='Daily',
                created_by=self.user
            )
        except ValidationError as e:
            print(f"Caught ValidationError: {e}")
        else:
            print("No ValidationError raised.")

        try:
            Contract.objects.create(
                vehicle=self.vehicle,
                companion=self.user_profile,
                effective_start_date='2023-05-05',
                expiry_date='2023-12-20',
                is_active=True,
                fuel_share=50,
                maintenance_share=60,
                schedule='Daily',
                created_by=self.user
            )
        except ValidationError as e:
            print(f"Caught ValidationError: {e}")
        else:
            print("No ValidationError raised.")

        contract = Contract.objects.create(
            vehicle=self.vehicle,
            companion=self.user_profile,
            effective_start_date='2023-05-05',
            expiry_date='2023-12-20',
            is_active=True,
            fuel_share=50,
            maintenance_share=50,
            schedule='Daily',
            created_by=self.user
        )
        print("Contract created.")
        self.assertIsNotNone(contract)


    # Test 4: Companions cannot have multiple active contracts simultaneously.
    def test_companion_cannot_have_multiple_active_contracts(self):
        Contract.objects.create(vehicle=self.vehicle, companion=self.user_profile,
                                   effective_start_date='2023-05-05',
                expiry_date='2023-12-20',
                                is_active=True, fuel_share=50, maintenance_share=50,
                                schedule='Daily', created_by=self.user)
        print("First contract created.")
        try:
            Contract.objects.create(vehicle=self.vehicle, companion=self.user_profile,
                                        effective_start_date='2023-05-05',
                expiry_date='2023-12-20',
                                    is_active=True, fuel_share=50, maintenance_share=50,
                                    schedule='Daily', created_by=self.user)
        except ValidationError as e:
            print(f"Caught ValidationError: {e}")
        else:
            print("No ValidationError raised.")

