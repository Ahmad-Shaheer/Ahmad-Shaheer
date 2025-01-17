
console.log('loading.js: This file has been loaded by the browser.');

if (typeof window.healthyContainers !== 'undefined') {
  console.log('loading.js: healthyContainers =', window.healthyContainers);
} else {
  console.warn('loading.js: window.healthyContainers is undefined!');
}

// Attempt to update spinners and checkboxes
console.log('loading.js: Attempting to update spinners and checkboxes...');

console.log(window.healthyContainers);
try{
  window.healthyContainers.forEach(function(containerName) {
    var spinnerEl = document.getElementById('icon-' + containerName);

    if (spinnerEl) {
        console.log(`Updating spinner for ${containerName}`);
        
        // Create checkbox and label
        const checkboxEl = document.createElement('input');
        checkboxEl.type = 'checkbox';
        checkboxEl.id = 'checkbox-' + containerName;
        checkboxEl.disabled = false; // Enable checkbox
        checkboxEl.checked = true;  // Mark as checked

        const labelEl = document.createElement('label');
        labelEl.htmlFor = 'checkbox-' + containerName;

        // Replace spinner with checkbox and label
        spinnerEl.replaceWith(checkboxEl, labelEl);
    } else {
        console.warn(`Spinner not found for ${containerName}`);
    }
  });
} catch (error) {
  console.error('loading.js: Error updating spinners and checkboxes:', error);
}

// Auto-reload every 5 seconds
function autoReloadPage(intervalSeconds) {
  console.log(`loading.js: Scheduling page reload in ${intervalSeconds} seconds.`);
  setTimeout(function() {
    console.log('loading.js: Reloading now...');
    window.location.reload();
  }, intervalSeconds * 1000);
}

autoReloadPage(5);
