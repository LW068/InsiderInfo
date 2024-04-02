const { exec } = require('child_process');
const path = require('path');

// Function to run the Python script and update the chart
function updateChart() {
    const pythonScript = path.join(__dirname, 'candles.py');
    exec(`python ${pythonScript}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            return;
        }
        console.log(`Python script output: ${stdout}`);
    });
}

// Function to refresh the page
function refreshPage() {
    window.location.reload();
}

// Update the chart immediately on script start
updateChart();

// Refresh the page every 60 seconds (60000 milliseconds)
setInterval(() => {
    updateChart(); // Update the chart data
    refreshPage(); // Refresh the page
}, 60000); // 60 seconds interval
