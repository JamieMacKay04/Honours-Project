import React from 'react';

const RunScriptsButton = () => {
    const handleButtonClick = async () => {
        try {
            // Send POST request to trigger the Python scripts
            const response = await fetch('http://localhost:5000/run-scripts', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Failed to run scripts');
            }

            // Get the CSV file data from the response
            const fileBlob = await response.blob();

            // Create a temporary link to download the CSV file
            const url = window.URL.createObjectURL(fileBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'newOrder.csv'; // Specify the filename
            link.click();

        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <button className="add-order-button" onClick={handleButtonClick}>
                Run Scripts and Fetch New Orders
            </button>
        </div>
    );
};

export default RunScriptsButton;
