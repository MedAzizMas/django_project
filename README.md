# Django Conference Management System

This is a web-based application for managing conferences and participants, built with Django. It allows users to create, modify, display, and delete conferences, manage participants, and handle conference reservations. The application demonstrates the use of Django's models, views, templates, and admin features, while incorporating relations between models like Many-to-One and Many-to-Many.

## Features

### Conference Management:
- Create, modify, display, and delete conferences.
- Each conference belongs to a specific category (or type of conference) via a Many-to-One relationship.
- A category can group several conferences, but each conference belongs to only one category.

### Participant Management:
- Create and modify participant accounts.
- Authenticate participants (login functionality).
- A participant can reserve multiple conferences and confirm their participation after reservation.
- The relationship between participants and conferences is Many-to-Many, allowing a participant to attend multiple conferences and a conference to have multiple participants.
- Participants can confirm their attendance after reservation.

## Prerequisites

Before running the project, ensure you have the following installed:
- **Python 3.11.4**
- **Django 4.2**
- **Virtual Environment** (Recommended)

## Setup Instructions

1. **Install Python 3.11.4 **
   Download and install Python from the [official website](https://www.python.org/downloads/).

2. **Create a virtual environment:**
   In your project root, create a virtual environment using the following command:
   ```bash
   python -m venv venv
