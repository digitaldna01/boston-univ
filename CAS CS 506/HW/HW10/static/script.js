document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("image-search-form").addEventListener("submit", async function(event) {
        event.preventDefault();  // Prevent form submission

        const submitButton = document.querySelector("button[type='submit']");
        submitButton.disabled = true; // 버튼 비활성화

        const queryType = document.getElementById("query-type").value;
        const embedType = document.getElementById("embed-type").value;
        
        const imageQuery = document.getElementById("image-query").files[0];
        const textQuery = document.getElementById("text-query").value;
        const hybridWeight = parseFloat(document.getElementById("hybrid-weight").value);

        const formData = new FormData();
        formData.append("query_type", queryType);
        formData.append("embed_type", embedType);
        formData.append("image_query", imageQuery);
        formData.append("text_query", textQuery);
        formData.append("hybrid_weight", hybridWeight);

        fetch("/run_experiment", {
            method: "POST",
            body: formData 
        })
        .then(response => response.json())
        .then(data => {
            // Show and set images if they exist
            const resultsDiv = document.getElementById("results");
            resultsDiv.style.display = "block";

            // clear previous results
            const resultContainer = document.getElementById("result-container");
            resultContainer.innerHTML = "";

            // Loop through the images and similarities
            data.images.forEach((image, index) => {
                console.log(image)
                // Create a new result item
                const resultItem = document.createElement("div");
                resultItem.className = 'result-item';

                // Create the image element
                const imgElment = document.createElement("img");
                imgElment.className = "result-image";
                imgElment.src = `/coco_images_resized/${image}`;
                imgElment.alt = `Search Result ${index + 1}`;

                // Create the similarity text
                const similarityText = document.createElement("p");
                similarityText.innerHTML = `Similarity: <span class="similarity-score">${data.top_sims[index]}<span>`;

                // Append the image and similarity text to the result item
                resultItem.appendChild(imgElment);
                resultItem.appendChild(similarityText);

                // Append the result item to the result container
                resultContainer.appendChild(resultItem);
            });

            submitButton.disabled = false;

        })
        .catch(error => {
            console.error("Error running experiment:", error);
            alert("An error occurred while running the experiment.");
            submitButton.disabled = false;
        });
    });
});