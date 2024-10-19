document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    console.log('Uploading image...');
    const formData = new FormData();
    const fileInput = document.getElementById('file');
    const rankInput = document.getElementById('rank');

    // Make the formData Package to send it to compress
    formData.append('file', fileInput.files[0]);
    formData.append('rank', rankInput.value);

    const response = await fetch('/compress', {
        method: 'POST',
        body: formData,
    });

    const imageBlob = await response.blob();
    const imageURL = URL.createObjectURL(imageBlob);

    const compressedImage = document.getElementById('compressedImage');
    compressedImage.src = imageURL;
    compressedImage.style.display = 'block';
});
