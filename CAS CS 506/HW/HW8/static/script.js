document.getElementById("experiment-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form submission

    const start = parseFloat(document.getElementById("start").value);
    const end = parseFloat(document.getElementById("end").value);
    const stepNum = parseInt(document.getElementById("step_num").value);

    // Validation checks
    if (isNaN(start)) {
        alert("Please enter a valid number for Shift Start.");
        return;
    }

    if (isNaN(end)) {
        alert("Please enter a valid number for Shift End.");
        return;
    }

    if (isNaN(stepNum) || stepNum <= 0) {
        alert("Please enter a positive integer for Number of Steps.");
        return;
    }

    if (start >= end) {
        alert("Shift Start should be smaller than Shift End.");
        return;
    }

    // If all validations pass, submit the form
    fetch("/run_experiment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ start: start, end: end, step_num: stepNum })
    })
    .then(response => response.json())
    .then(data => {
        // Show and set images if they exist
        const resultsDiv = document.getElementById("results");
        resultsDiv.style.display = "block";

        const datasetImg = document.getElementById("dataset-img");
        if (data.dataset_img) {
            datasetImg.src = `/${data.dataset_img}`;
            datasetImg.style.display = "block";
        }

        const parametersImg = document.getElementById("parameters-img");
        if (data.parameters_img) {
            parametersImg.src = `/${data.parameters_img}`;
            parametersImg.style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error running experiment:", error);
        alert("An error occurred while running the experiment.");
    });
});