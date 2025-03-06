# Project Setup and Execution Guide

This guide provides step-by-step instructions to clone, set up, and run the project on your system.

## Prerequisites

Ensure you have the following installed:

- Git (for cloning the repository)
- Python (latest stable version recommended)
- Pipenv (Python dependency manager)

## Cloning the Repository

To get started, clone the project repository from GitHub:

```sh
git clone https://github.com/SydneyTechnologies/skinnovate.git
```

Then, navigate into the project directory:

```sh
cd skinnovate
```

## Installation

### 1. **Check Python Installation**

Check if you have Python running on your computer with the command below:

```sh
python --version
```

If Python is installed, check if you have Pipenv installed with the following command:

```sh
pipenv --version
```

If Pipenv is not installed, you can install it using the following command:

```sh
pip install --user pipenv
```

For more information on Pipenv installation, reference the [Pipenv documentation](https://pipenv.pypa.io/en/latest/).

### 2. **Set Up a Virtual Environment and Install Dependencies**

Run the following commands to set up the environment and install dependencies:

```sh
pipenv install --dev
```

This will create a virtual environment and install all required dependencies as specified in the `Pipfile`.

### 3. **Environment Variables Setup**

The project requires certain environment variables to be configured. Copy the sample `.env.sample` file and rename it to `.env`:

```sh
cp sample.env .env
```

If the command above doesn't work you can just rename the file manually and continue

Then, open the `.env` file and replace the placeholder values with the appropriate secrets.

### 4. **Tesseract Setup (Windows Users Only)**

If you are running the project on Windows and require Tesseract OCR, follow these steps:

- Download and install Tesseract OCR from the official [Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html).
- Update the `TESSERACT_PATH` variable in `utils.py` with the path to the Tesseract executable.

## Running the Project with Pipenv

Activate the virtual environment and run the project:

```sh
pipenv shell
python app.py
```

## Running the Project Directly

If you prefer to run the project without using Pipenv, ensure dependencies are installed and then execute:

```sh
python app.py
```

The project should now be up and running.
