import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_from_directory
import uuid
import threading

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'
MAX_IMAGES = 10
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'images': []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def cleanup_images():
    data = load_data()
    current_time = datetime.now()
    
    # Remove images older than 15 seconds
    data['images'] = [
        img for img in data['images'] 
        if (current_time - datetime.fromisoformat(img['timestamp'])).total_seconds() < 15
    ]
    
    # Remove actual image files
    for img in data['images']:
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, img['filename'])):
            data['images'].remove(img)
    
    save_data(data)
    
    # Schedule next cleanup
    threading.Timer(2, cleanup_images).start()

# Start cleanup thread
cleanup_images()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    data = load_data()
    return render_template('gallery.html', images=data['images'])

@app.route('/api/images')
def api_images():
    data = load_data()
    return jsonify(data['images'])

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    comment = request.form.get('comment', '')[:100]
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    if file.content_length > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large'}), 400
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Load and update data
    data = load_data()
    
    # Remove oldest images if max capacity reached
    if len(data['images']) >= MAX_IMAGES:
        data['images'] = data['images'][-(MAX_IMAGES-1):]
    
    # Add new image
    data['images'].append({
        'filename': filename,
        'comment': comment,
        'timestamp': datetime.now().isoformat()
    })
    
    save_data(data)
    
    return jsonify({'success': True, 'filename': filename}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)