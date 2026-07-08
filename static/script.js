const video = document.getElementById('video');
const captureBtn = document.getElementById('capture');
const imageDataInput = document.getElementById('imageData');

// Start camera
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error("Camera not available:", err));

// Capture button
captureBtn.addEventListener('click', () => {
    if (video.videoWidth === 0 || video.videoHeight === 0) {
        alert("Camera not ready yet");
        return;
    }

    const maxWidth = 640;
    const maxHeight = 480;
    let width = video.videoWidth;
    let height = video.videoHeight;

    if (width > maxWidth) {
        height = Math.round(height * (maxWidth / width));
        width = maxWidth;
    }
    if (height > maxHeight) {
        width = Math.round(width * (maxHeight / height));
        height = maxHeight;
    }

    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(video, 0, 0, width, height);

    imageDataInput.value = canvas.toDataURL('image/jpeg', 0.6);

    // Submit form to detect currency
    document.getElementById('sendForm').submit();
});