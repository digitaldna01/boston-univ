document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    console.log('Uploading image...');
    const formData = new FormData();
    const fileInput = document.getElementById('file');
    const nColorsInput = document.getElementById('n_colors');

    formData.append('file', fileInput.files[0]);
    formData.append('n_colors', nColorsInput.value);

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
