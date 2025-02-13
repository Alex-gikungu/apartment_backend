import unittest
import requests

# Base URL of your Flask app
BASE_URL = 'http://127.0.0.1:5000'

class TestFlaskApp(unittest.TestCase):

 def test_register_user(self):
    """Test the /register endpoint."""
    url = f'{BASE_URL}/register'
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "location": "New York",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    self.assertEqual(response.status_code, 201)
    self.assertIn("User registered successfully", response.json()["message"])

    def test_login_user(self):
        """Test the /login endpoint."""
        # Register a user first
        register_url = f'{BASE_URL}/register'
        register_data = {
            "name": "John Doe",
            "email": "johns@example.com",
            "phone": "1234545890",
            "location": "Nairobi",
            "password": "password123"
        }
        requests.post(register_url, json=register_data)

        
        login_url = f'{BASE_URL}/login'
        login_data = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = requests.post(login_url, json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.json()["message"])

    def test_create_apartment(self):
        """Test the /apartments endpoint."""
        url = f'{BASE_URL}/apartments'
        data = {
            "name": "Luxury Apartment",
            "location": "Los Angeles",
            "price": 1500.00,
            "images": ["url1.jpg", "url2.jpg"],
            "description": "A beautiful apartment in the heart of LA."
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Apartment created successfully", response.json()["message"])

 def test_create_booking(self):
    """Test the /bookings endpoint."""
    url = f'{BASE_URL}/bookings'
    data = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "0987654321",
        "house_location": "Los Angeles",
        "visit_date": "2023-12-25",  # Date in YYYY-MM-DD format
        "visit_time": "14:00"         # Time in HH:MM format
    }
    response = requests.post(url, json=data)
    self.assertEqual(response.status_code, 201)
    self.assertIn("Booking created successfully", response.json()["message"])

    def test_create_contact(self):
        """Test the /contacts endpoint."""
        url = f'{BASE_URL}/contacts'
        data = {
            "name": "Alice",
            "email": "alice@example.com",
            "subject": "Inquiry",
            "message": "Hello, I have a question about your apartments."
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Contact message sent successfully", response.json()["message"])

if __name__ == '__main__':
    unittest.main()