import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(input_path, output_path, max_dimension):
    """
    Resize an image while maintaining aspect ratio to fit within the max_dimension.
    :param input_path: Path to the input image file.
    :param output_path: Path to save the resized image.
    :param max_dimension: Tuple (width, height) specifying the maximum dimensions.
    """
    with Image.open(input_path) as img:
        img.thumbnail(max_dimension)
        img.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    photos = []
    if request.method == 'POST':
        files = request.files.getlist('photos[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Resize the image using Pillow
                resized_filename = 'resized_' + filename
                resized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], resized_filename)
                resize_image(filepath, resized_filepath, (400, 400))  # Max dimension of 4 inches x 4 inches
                
                photos.append(resized_filename)
    return render_template('index.html', photos=photos)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
