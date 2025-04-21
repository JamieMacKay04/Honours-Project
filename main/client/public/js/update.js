let selectedFile = null;

// Function to trigger file input on "Select File" button click
function triggerFileInput() {
    document.getElementById('file-upload').click();
}

// Function to handle when a file is selected
function fileSelected(event) {
    selectedFile = event.target.files[0];  // Get the selected file
    if (selectedFile) {
        // Enable the "Submit File" button when a file is selected
        document.querySelector('.submit-file-button').disabled = false;
        
        // Display the file name next to the button
        document.getElementById('file-name').textContent = selectedFile.name;
    }
}

// Function to submit the file
function submitFile() {
    if (!selectedFile) {
        alert('Please select a file first.');
        return;
    }

    // Example file upload (use your actual endpoint)
    const formData = new FormData();
    formData.append('file', selectedFile);

    fetch('/upload-endpoint', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('File uploaded successfully!');
        document.querySelector('.submit-file-button').disabled = true; // Disable after upload
        document.getElementById('file-upload').value = ''; // Reset the file input
        document.getElementById('file-name').textContent = ''; // Clear file name display
    })
    .catch(error => {
        alert('Error uploading file: ' + error.message);
    });
}
