# Project Structure - Gluco-Guide

### Root Directory

- **`accounts`**: This app manages secure authentication and authorization for the web application.

- **`data`**: This directory stores CSV files containing datasets used to train the diabetes predictor model.

- **`diabetes_predictor`**: This is the root of our web application, where settings, URL routing, and HTTP request mapping are handled.

- **`main`**: The base app that manages most tasks. It contains the views for the web application and defines the database tables in `models.py`. Static files like CSS, JavaScript, and images are located in the `static` directory. This app also includes the `UserHealthSurveyForm` in `forms.py`.

- **`media`**: A directory for storing user-uploaded images, such as profile pictures.

- **`model`**: This directory contains the diabetes predictor model that has been trained.

- **`predictor`**: This app is responsible for predicting whether the user has diabetes. It takes necessary data from the user profile and daily calendar input, processes it, and loads the model to generate dietary suggestions based on the user's health condition. The dietary suggestions are derived from predefined conditions rather than directly from the model.

- **`saved_model`**: This directory stores the trained model and the scaler that assists in model indexing.

- **`templates`**: Contains all HTML templates, organized by app name for easy access.

- **`.gitignore`**: Specifies files and directories to be ignored by Git (e.g., virtual environments).

- **`build.sh`**: Contains commands used for deployment.

- **`db.sqlite3`**: A file-based database used to store necessary application data.

- **`manage.py`**: A script used to manage the Django server.

- **`model_training.ipynb`**: Documentation detailing the model training process.

- **`render.yaml`**: Contains necessary commands for hosting the application.

- **`requirements.txt`**: Lists the essential packages required for the application.

### How It Works

In the root of this application (`diabetes_predictor` directory), the `urls.py` file is responsible for URL routing. When a user makes a request to the base URL, it redirects to the `main` app, where the `urls.py` file handles further routing. For example, if a user requests `/accounts`, the request is routed to the `accounts` app for authentication. Similarly, requests to `/predictor` are directed to the `predictor` app. This routing occurs seamlessly in the background as users interact with buttons or links.

### How Dietary Suggestions Are Generated

When a user submits their daily health information, the predictor app processes the data in the background to determine if the user has diabetes. Simultaneously, it calculates a percentage indicating the user's health condition. Another view within the predictor app then runs, utilizing predefined conditions associated with the percentage to generate dietary suggestions. These suggestions are saved in the database along with the corresponding date.

### Conclusion

Gluco-Guide is designed to provide a seamless user experience while efficiently managing health data and generating personalized dietary recommendations based on predictive modeling. The modular structure ensures that each app has a specific purpose, facilitating easier maintenance and scalability of the application.
