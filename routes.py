# routes.py

from flask import Blueprint, request, jsonify
from models import db, User, Apartment, Booking, Contact
from datetime import datetime, date, time

# Create a Blueprint for routes
routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    print("Received data:", data)  # Log the request data

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    location = data.get('location')
    password = data.get('password')

    # Check if all required fields are provided
    if not all([name, email, phone, location, password]):
        print("Missing fields in request data")  # Log missing fields
        return jsonify({"message": "All fields are required"}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        print("Email already registered")  # Log duplicate email
        return jsonify({"message": "Email already registered"}), 400

    # Create a new user
    new_user = User(
        name=name,
        email=email,
        phone=phone,
        location=location
    )
    new_user.set_password(password)  # Hash the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201



@routes_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@routes_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        location=data['location'],
    )
    new_user.set_password(data['password'])  # Hash the password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User  created successfully"}), 201

@routes_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "location": user.location
    })

@routes_blueprint.route('/apartments', methods=['POST'])
def create_apartment():
    data = request.json
    new_apartment = Apartment(
        name=data['name'],
        location=data['location'],
        price=data['price'],
        images=data.get('images', []),
        description=data['description']
    )
    db.session.add(new_apartment)
    db.session.commit()
    return jsonify({"message": "Apartment created successfully"}), 201


@routes_blueprint.route('/apartments', methods=['GET'])
def get_all_apartments():
    try:
        # Query all apartments from the database
        apartments = Apartment.query.all()

        # Prepare the response data
        apartments_data = []
        for apartment in apartments:
            apartments_data.append({
                "id": apartment.id,
                "name": apartment.name,
                "location": apartment.location,
                "price": apartment.price,
                "images": apartment.images,  # List of image URLs
                "description": apartment.description
            })

        return jsonify({"apartments": apartments_data}), 200
    except Exception as e:
        print("Error fetching apartments:", str(e))  # Log the error
        return jsonify({"message": "An error occurred while fetching apartments"}), 500
    
    

@routes_blueprint.route('/apartments/<int:apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    return jsonify({
        "id": apartment.id,
        "name": apartment.name,
        "location": apartment.location,
        "price": apartment.price,
        "images": apartment.images,
        "description": apartment.description
    })


@routes_blueprint.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    print("Received data:", data)  # Log the request data

    full_name = data.get('full_name')
    email = data.get('email')
    phone = data.get('phone')
    house_location = data.get('house_location')
    visit_date_str = data.get('visit_date')  # Get the date as a string
    visit_time_str = data.get('visit_time')  # Get the time as a string

    # Check if all required fields are provided
    if not all([full_name, email, phone, house_location, visit_date_str, visit_time_str]):
        print("Missing fields in request data")  # Log missing fields
        return jsonify({"message": "All fields are required"}), 400

    try:
        # Convert visit_date and visit_time strings to Python objects
        visit_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()
        visit_time = datetime.strptime(visit_time_str, "%H:%M").time()

        # Create a new booking
        new_booking = Booking(
            full_name=full_name,
            email=email,
            phone=phone,
            house_location=house_location,
            visit_date=visit_date,
            visit_time=visit_time
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Booking created successfully"}), 201
    except Exception as e:
        print("Error creating booking:", str(e))  # Log the error
        return jsonify({"message": "An error occurred while creating the booking"}), 500


@routes_blueprint.route('/contacts', methods=['POST'])
def create_contact():
    data = request.json
    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"message": "Contact message sent successfully"}), 201