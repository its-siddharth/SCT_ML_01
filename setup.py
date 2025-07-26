#!/usr/bin/env python3
"""
House Price Prediction Web App Setup Script
This script sets up the Flask web application with all necessary files and directories.
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directory_structure():
    """Create the necessary directory structure"""
    directories = [
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'saved_models'
    ]
    
    print("📁 Setting up directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created: {directory}")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = """Flask==2.3.3
joblib==1.3.2
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
pickle-mixin==1.0.2
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✓ Created requirements.txt")

def create_base_template():
    """Create the base HTML template"""
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}House Price Predictor{% endblock %}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 2rem auto;
            padding: 2rem;
            max-width: 1200px;
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .btn-primary {
            background: linear-gradient(45deg, var(--secondary-color), #5dade2);
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-weight: 600;
        }
        
        .prediction-result {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
        }
        
        .confidence-high { background-color: var(--success-color); color: white; }
        .confidence-medium { background-color: var(--warning-color); color: white; }
        .confidence-low { background-color: var(--danger-color); color: white; }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: var(--success-color); }
        .status-offline { background-color: var(--danger-color); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-home"></i> House Price Predictor
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('load_model_page') }}">Load Model</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('predict') }}">Predict</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('model_info_page') }}">Model Info</a>
                    </li>
                    <li class="nav-item">
                        <span class="nav-link">
                            <span class="status-indicator {{ 'status-online' if model_loaded else 'status-offline' }}"></span>
                            {{ 'Model Loaded' if model_loaded else 'No Model' }}
                        </span>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid" style="margin-top: 80px;">
        <div class="main-container">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            {% block content %}{% endblock %}
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>"""
    
    with open('templates/base.html', 'w') as f:
        f.write(base_html)
    print("✓ Created templates/base.html")

def create_templates():
    """Create all HTML templates"""
    
    # Index template
    index_html = """{% extends "base.html" %}
{% block content %}
<div class="text-center mb-5">
    <h1 class="display-4 mb-3"><i class="fas fa-home text-primary"></i> House Price Predictor</h1>
    <p class="lead">Predict house prices using machine learning</p>
</div>

<div class="row g-4">
    <div class="col-md-4">
        <div class="card text-center h-100">
            <div class="card-body">
                <i class="fas fa-upload fa-3x text-primary mb-3"></i>
                <h4>Load Model</h4>
                <p>Upload your trained model</p>
                <a href="{{ url_for('load_model_page') }}" class="btn btn-primary">Load Model</a>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center h-100">
            <div class="card-body">
                <i class="fas fa-calculator fa-3x text-primary mb-3"></i>
                <h4>Predict Price</h4>
                <p>Get price predictions</p>
                <a href="{{ url_for('predict') }}" class="btn btn-primary">Predict Price</a>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center h-100">
            <div class="card-body">
                <i class="fas fa-info-circle fa-3x text-primary mb-3"></i>
                <h4>Model Info</h4>
                <p>View model details</p>
                <a href="{{ url_for('model_info_page') }}" class="btn btn-primary">View Info</a>
            </div>
        </div>
    </div>
</div>

{% if not model_loaded %}
<div class="alert alert-warning text-center mt-4">
    <strong>No Model Loaded</strong><br>
    Please load a model first to start making predictions.
</div>
{% endif %}
{% endblock %}"""
    
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    
    # Load model template
    load_model_html = """{% extends "base.html" %}
{% block content %}
<h2><i class="fas fa-upload text-primary"></i> Load Prediction Model</h2>

<div class="card mt-4">
    <div class="card-body">
        {% if models %}
        <table class="table">
            <thead>
                <tr><th>Model File</th><th>Size</th><th>Modified</th><th>Action</th></tr>
            </thead>
            <tbody>
                {% for model in models %}
                <tr>
                    <td>{{ model.filename }}</td>
                    <td>{{ "%.1f KB"|format(model.size / 1024) }}</td>
                    <td>{{ model.modified }}</td>
                    <td>
                        <button class="btn btn-primary btn-sm load-model-btn" 
                                data-model-path="{{ model.path }}"
                                data-metadata-path="{{ model.metadata_path or '' }}">
                            Load
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="text-center">
            <p>No models found. Place your .joblib or .pkl files in the saved_models directory.</p>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.querySelectorAll('.load-model-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const modelPath = this.getAttribute('data-model-path');
        const metadataPath = this.getAttribute('data-metadata-path');
        
        fetch('/api/load_model', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({model_path: modelPath, metadata_path: metadataPath})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Model loaded successfully!');
                window.location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    });
});
</script>
{% endblock %}"""
    
    with open('templates/load_model.html', 'w') as f:
        f.write(load_model_html)
    
    # Predict template
    predict_html = """{% extends "base.html" %}
{% block content %}
<h2><i class="fas fa-calculator text-primary"></i> House Price Prediction</h2>

{% if not model_loaded %}
<div class="alert alert-warning">
    No model loaded. <a href="{{ url_for('load_model_page') }}">Load a model first</a>.
</div>
{% else %}

<div class="row">
    <div class="col-lg-6">
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Square Footage</label>
                        <input type="number" class="form-control" name="square_footage" 
                               placeholder="e.g., 2000" required min="1">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Bedrooms</label>
                        <input type="number" class="form-control" name="bedrooms" 
                               placeholder="e.g., 3" required min="1">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Total Bathrooms</label>
                        <input type="number" class="form-control" name="total_bathrooms" 
                               placeholder="e.g., 2.5" required min="0.5" step="0.5">
                    </div>
                    <button type="submit" class="btn btn-primary">Predict Price</button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-lg-6">
        {% if prediction_result %}
        <div class="prediction-result">
            <h3>Prediction Result</h3>
            <div class="display-4">{{ prediction_result.formatted_price }}</div>
            <span class="badge confidence-{{ prediction_result.confidence.lower() }}">
                {{ prediction_result.confidence }} Confidence
            </span>
        </div>
        {% else %}
        <div class="card">
            <div class="card-body text-center">
                <i class="fas fa-chart-line fa-3x text-muted mb-3"></i>
                <h5>Ready for Prediction</h5>
                <p>Enter house details to get a price prediction.</p>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endif %}
{% endblock %}"""
    
    with open('templates/predict.html', 'w') as f:
        f.write(predict_html)
    
    # Model info template
    model_info_html = """{% extends "base.html" %}
{% block content %}
<h2><i class="fas fa-info-circle text-primary"></i> Model Information</h2>

{% if model_loaded and model_info %}
<div class="row">
    <div class="col-lg-6">
        <div class="card">
            <div class="card-header"><h5>Basic Information</h5></div>
            <div class="card-body">
                <p><strong>Model Type:</strong> {{ model_info.model_type }}</p>
                <p><strong>Loaded At:</strong> {{ model_info.loaded_at }}</p>
                {% if model_info.r2_score %}
                <p><strong>R² Score:</strong> {{ "%.4f"|format(model_info.r2_score) }}</p>
                <p><strong>RMSE:</strong> ${{ "{:,.0f}".format(model_info.rmse) }}</p>
                {% endif %}
            </div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="card">
            <div class="card-header"><h5>Features</h5></div>
            <div class="card-body">
                {% for feature in model_info.features %}
                <span class="badge bg-secondary">{{ feature }}</span>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="alert alert-warning">
    No model loaded. <a href="{{ url_for('load_model_page') }}">Load a model first</a>.
</div>
{% endif %}
{% endblock %}"""
    
    with open('templates/model_info.html', 'w') as f:
        f.write(model_info_html)
    
    print("✓ Created all HTML templates")

def create_run_script():
    """Create a simple run script"""
    run_script = """#!/usr/bin/env python3
\"\"\"
Simple script to run the House Price Prediction Web App
\"\"\"

import os
import sys

def main():
    print("🏠 House Price Prediction Web App")
    print("=" * 50)
    
    # Check if Flask app exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        print("Please make sure the Flask application file is named 'app.py'")
        return
    
    # Check if saved_models directory exists
    if not os.path.exists('saved_models'):
        print("📁 Creating saved_models directory...")
        os.makedirs('saved_models')
    
    # Check for model files
    model_files = [f for f in os.listdir('saved_models') if f.endswith(('.joblib', '.pkl'))]
    if model_files:
        print(f"✓ Found {len(model_files)} model file(s)")
    else:
        print("⚠️  No model files found in saved_models directory")
        print("   Copy your .joblib or .pkl model files to the saved_models directory")
    
    print("\\n🚀 Starting web application...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("\\n" + "=" * 50)
    
    # Run the Flask app
    os.system('python app.py')

if __name__ == "__main__":
    main()
"""
    
    with open('run_app.py', 'w') as f:
        f.write(run_script)
    
    # Make it executable on Unix systems
    try:
        os.chmod('run_app.py', 0o755)
    except:
        pass
    
    print("✓ Created run_app.py")

def create_readme():
    """Create README file with instructions"""
    readme = """# House Price Prediction Web App

A Flask-based web application for predicting house prices using your trained machine learning model.

## Features

- 🏠 **Load Models**: Upload and switch between different trained models
- 📊 **Price Prediction**: Get instant house price predictions
- 📈 **Model Information**: View detailed model performance metrics
- 🎨 **Modern UI**: Clean, responsive web interface

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Model Files
Copy your trained model files to the `saved_models` directory:
- `your_model.joblib` (recommended) or `your_model.pkl`
- `your_model_metadata.json` (optional, for enhanced features)

### 3. Run the Application
```bash
python run_app.py
```
or
```bash
python app.py
```

### 4. Open Your Browser
Navigate to: http://localhost:5000

## File Structure
```
house-price-app/
├── app.py                 # Main Flask application
├── run_app.py            # Simple run script
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── load_model.html
│   ├── predict.html
│   └── model_info.html
├── static/              # Static files (CSS, JS, images)
├── saved_models/        # Your trained models go here
└── README.md           # This file
```

## Model Requirements

Your model should be a trained scikit-learn LinearRegression model that expects 3 features:
1. **Square Footage** (numerical)
2. **Bedrooms** (numerical)
3. **Total Bathrooms** (numerical, can be decimal like 2.5)

## Usage

1. **Load Model**: Go to "Load Model" page and select your model file
2. **Make Predictions**: Enter house details in the "Predict Price" page
3. **View Model Info**: Check model performance and details

## API Endpoints

- `GET /` - Home page
- `GET /load_model` - Model loading page
- `POST /api/load_model` - Load model API
- `GET/POST /predict` - Prediction page/API
- `GET /model_info` - Model information page
- `GET /api/model_info` - Model info API

## Troubleshooting

### Model Won't Load
- Ensure model file is in `saved_models/` directory
- Check that model is a valid joblib/pickle file
- Verify model was trained with scikit-learn

### Predictions Fail
- Make sure a model is loaded first
- Check that input values are positive numbers
- Verify model expects the correct feature format

### Port Already in Use
The app runs on port 5000 by default. If it's in use, modify the `app.run()` line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## Development

To modify the application:
1. Edit `app.py` for backend logic
2. Modify templates in `templates/` for frontend
3. Add CSS/JS files to `static/` directory

## License

This project is open source. Feel free to modify and distribute.
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    print("✓ Created README.md")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function"""
    print("🏠 House Price Prediction Web App Setup")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Create files
    create_requirements_file()
    create_base_template()
    create_templates()
    create_run_script()
    create_readme()
    
    print("\n" + "=" * 50)
    print("✅ SETUP COMPLETE!")
    print("=" * 50)
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Copy your model files to the saved_models/ directory")
    print("3. Save the Flask app code as 'app.py'")
    print("4. Run the app: python run_app.py")
    print("5. Open http://localhost:5000 in your browser")
    
    print("\n📁 Files Created:")
    files_created = [
        "requirements.txt",
        "run_app.py", 
        "README.md",
        "templates/base.html",
        "templates/index.html",
        "templates/load_model.html", 
        "templates/predict.html",
        "templates/model_info.html",
        "static/css/ (directory)",
        "static/js/ (directory)",
        "saved_models/ (directory)"
    ]
    
    for file in files_created:
        print(f"   ✓ {file}")
    
    # Ask if user wants to install dependencies
    print(f"\n🤔 Install dependencies now? (y/n): ", end="")
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes']:
            install_dependencies()
        else:
            print("⏭️  Skipping dependency installation")
    except KeyboardInterrupt:
        print("\n⏭️  Skipping dependency installation")
    
    print(f"\n🎉 Ready to go! Your web app is set up and ready to use.")
    print(f"📖 Check README.md for detailed instructions.")

if __name__ == "__main__":
    main()