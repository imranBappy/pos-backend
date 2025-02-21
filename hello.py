import random
import faker
from apps.accounts.models import User

fake = faker.Faker()  # Use default (English) locale

def generate_customer_data(num_customers=100):
    """Generates customer data with English names, emails, and phone numbers."""

    customer_data = []
    for _ in range(num_customers):
        name = fake.name()
        email = fake.email()
        phone = "01" + "".join(random.choice("3456789") for _ in range(9)) # Bangladeshi phone format
        registration_date = fake.date_between(start_date='-2y', end_date='today')
        customer_data.append({
            'name': name,
            'email': email,
            'phone': phone,
            'registration_date': registration_date.strftime('%Y-%m-%d')
        })
    return customer_data



def users100():
    customer_data = generate_customer_data()
    for customer in customer_data:
        print(type(customer['phone']),customer['phone'])

        User.objects.create(
            name=customer['name'],
            phone=customer['phone'],
            email=customer['email'],
            password=customer['email']
        )
