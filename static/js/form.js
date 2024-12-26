function handleStorageChange(selectElement) {
    updateStorageTool(selectElement);
    updateScreenStorageTool(selectElement);
  }

  function handleIntermediateChange(selectElement) {
    updateIntermediateTool(selectElement);
    updateScreenIntermediateTool(selectElement);
  }

  function handleStructuredChange(selectElement) {
    updateStructuredTool(selectElement);
    updateScreenStructuredTool(selectElement);
  }

  function handleSemiChange(selectElement) {
    updateSemiTool(selectElement);
    updateScreenSemiTool(selectElement);
  }





  function updateStorageTool(selectElement) {
    document.getElementById('storage_tool_value_temp').value = document.getElementById('storage_tool_value').value
    document.getElementById('storage_tool_value').value = selectElement.value;
    console.log("Storage tool value successfully updated to:", selectElement.value);
  }

  function updateIntermediateTool(selectElement) {
      document.getElementById('intermediate_storage_tool_value_temp').value = document.getElementById('intermediate_storage_tool_value').value
      document.getElementById('intermediate_storage_tool_value').value = selectElement.value;
      console.log("Ingestion tool value successfully updated to:", selectElement.value);
    }
  function updateStructuredTool(selectElement) {
    document.getElementById('structured_tool_value_temp').value = document.getElementById('structured_tool_value').value
    document.getElementById('structured_tool_value').value = selectElement.value;
    console.log("Ingestion tool value successfully updated to:", selectElement.value);
  }

  function updateSemiTool(selectElement) {
      document.getElementById('semi_structured_tool_value_temp').value = document.getElementById('semi_structured_tool_value').value
      document.getElementById('semi_structured_tool_value').value = selectElement.value;
      console.log("Ingestion tool value successfully updated to:", selectElement.value);
    }

  



//  let currentStorageTool = "{{ pipeline['Storage'] }}";
//  let currentIntermediateTool = "{{ pipeline['Intermediate Storage'] }}";
//  let currentStructuredTool = "{{ pipeline['Structured'] }}";
//  let currentSemiTool = "{{ pipeline['Semi'] }}";
  



  function updateScreenStorageTool(selectElement) {
      const selectedTool = selectElement.value;
      const previousTool = document.getElementById('storage_tool_value_temp').value;
      // currentStorageTool = selectedTool;
      const storageToolElement = document.getElementById('storage-tool');
      storageToolElement.innerHTML = `
      <img src="/static/images/${selectedTool}.svg" alt="${selectedTool} Icon" style="width: 40px; height: 40px;"/>
      <strong>Storage:</strong> ${selectedTool}
      `;

      const option = document.createElement('option');
      option.value = previousTool;
      option.textContent = previousTool;
      selectElement.appendChild(option);
      selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
      selectElement.selectedIndex = 0;
    }

    
  function updateScreenIntermediateTool(selectElement) {
      const selectedTool = selectElement.value;
      const previousTool = document.getElementById('intermediate_storage_tool_value_temp').value;
      currentIntermediateTool = selectedTool;
      const intermediateToolElement = document.getElementById('intermediate-storage-tool');
      intermediateToolElement.innerHTML = `
      <img src="/static/images/${currentIntermediateTool}.svg" alt="${currentIntermediateTool} Icon" style="width: 40px; height: 40px;"/>
      <strong>Intermediate Storage:</strong> ${currentIntermediateTool}
      `;

      const option = document.createElement('option');
      option.value = previousTool;
      option.textContent = previousTool;
      selectElement.appendChild(option);
      selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
      selectElement.selectedIndex = 0;
    }


  function updateScreenStructuredTool(selectElement) {
    const selectedTool = selectElement.value;
    const previousTool = document.getElementById('structured_tool_value_temp').value;
    currentStructuredTool = selectedTool;
    const structuredToolElement = document.getElementById('structured-tool');
    structuredToolElement.innerHTML = `
      <img src="/static/images/${currentStructuredTool}.svg" alt="${currentStructuredTool} Icon" style="width: 40px; height: 40px;"/>
      <strong>Structured Storage:</strong> ${currentStructuredTool}
      `;

    const option = document.createElement('option');
    option.value = previousTool;
    option.textContent = previousTool;
    selectElement.appendChild(option);
    selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
    selectElement.selectedIndex = 0;
  }


  function updateScreenSemiTool(selectElement) {
    const selectedTool = selectElement.value;
    const previousTool = document.getElementById('semi_structured_tool_value_temp').value;
    currentSemiTool = selectedTool;
    const semiToolElement = document.getElementById('semi-tool');
    semiToolElement.innerHTML = `
      <img src="/static/images/${currentSemiTool}.svg" alt="${currentSemiTool} Icon" style="width: 40px; height: 40px;"/>
      <strong>Semi Storage:</strong> ${currentSemiTool}
      `;

    const option = document.createElement('option');
    option.value = previousTool;
    option.textContent = previousTool;
    selectElement.appendChild(option);
    selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
    selectElement.selectedIndex = 0;
  }