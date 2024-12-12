# Image to Blender Converter

## Prerequisites

1. Install Blender and ensure it's accessible from command line
   - On Windows, add Blender to your PATH environment variable
   - On Linux/Mac, create a symlink if needed

2. Install Python dependencies:
```bash
pip install flask pillow trellis imageio
```

## Setup

1. Clone this repository
2. Navigate to the project directory
3. Run the Flask application:
```bash
python app.py
```
4. Open your web browser to http://localhost:5000

## Usage

1. Drag and drop an image onto the webpage (or click to select)
2. Wait for processing (this may take a few minutes)
3. Preview the 3D model in the video player
4. Click 'Download Blender File' to get the .blend file

## How it Works

1. Frontend accepts image upload
2. TRELLIS AI processes image into 3D model (GLB format)
3. Blender CLI converts GLB to .blend file
4. User downloads final .blend file

## Troubleshooting

1. If Blender conversion fails:
   - Ensure Blender is installed and accessible from command line
   - Try running `blender --version` in terminal to verify
   - Check the application logs for specific errors

2. If image processing fails:
   - Ensure image is in a supported format (PNG, JPG)
   - Try with a different image
   - Check console for error messages

## File Structure

- `app.py` - Flask backend
- `convert_glb.py` - Blender conversion script
- `index.html` - Web interface
- `script.js` - Frontend logic
- `outputs/` - Generated files directory
