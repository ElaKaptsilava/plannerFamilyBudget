# Family Budget Manager
[![codecov](https://codecov.io/github/ElaKaptsilava/plannerFamilyBudget/graph/badge.svg?token=NI0789I2JM)](https://codecov.io/github/ElaKaptsilava/plannerFamilyBudget)

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Installation](#installation)

## Project Overview
The **Family Budget Manager** is a web application designed to help families manage their finances effectively. The application allows users to create multiple budgets, track expenses and income, set financial targets, and invite family members to collaborate on budgeting. Leveraging OpenAI for message generation, the app offers insightful recommendations and automated responses, enhancing the user experience.

## Features
- **Budget Management**: Create and manage multiple family budgets.
- **Expense Tracking**: Monitor running costs and expenses in real-time.
- **Income Monitoring**: Keep track of all sources of income.
- **Target Setting**: Set financial targets to achieve specific goals.
- **Family Collaboration**: Invite family members to contribute to budgeting.
- **OpenAI Integration**: Send messages and receive insights using OpenAI technology.
- **Translation**: Multi-language support to translate web pages with Django.
- **CI/CD Implementation**: Continuous integration and deployment for streamlined updates.

## Technologies Used
- **Python**: Backend development with Django.
- **Django**: Web framework for building the application.
- **OpenAI**: For generating messages and insights.
- **Redis**: Caching and session management.
- **Celery**: For background task processing.
- **Sentry**: Monitoring and error tracking.
- **HTML/CSS/JavaScript**: Frontend development.
- **Docker & Docker Compose**: Containerization for development and deployment.
- **CI/CD**: Implementation for automated testing and deployment.

## Getting Started
To get a copy of this project up and running on your local machine for development and testing purposes, follow these instructions.

### Installation
1. **Clone the repository**
    ```bash
    git clone https://github.com/ElaKaptsilava/plannerFamilyBudget
    ```
2. **Create a .env file**
   - On Unix-based systems (Linux/macOS)
       ```bash
       cp .env.dist .env
       ```
   - On Windows:
    ```bash
    copy .env.dist .env
    ```
3. **Build and up Docker containers**
    ```bash
    docker-compose build
    docker-compose up
    ```
4. **Run migrations**
    ```bash
    docker-compose exec web python manage.py migrate
    ```
5. **Create superuser (optional)**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```