
console.log('loading.js: This file has been loaded by the browser.');

if (typeof window.healthyContainers !== 'undefined') {
  console.log('loading.js: healthyContainers =', window.healthyContainers);
} else {
  console.warn('loading.js: window.healthyContainers is undefined!');
}

// Attempt to update spinners and checkboxes
console.log('loading.js: Attempting to update spinners and checkboxes...');

window.healthyContainers.forEach(function(containerName) {
  var iconEl = document.getElementById('icon-' + containerName);
  var checkboxEl = document.getElementById('checkbox-' + containerName);

  if (checkboxEl) {
    // Ensure the checkbox is disabled initially
    checkboxEl.disabled = true;
}
  if (iconEl) {
    iconEl.classList.remove('spinner');
  } 

  if (checkboxEl) {
    checkboxEl.disabled = false;
    checkboxEl.checked = true;
  } 
});

// Auto-reload every 5 seconds
function autoReloadPage(intervalSeconds) {
  console.log(`loading.js: Scheduling page reload in ${intervalSeconds} seconds.`);
  setTimeout(function() {
    console.log('loading.js: Reloading now...');
    window.location.reload();
  }, intervalSeconds * 1000);
}

autoReloadPage(5);
