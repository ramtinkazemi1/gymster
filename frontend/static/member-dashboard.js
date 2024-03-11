document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');
  
    searchForm.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const zipcode = document.getElementById('zipcode').value;
      const radius = document.getElementById('radius').value;
  
      // Here you can implement the logic to fetch coaches based on zipcode and radius
      // For demonstration purposes, let's just display a message with the entered values
  
      searchResults.innerHTML = `
        <p>Searching for coaches near ${zipcode} within ${radius} miles...</p>
        <!-- Display actual search results here -->
      `;
    });
  
    const radiusInput = document.getElementById('radius');
    const radiusOutput = document.getElementById('radius-value');
  
    // Update the output value with the current value of the radius input
    radiusInput.addEventListener('input', function() {
      radiusOutput.textContent = radiusInput.value;
    });
  });
  