const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const previewSection = document.getElementById('previewSection');
const videoPreview = document.getElementById('video-preview');
const exportBtn = document.getElementById('exportBtn');

// Handle drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#000';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = '#ccc';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    handleFile(e.dataTransfer.files[0]);
});

// Handle click to upload
dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) {
        alert('Please upload an image file');
        return;
    }

    // Show loading state
    dropZone.textContent = 'Processing...';
    dropZone.style.backgroundColor = '#f0f0f0';

    const formData = new FormData();
    formData.append('image', file);

    // Send to backend
    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Reset drop zone
        dropZone.textContent = 'Drop image here or click to upload';
        dropZone.style.backgroundColor = '';

        // Show preview section
        previewSection.classList.remove('hidden');
        videoPreview.src = data.video_url;
        
        // Enable export button if blend file is available
        if (data.blend_available) {
            exportBtn.disabled = false;
            exportBtn.textContent = 'Download Blender File';
            exportBtn.onclick = () => {
                fetch(`/download_blend/${data.id}`)
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'model.blend';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                });
            };
        } else {
            exportBtn.disabled = true;
            exportBtn.textContent = 'Blender conversion failed';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing image');
        dropZone.textContent = 'Drop image here or click to upload';
        dropZone.style.backgroundColor = '';
    });
}
