# 🫘 Dry Bean Classification Web App

This project is a web application that classifies seven different types of dry beans based on their morphological features. It uses a pre-trained Random Forest model. The application is built separate frontend (HTML, CSS, JavaScript) and backend (Flask API), and is fully containerized with Docker for easy deployment and portability.

## Features

-   **Bean Classification**: Predicts the bean type from 16 distinct morphological features.
-   **Prediction Probabilities**: Displays the confidence score for each of the seven possible bean types.
-   **Randomize Inputs**: A helper button to populate all feature fields with valid random values for quick testing.

## Tech Stack

-   **Backend**: Python, Flask, Gunicorn, Pandas, Scikit-learn
-   **Frontend**: HTML, CSS, JavaScript (Fetch API)
-   **Containerization**: Docker

## Project Structure

```
/dry-bean-app/
├── Dockerfile              # Instructions to build the Docker image
├── requirements.txt        # Python package dependencies
├── app.py                  # The Flask backend application (serves frontend and API)
├── dry_bean_rf.joblib      # The pre-trained machine learning model
└── /templates/
    └── index.html          # The frontend HTML, CSS, and JavaScript
```

## Getting Started

There are two ways to run this application: using Docker (recommended for consistency) or running it locally in a Python environment.

### Method 1: Running with Docker (Recommended)

This method ensures the application runs in a clean, isolated environment with all dependencies handled automatically.

**Prerequisites:**

-   [Docker](https://www.docker.com/get-started) must be installed and running on your system.

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd dry-bean-app
    ```

2.  **Build the Docker image:**
    This command reads the `Dockerfile` and builds an image named `dry-bean-classifier`. The `.` indicates the build context is the current directory.

    ```bash
    docker build -t dry-bean-classifier .
    ```

3.  **Run the Docker container:**
    This command starts a container from the image you just built.

    -   `-d`: Runs the container in detached mode (in the background).
    -   `-p 5001:5000`: Maps port `5001` on your host machine to port `5000` inside the container (where Gunicorn is running).
    -   `--name my-bean-app`: Assigns a convenient name to the running container.

    ```bash
    docker run -d -p 5001:5000 --name my-bean-app dry-bean-classifier
    ```

4.  **Access the application:**
    Open your web browser and navigate to:
    **[http://localhost:5001](http://localhost:5001)**

### Method 2: Running Locally (Without Docker)

This method is suitable for development or if you prefer not to use Docker.

**Prerequisites:**

-   Python 3.8+ and `pip` installed.

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd dry-bean-app
    ```

2.  **Create and activate a virtual environment:**
    This is a best practice to keep project dependencies isolated.

    -   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**

    ```bash
    python app.py
    ```

5.  **Access the application:**
    The application will be running in debug mode. Open your web browser and navigate to:
    **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## Usage

1.  Navigate to the application URL in your browser.
2.  The form will be pre-filled with default values for each feature.
3.  You can manually change any of the input values.
4.  Alternatively, click the **"🎲 Randomize Inputs"** button to fill the form with random data within valid ranges.
5.  Click the **"Classify Bean"** button to submit the data to the backend.
6.  The prediction result and probability table will appear below the form without the page reloading.

## API Endpoint Documentation

The application exposes a single API endpoint for predictions.

### `POST /predict`

Accepts a JSON object containing the 16 bean features and returns a classification result.

-   **Request Body (JSON):**

    ```json
    {
        "Area": 58778,
        "Perimeter": 978.937,
        "MajorAxisLength": 35,
        "MinorAxisLength": 216,
        "AspectRation": 1.638,
        "Eccentricity": 0.791,
        "ConvexArea": 59560,
        "EquivDiameter": 273.4,
        "Extent": 0.77,
        "Solidity": 0.987,
        "roundness": 0.772,
        "Compactness": 0.776,
        "ShapeFactor1": 0.006,
        "ShapeFactor2": 0.0014,
        "ShapeFactor3": 0.602,
        "ShapeFactor4": 0.992
    }
    ```

-   **Success Response (200 OK):**

    ```json
    {
        "success": true,
        "prediction": "Dermason",
        "probabilities": {
            "Barbunya": 0.01,
            "Bombay": 0.0,
            "Cali": 0.04,
            "Dermason": 0.88,
            "Horoz": 0.03,
            "Seker": 0.02,
            "Sira": 0.02
        }
    }
    ```

-   **Error Response (400 Bad Request or 500 Internal Server Error):**
    ```json
    {
        "success": false,
        "error": "Feature 'Area' is missing from the request."
    }
    ```

## How to Stop the Container

If you started the application using Docker, you can stop and remove the container with these commands:

1.  **Stop the running container:**

    ```bash
    docker stop my-bean-app
    ```

2.  **Remove the stopped container:**
    ```bash
    docker rm my-bean-app
    ```
