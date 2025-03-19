document.getElementById('runScriptsButton').addEventListener('click', async () => {
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-container');
    const statusText = document.getElementById('status-text');

    // Reset Progress Bar
    progressBar.style.width = '0%';
    progressContainer.style.display = 'block';
    statusText.textContent = 'Processing...';

    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        progressBar.style.width = `${progress}%`;
        if (progress >= 100) clearInterval(progressInterval);
    }, 1500);

    try {
        const response = await fetch('http://localhost:5000/api/script/run-scripts', { method: 'POST' });

        if (!response.ok) {
            throw new Error('Failed to run scripts');
        }

        // Download the file
        const fileBlob = await response.blob();

        const url = window.URL.createObjectURL(fileBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'newOrder.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Progress Bar Completion
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        statusText.textContent = 'Success! File downloaded.';
    } catch (error) {
        console.error(' Error:', error);
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        statusText.textContent = 'Error: Failed to run scripts.';
    }
});
