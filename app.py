# ============================================================================
# FLASK WEB APPLICATION FOR HOUSE PRICE PREDICTION
# ============================================================================

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import joblib
import pickle
import json
import os
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables for the loaded model
loaded_model = None
model_metadata = None
model_info = None

# ============================================================================
# MODEL MANAGEMENT FUNCTIONS
# ============================================================================

def load_model_from_file(model_path, metadata_path=None):
    """Load model from file with error handling"""
    global loaded_model, model_metadata, model_info
    
    try:
        # Determine file type and load accordingly
        if model_path.endswith('.joblib'):
            loaded_model = joblib.load(model_path)
            logger.info(f"Model loaded successfully with joblib from: {model_path}")
        elif model_path.endswith('.pkl'):
            with open(model_path, 'rb') as file:
                loaded_model = pickle.load(file)
            logger.info(f"Model loaded successfully with pickle from: {model_path}")
        else:
            raise ValueError("Unsupported model file format. Use .joblib or .pkl")
        
        # Load metadata if available
        model_metadata = None
        if metadata_path and os.path.exists(metadata_path):
            with open(metadata_path, 'r') as file:
                model_metadata = json.load(file)
            logger.info(f"Metadata loaded from: {metadata_path}")
        
        # Set model info
        model_info = {
            'model_path': model_path,
            'metadata_path': metadata_path,
            'loaded_at': datetime.now().isoformat(),
            'model_type': 'LinearRegression',
            'features': ['Square_Footage', 'Bedrooms', 'Total_Bathrooms']
        }
        
        if model_metadata:
            model_info.update({
                'r2_score': model_metadata.get('r2_score'),
                'rmse': model_metadata.get('rmse'),
                'mae': model_metadata.get('mae'),
                'training_samples': model_metadata.get('training_samples')
            })
        
        return True, "Model loaded successfully!"
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False, f"Error loading model: {str(e)}"

def predict_price(square_footage, bedrooms, total_bathrooms):
    """Make prediction using loaded model"""
    try:
        if loaded_model is None:
            return None, "No model loaded. Please load a model first."
        
        # Validate inputs
        if square_footage <= 0 or bedrooms <= 0 or total_bathrooms <= 0:
            return None, "All values must be positive numbers."
        
        # Make prediction
        features = [[float(square_footage), float(bedrooms), float(total_bathrooms)]]
        prediction = loaded_model.predict(features)[0]
        
        # Calculate confidence (simplified version)
        confidence = calculate_confidence(square_footage, bedrooms, total_bathrooms)
        
        result = {
            'predicted_price': float(prediction),
            'formatted_price': f"${prediction:,.2f}",
            'confidence': confidence,
            'inputs': {
                'square_footage': square_footage,
                'bedrooms': bedrooms,
                'total_bathrooms': total_bathrooms
            }
        }
        
        return result, None
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return None, f"Prediction error: {str(e)}"

def calculate_confidence(square_footage, bedrooms, total_bathrooms):
    """Calculate prediction confidence"""
    if not model_metadata or 'feature_ranges' not in model_metadata:
        return "Unknown"
    
    try:
        ranges = model_metadata['feature_ranges']
        features = ['Square_Footage', 'Bedrooms', 'Total_Bathrooms']
        values = [square_footage, bedrooms, total_bathrooms]
        
        confidence_scores = []
        
        for feature, value in zip(features, values):
            if feature in ranges:
                min_val = ranges[feature]['min']
                max_val = ranges[feature]['max']
                mean_val = ranges[feature]['mean']
                std_val = ranges[feature]['std']
                
                # Calculate z-score
                z_score = abs((value - mean_val) / std_val) if std_val > 0 else 0
                
                # Score based on z-score
                if z_score <= 1:
                    confidence_scores.append(0.9)
                elif z_score <= 2:
                    confidence_scores.append(0.7)  
                elif z_score <= 3:
                    confidence_scores.append(0.5)
                else:
                    confidence_scores.append(0.3)
        
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            if avg_confidence >= 0.8:
                return "High"
            elif avg_confidence >= 0.6:
                return "Medium"
            else:
                return "Low"
        
        return "Unknown"
        
    except Exception as e:
        logger.error(f"Confidence calculation error: {str(e)}")
        return "Unknown"

def get_available_models():
    """Get list of available model files"""
    models = []
    
    # Check saved_models directory
    models_dir = "saved_models"
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith(('.joblib', '.pkl')):
                model_path = os.path.join(models_dir, file)
                metadata_path = None
                
                # Look for corresponding metadata file
                base_name = file.rsplit('.', 1)[0]
                potential_metadata = os.path.join(models_dir, f"{base_name}_metadata.json")
                if os.path.exists(potential_metadata):
                    metadata_path = potential_metadata
                
                models.append({
                    'filename': file,
                    'path': model_path,
                    'metadata_path': metadata_path,
                    'size': os.path.getsize(model_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(model_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return sorted(models, key=lambda x: x['modified'], reverse=True)

# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         model_loaded=loaded_model is not None,
                         model_info=model_info)

@app.route('/load_model')
def load_model_page():
    """Model loading page"""
    available_models = get_available_models()
    return render_template('load_model.html', 
                         models=available_models,
                         current_model=model_info)

@app.route('/api/load_model', methods=['POST'])
def api_load_model():
    """API endpoint to load a model"""
    try:
        model_path = request.json.get('model_path')
        metadata_path = request.json.get('metadata_path')
        
        if not model_path:
            return jsonify({'success': False, 'message': 'Model path is required'})
        
        if not os.path.exists(model_path):
            return jsonify({'success': False, 'message': 'Model file not found'})
        
        success, message = load_model_from_file(model_path, metadata_path)
        
        if success:
            return jsonify({
                'success': True, 
                'message': message,
                'model_info': model_info
            })
        else:
            return jsonify({'success': False, 'message': message})
            
    except Exception as e:
        logger.error(f"API load model error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page"""
    if request.method == 'GET':
        return render_template('predict.html', 
                             model_loaded=loaded_model is not None,
                             model_info=model_info)
    
    # Handle POST request for prediction
    try:
        square_footage = float(request.form.get('square_footage', 0))
        bedrooms = float(request.form.get('bedrooms', 0))
        total_bathrooms = float(request.form.get('total_bathrooms', 0))
        
        result, error = predict_price(square_footage, bedrooms, total_bathrooms)
        
        if error:
            flash(f'Error: {error}', 'error')
            return render_template('predict.html', 
                                 model_loaded=loaded_model is not None,
                                 model_info=model_info)
        
        return render_template('predict.html',
                             model_loaded=loaded_model is not None,
                             model_info=model_info,
                             prediction_result=result)
                             
    except ValueError as e:
        flash('Please enter valid numbers for all fields.', 'error')
        return render_template('predict.html', 
                             model_loaded=loaded_model is not None,
                             model_info=model_info)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        flash(f'Prediction error: {str(e)}', 'error')
        return render_template('predict.html', 
                             model_loaded=loaded_model is not None,
                             model_info=model_info)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.json
        square_footage = float(data.get('square_footage', 0))
        bedrooms = float(data.get('bedrooms', 0))
        total_bathrooms = float(data.get('total_bathrooms', 0))
        
        result, error = predict_price(square_footage, bedrooms, total_bathrooms)
        
        if error:
            return jsonify({'success': False, 'message': error})
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/model_info')
def model_info_page():
    """Model information page"""
    return render_template('model_info.html',
                         model_loaded=loaded_model is not None,
                         model_info=model_info,
                         model_metadata=model_metadata)

@app.route('/api/model_info')
def api_model_info():
    """API endpoint for model information"""
    if loaded_model is None:
        return jsonify({'success': False, 'message': 'No model loaded'})
    
    return jsonify({
        'success': True,
        'model_info': model_info,
        'model_metadata': model_metadata
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return render_template('error.html',
                         error_code=500, 
                         error_message="Internal server error"), 500

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Try to auto-load the most recent model
    available_models = get_available_models()
    if available_models:
        latest_model = available_models[0]
        success, message = load_model_from_file(latest_model['path'], latest_model['metadata_path'])
        if success:
            logger.info(f"Auto-loaded latest model: {latest_model['filename']}")
        else:
            logger.warning(f"Failed to auto-load model: {message}")
    
    print("="*60)
    print("🏠 HOUSE PRICE PREDICTION WEB APP")
    print("="*60)
    print(f"🚀 Starting Flask web server...")
    print(f"🌐 Open your browser and go to: http://localhost:5000")
    print(f"📁 Make sure your saved_models directory contains the model files")
    print("="*60)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)