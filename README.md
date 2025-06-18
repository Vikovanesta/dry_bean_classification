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
├── docker-compose.yml      # Configuration for running the app with Docker Compose
├── requirements.txt        # Python package dependencies
├── app.py                  # The Flask backend application (serves frontend and API)
├── dry_bean_rf.joblib      # The pre-trained machine learning model
├── scaler.joblib           # The pre-fitted scaler for data transformation
└── /templates/
    └── index.html          # The frontend HTML, CSS, and JavaScript
```

## Getting Started

The recommended way to run this application is with Docker Compose, as it handles all setup, dependencies, and provides a live-reloading development server with a single command.

### Method 1: Running with Docker Compose (Recommended)

This method is ideal for both development and production-like environments. It provides a consistent setup and enables live-reloading of the code.

**Prerequisites:**

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed and running on your system.

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd dry_bean_classification
    ```

2.  **Start the application:**
    This single command reads the `docker-compose.yaml` file, builds the Docker image, and starts the container. The `-d` flag runs it in the background (detached mode).

    ```bash
    docker-compose up -d
    ```

    _If you want to see the application logs live in your terminal, run it without the `-d` flag: `docker-compose up`._

3.  **Access the application:**
    Open your web browser and navigate to:
    **[http://localhost:5001](http://localhost:5001)**

    Any changes you make to the Python code (`app.py`) will automatically restart the server inside the container.

4.  **To stop the application:**
    This command will gracefully stop and remove the container and its associated network.
    ```bash
    docker-compose down
    ```

### Method 2: Running with Docker (Without Compose)

Use this method if you don't have Docker Compose or prefer to manage the container manually.

**Prerequisites:**

-   Docker installed and running.

**Steps:**

1.  **Build the Docker image:**

    ```bash
    docker build -t dry-bean-classifier .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -d -p 5001:5000 --name bean-app dry-bean-classifier
    ```

3.  **Access the application** at [http://localhost:5001](http://localhost:5001).

4.  **To stop and remove the container:**
    ```bash
    docker stop bean-app
    docker rm bean-app
    ```

### Method 3: Running Locally (Without Docker)

This method is suitable for quick tests or if you cannot use Docker.

**Prerequisites:**

-   Python 3.8+ and `pip` installed.

**Steps:**

1.  **Set up a virtual environment:**

    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask application:**

    ```bash
    python app.py
    ```

4.  **Access the application** at [http://127.0.0.1:5000](http://127.0.0.1:5000).

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
        "MajorAxisLength": 353. MajorAxisLength,
        "MinorAxisLength": 216. MinorAxisLength,
        "AspectRation": 1.638,
        "Eccentricity": 0.791,
        "ConvexArea": 59560,
        "EquivDiameter": 273.4 EquivDiameter,
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
