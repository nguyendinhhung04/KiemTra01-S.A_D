from django.core.management.base import BaseCommand
from staffs.models import Staff

class Command(BaseCommand):
    help = 'Seeds the database with initial staff data'

    def handle(self, *args, **kwargs):
        staff_data = [
            {
                'staff_id': 'ADM001',
                'name': 'System Administrator',
                'phone': '0000000000',
                'email': 'admin@example.com',
                'username': 'admin',
                'password': 'admin',
                'role': 'Admin'
            },
            {
                'staff_id': 'ST001',
                'name': 'John Doe',
                'phone': '1234567890',
                'email': 'john@example.com',
                'username': 'john_doe',
                'password': 'password123',
                'role': 'Admin'
            },
            {
                'staff_id': 'ST002',
                'name': 'Jane Smith',
                'phone': '0987654321',
                'email': 'jane@example.com',
                'username': 'jane_smith',
                'password': 'password456',
                'role': 'Manager'
            },
            {
                'staff_id': 'ST003',
                'name': 'Bob Wilson',
                'phone': '5551234567',
                'email': 'bob@example.com',
                'username': 'bob_wilson',
                'password': 'password789',
                'role': 'Staff'
            }
        ]

        for data in staff_data:
            staff, created = Staff.objects.update_or_create(
                username=data['username'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created staff: {staff.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated staff: {staff.username}'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
