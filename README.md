# Waste Classification

A deep learning-based system for classifying different types of waste materials. This project includes model training scripts and a web application interface for easy interaction.

---

## Features

- Waste classification using deep learning models  
- Web app interface for uploading and classifying waste images  
- Database integration for storing classification data

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/himanshuXDebug/Waste-Classification.git
cd Waste-Classification
2. Set Up a Python Virtual Environment (recommended)

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Required Packages

pip install -r requirements.txt
Dataset
Download the dataset required for training and testing from the following link:

Download Dataset
https://drive.google.com/drive/folders/1CTvT_gnTvwlcKwJ8yz4jUOs0JYTKrplA?usp=drive_link
Extract the dataset and place it in the appropriate directory as required by the training scripts.

Usage
To Train the Model
Navigate to the training directory and run the training script:

python Train-model/train.py
To Run the Web Application
python app.py
Open your browser and visit http://localhost:5000 to use the application.

Project Structure
Train-model/ - Contains scripts to train the waste classification model

app.py, Main.py, routes.py - Flask web app files

static/ - Static files for the web app (CSS, JS, images)

templates/ - HTML templates for the web app

ECOFY.db - SQLite database file
