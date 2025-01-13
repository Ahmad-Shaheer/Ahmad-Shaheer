
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

  console.log(`loading.js: containerName='${containerName}', iconEl=`, iconEl, ', checkboxEl=', checkboxEl);

  if (iconEl) {
    iconEl.classList.remove('spinner');
  } else {
    console.warn(`loading.js: Could not find icon for ${containerName}`);
  }

  if (checkboxEl) {
    checkboxEl.disabled = false;
    checkboxEl.checked = true;
  } else {
    console.warn(`loading.js: Could not find checkbox for ${containerName}`);
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
