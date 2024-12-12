from flask import Flask, request, jsonify, send_file
from PIL import Image
import os
import subprocess
from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils
import uuid
import imageio

app = Flask(__name__)

# Initialize TRELLIS pipeline
pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
pipeline.cuda()

# Storage for processed files
OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_to_blend(glb_path, blend_path):
    """Convert GLB to Blend file using Blender's command line"""
    blender_cmd = 'blender'
    script_path = os.path.join(os.path.dirname(__file__), 'convert_glb.py')
    
    try:
        subprocess.run([
            blender_cmd,
            '--background',
            '--python', script_path,
            '--',
            glb_path,
            blend_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e}")
        return False

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    image = Image.open(file)
    
    # Generate unique ID for this process
    process_id = str(uuid.uuid4())
    process_dir = os.path.join(OUTPUT_DIR, process_id)
    os.makedirs(process_dir, exist_ok=True)

    # Run TRELLIS pipeline
    outputs = pipeline.run(image)

    # Generate and save preview video
    video = render_utils.render_video(outputs['gaussian'][0])['color']
    video_path = os.path.join(process_dir, 'preview.mp4')
    imageio.mimsave(video_path, video, fps=30)

    # Generate and save GLB
    glb = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        simplify=0.95,
        texture_size=1024
    )
    glb_path = os.path.join(process_dir, 'model.glb')
    blend_path = os.path.join(process_dir, 'model.blend')
    glb.export(glb_path)

    # Convert GLB to Blend
    success = convert_to_blend(glb_path, blend_path)

    return jsonify({
        'id': process_id,
        'video_url': f'/outputs/{process_id}/preview.mp4',
        'blend_available': success
    })

@app.route('/download_blend/<process_id>')
def download_blend(process_id):
    blend_path = os.path.join(OUTPUT_DIR, process_id, 'model.blend')
    if not os.path.exists(blend_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(blend_path, as_attachment=True, download_name='model.blend')

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename))

if __name__ == '__main__':
    app.run(debug=True)
