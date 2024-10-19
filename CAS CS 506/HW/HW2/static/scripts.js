
let currentStep = 0;
let totalSteps = 0;
let selectedPoints = [];

function generateInitialVisualization(){
    const numPoints = document.getElementById('numPoints').value || 300;
    const url = `/initial?numPoints=${numPoints}&t=${new Date().getTime()}`;

    const img = document.getElementById('data-visualization');
    img.src = url;
    img.style.display = 'block'; // Show the image
}

function stepThroughKMeans() {
    // Check if we need to initialize the KMeans process
    if (currentStep == 0) {
        const kClusters = document.getElementById('kClusters').value;
        const initMethod = document.getElementById('initMethod').value;

        if(initMethod === 'manual') {
            const encodedPoints = encodeURIComponent(JSON.stringify(selectedPoints));
            const url = `/generate_manual?k=${kClusters}&manuel_data=${encodedPoints}`;

            // Make an AJAX request to get the total steps from the server
        fetch(url)
            .then(response => response.text()) // Assuming the server returns a plain text with totalSteps
            .then(data => {
                totalSteps = parseInt(data, 10); // Convert the response to an integer
                if (isNaN(totalSteps)) {
                    console.error("Failed to retrieve total steps from the server.");
                    return;
                }
                // Start the visualization process
                updateVisualization();
        })
        .catch(error => console.error("Error during initialization:", error));
        }else{
            // Create the URL for the initial generation request
        const url = `/generate?k=${kClusters}&init_method=${initMethod}`;
        
        // Make an AJAX request to get the total steps from the server
        fetch(url)
            .then(response => response.text()) // Assuming the server returns a plain text with totalSteps
            .then(data => {
                totalSteps = parseInt(data, 10); // Convert the response to an integer
                if (isNaN(totalSteps)) {
                    console.error("Failed to retrieve total steps from the server.");
                    return;
                }
                // Start the visualization process
                updateVisualization();
            })
            .catch(error => console.error("Error during initialization:", error));
        }
    } else {
        // Check if we have reached the total steps
        if (currentStep >= totalSteps) {
            alert("KMeans has converged.");
            return; // Stop if we've reached the end
        }
        
        // Show the next step visualization
        updateVisualization();
    }
}
    

// Function to update the image for the current step
function updateVisualization() {
    const initMethod = document.getElementById('initMethod').value;
    if (initMethod === 'manual'){
        const canvas = document.getElementById('plotly-div');
        canvas.style.display = 'none';
    }
    const img = document.getElementById('data-visualization');
    
    // Add a timestamp to the URL to prevent caching
    const timestamp = new Date().getTime();
    img.src = `/step?step=${currentStep}&t=${timestamp}`;
    
    img.style.display = 'block'; // Show the image
    currentStep++; // Increment the current step after updating the image
}

// Function to run to convergence
function runToConvergence() {
    // Implement functionality to complete the algorithm
    if (currentStep == 0) {
        const kClusters = document.getElementById('kClusters').value;
        const initMethod = document.getElementById('initMethod').value;
        
        if(initMethod === 'manual') {
            const encodedPoints = encodeURIComponent(JSON.stringify(selectedPoints));
            const url = `/generate_manual?k=${kClusters}&manuel_data=${encodedPoints}`;

            // Make an AJAX request to get the total steps from the server
        fetch(url)
            .then(response => response.text()) // Assuming the server returns a plain text with totalSteps
            .then(data => {
                totalSteps = parseInt(data, 10); // Convert the response to an integer
                if (isNaN(totalSteps)) {
                    console.error("Failed to retrieve total steps from the server.");
                    return;
                }
                // Start the visualization process
                currentStep = totalSteps;
                updateVisualization();
        })
        .catch(error => console.error("Error during initialization:", error));
        }else{
            // Create the URL for the initial generation request
            const url = `/generate?k=${kClusters}&init_method=${initMethod}`;
        
            // Make an AJAX request to get the total steps from the server
            fetch(url)
                .then(response => response.text()) // Assuming the server returns a plain text with totalSteps
                .then(data => {
                    totalSteps = parseInt(data, 10); // Convert the response to an integer
                    if (isNaN(totalSteps)) {
                        console.error("Failed to retrieve total steps from the server.");
                        return;
                    }
                    // Start the visualization process
                    currentStep = totalSteps;
                    updateVisualization();
                })
                .catch(error => console.error("Error during initialization:", error));
        }
    } else {
        // Check if we have reached the total steps
        if (currentStep >= totalSteps) {
            alert("KMeans has converged.");
            return; // Stop if we've reached the end
        }
        
        // Show the next step visualization
        currentStep = totalSteps;
        updateVisualization();
    }
}

// Function to generate a new dataset
function generateNewDataset() {

    const numPoints = document.getElementById('numPoints').value || 300;
    const url = `/newDataset?numPoints=${numPoints}&t=${new Date().getTime()}`;

    currentStep = 0;
    totalSteps = 0;
    selectedPoints = [];
    // Reset the dropdown menu to "Select the Initialization Method"
    document.getElementById('initMethod').selectedIndex = 0;

    const img = document.getElementById('data-visualization');
    img.src = url;
    img.style.display = 'block'; // Show the image
}

// Function to reset the algorithm
function resetAlgorithm() {
    // Reset necessary variables and UI components
    const url = `/reset`;

    const img = document.getElementById('data-visualization');
    img.src = url;
    img.style.display = 'block'; // Show the image
    currentStep = 0;
    totalSteps = 0;
    selectedPoints = [];

    // Reset the dropdown menu to "Select the Initialization Method"
    document.getElementById('initMethod').selectedIndex = 0;
}


// From here the manual Starts
document.getElementById('initMethod').addEventListener('change', function () {
    const selectedMethod = this.value;
    const canvas = document.getElementById('plotly-div');
    const img = document.getElementById('data-visualization');

    if (selectedMethod === 'manual') {
        img.style.display = 'none';
        canvas.style.display = 'block';

        // Request Ajax for tne current Data points
        fetch('/getDataPoints')
            .then(response => response.json())
            .then(dataPoints => {
                // Use dataPoints to select manualy
                initManualSelection(dataPoints);
            })
        
    } else {
        canvas.style.display = 'none';
        img.style.display = 'block';
    }
});

function initManualSelection(initialData) {
    const kClusters = parseInt(document.getElementById('kClusters').value, 10);

    const trace = {
        x: initialData.map(point => point[0]),
        y: initialData.map(point => point[1]),
        mode: 'markers',
        type: 'scatter',
        marker: {color:'blue'}, // initial points in blue
        name: 'Data Points',
        showlegend: false
    };

    const layout = {
        title: 'Select k Points',
        xaxis: { title: 'X'},
        yaxis: {title: 'Y'},
        dragmode: 'select',
    };

    Plotly.newPlot('plotly-div', [trace], layout);

    const plotlyDiv = document.getElementById('plotly-div');

    plotlyDiv.on('plotly_click', function(data) {
        if(selectedPoints.length < kClusters){
            const x = data.points[0].x;
            const y = data.points[0].y;
            selectedPoints.push({ x, y });
            
            const newTrace = {
                x: selectedPoints.map(point => point.x),
                y: selectedPoints.map(point => point.y),
                mode: 'markers',
                marker: {color: 'red', size: 10, symbol: 'x'}, // Selected points in red with a border
                type: 'scatter',
                name: 'Selected Points',
                hoverinfo: 'text',
                showlegend: true
            };

            Plotly.addTraces(plotlyDiv, newTrace); // Add the new trace with the selected points

            if (selectedPoints.length === kClusters){
                console.log('Selected Points:', selectedPoints);
            }
        } else{
            alert('You have selected all k points. Run KMeans Algorithm');
        }
    });
}


// Automatically generate visualization on page load
window.onload = function() {
    generateInitialVisualization();
};
