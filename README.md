# House Price Prediction Web App

A Flask-based web application that predicts house prices using machine learning based on square footage, bedrooms, and bathrooms.

## Features

- **Interactive Web Interface**: Clean, modern UI for easy predictions
- **Model Management**: Load and switch between different trained models
- **Real-time Predictions**: Instant house price estimates with confidence levels
- **Model Information**: Detailed performance metrics and statistics
- **API Endpoints**: RESTful API for programmatic access

## Quick Start

1. **Install Requirements**
   ```bash
   pip install flask joblib scikit-learn pandas numpy
   ```

2. **Prepare Your Model**
   - Place your trained model files (.joblib or .pkl) in the `saved_models/` directory
   - Include metadata files for better functionality

3. **Run the App**
   ```bash
   python app.py
   ```

4. **Open Your Browser**
   - Go to `http://localhost:5000`
   - Load your model and start predicting!

## Project Structure

```
├── app.py                 # Main Flask application
├── saved_models/          # Directory for model files
├── templates/             # HTML templates
└── static/               # CSS, JS, images
```

## Model Requirements

The app expects models trained on these features:
- **Square Footage**: Above-grade living area
- **Bedrooms**: Number of bedrooms
- **Total Bathrooms**: Full + (Half × 0.5) bathrooms

## Built With

- **Flask**: Web framework
- **Bootstrap 5**: UI components
- **scikit-learn**: Model loading and predictions
- **Chart.js**: Data visualizations

## License

Open source - feel free to modify and use for your projects!