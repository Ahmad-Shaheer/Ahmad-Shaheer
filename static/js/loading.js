    
    // Enable and check the boxes for the healthy containers
    healthyContainers.forEach(function(containerName) {
        var iconEl = document.getElementById("icon-" + containerName);
        var checkboxEl = document.getElementById("checkbox-" + containerName);

        if (iconEl) {
            iconEl.classList.remove("spinner");  // Removes the spinner animation
        }
        if (checkboxEl) {
            checkboxEl.disabled = false;         // Enable the checkbox
            checkboxEl.checked = true;           // Mark it checked
        }
    });

    // Optionally, if you want to do a client-side redirect *after* everything is healthy:
    // You can compare the number of healthy containers to the total number of services.
    if (healthyContainers.length === totalServices) {
        // All services are healthy - redirect to final page:
        window.location.href = "{{ url_for('final_page') }}";
    }