# Resolute-ML-APP

## Overview

Resolute-ML-APP is a web application built using Flask for clustering and classification tasks. It provides functionalities to predict clusters and classifications based on user input features, visualize the clustering results, and analyze activity durations and numbers from a dataset.

## Features

- **Clustering**: Predicts the cluster of a given input feature set and visualizes the result.
- **Classification**: Predicts the class of a given input feature set.
- **Data Analysis**: Calculates and displays the duration of activities and the number of activities on a given date.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/Resolute-ML-APP.git
    cd Resolute-ML-APP
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare your data**:
    - Place your clustering and classification models in the `models` directory.
    - Place your datasets in the `data` directory.

## Usage

1. **Run the application**:
    ```bash
    python app.py
    ```

2. **Access the application**:
    Open your web browser and navigate to `http://0.0.0.0:8080`.

## File Structure

- `app.py`: The main Flask application.
- `Dockerfile`: Dockerfile for containerizing the application.
- `data/`: Directory containing the datasets.
- `models/`: Directory containing the trained models.
- `static/`: Directory containing static files like images.
- `templates/`: Directory containing HTML templates.

## Routes

- `/`: Home page.
- `/cluster`: Clustering page where users can input features and get the predicted cluster.
- `/classification`: Classification page where users can input features and get the predicted class.
- `/python`: Page that displays activity durations and numbers for given dates.

## Functions

### Clustering and Classification

- **Cluster Prediction**: Takes 18 input features, scales them, transforms them using PCA, and predicts the cluster using a KMeans model. The results are visualized and displayed.
- **Class Prediction**: Takes 18 input features, scales them, and predicts the class using a SVM model. The predicted class is then displayed.

### Data Analysis

- **calculate_position_duration(data, date)**: Calculates the total duration spent inside and outside for a given date.
- **duration_datewise(data)**: Returns the inside and outside durations for all unique dates in the dataset.
- **calculate_activity_number(data, date)**: Calculates the number of 'placed' and 'picked' activities for a given date.
- **activity_datewise(data)**: Returns the number of 'placed' and 'picked' activities for all unique dates in the dataset.

## Example

Here’s an example of how to use the clustering feature:

1. Go to the clustering page (`/cluster`).
2. Input the required 18 features.
3. Click submit to see the predicted cluster and a visualization of the clustering result.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
