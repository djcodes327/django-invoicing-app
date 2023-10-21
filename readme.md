# Django Invoice Management System

## Overview

Django Invoice Management System is a web application designed to allow users to manage their company profiles,
including user information, contact details, and financial information. It is built using Django, a Python web
framework, and provides a user-friendly interface for creating, updating, and viewing company profiles.

## Features

- User registration and authentication.
- Ability to create, update, and view company profiles.
- User profile information, including personal details and profile pictures.
- Company details, including client name, logo, address, and financial information.
- Customized forms for easy data entry and management.
- UserSettings model to store user-specific company profiles.
- Profile pictures and logos are uploaded and stored securely.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/company-profile-management.git
   ```

2. Create a virtual environment and activate it:

   ``` python
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the project dependencies:

   ``` python
   pip install -r requirements.txt
   ```
   
4. Apply migrations to set up the database:

   ``` python
   python manage.py migrate
   ```

5. Run the development server:

   ``` python
   python manage.py runserver
   ```

6. Access the application at http://localhost:8000 in your web browser.

## Usage

* Create a new account or log in to the system.
* Access your profile page to view and update your user information.
* Click on "Company Profile" to create or update your company's profile.
* Upload profile pictures and logos to personalize your profile.
* Fill in the required company details and financial information.
* Save changes to update your company profile.

## Contributing

We welcome contributions from the community. If you'd like to contribute to the project, please follow our contribution
guidelines.