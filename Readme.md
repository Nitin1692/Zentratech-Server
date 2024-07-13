# Django Interest & Chat Application

Develop a minimal full-stack application that demonstrates your capabilities in both front-end and back-end development, with a focus on Python (Django) and JavaScript frameworks. This project is an opportunity for you to illustrate your technical strengths, decision-making process, and your approach to solving practical problems.

## Project Setup

### Prerequisites

- Python (version 3.8+ recommended)
- Virtualenv
- MySQL server (installed via XAMPP)

### Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd projectfolder
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure MySQL database:**

    Open `settings.py` and set up your MySQL database credentials in the `DATABASES` section:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'zentratech',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'your_database_host',
            'PORT': 'your_database_port',
        }
    }
    ```
5. **Navigate to server folder**

    ```bash
    cd server
    ```

6. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```    