document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.getElementById('search-form');
  const searchResults = document.getElementById('search-results');

  // Add event listener to the search button
  const searchButton = document.getElementById('search-button');
  searchButton.addEventListener('click', function(event) {
    event.preventDefault();
    searchCoaches();
  });


const radiusInput = document.getElementById('radius');
const radiusOutput = document.getElementById('radius-value');

// Add an event listener to the range input element
radiusInput.addEventListener('input', function() {
    // Update the content of the output element with the current value of the range input
    radiusOutput.textContent = this.value;
});

  function searchCoaches() {
    // Retrieve the user's zipcode and selected radius from the form
    const zipcode = document.getElementById('zipcode').value;
    const radius = document.getElementById('radius').value;

    // Make AJAX request to the server to search for coaches
    fetch('/search_coaches', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ zipcode: zipcode, radius: radius })
    })
    .then(response => response.json())
    .then(coaches => {
      // Clear previous search results
      searchResults.innerHTML = '';

      // Display search results
      coaches.forEach(coach => {
        const coachCard = createCoachCard(coach);
        searchResults.appendChild(coachCard);
      });
    })
    .catch(error => {
      console.error('Error searching for coaches:', error);
    });
  }

  function createCoachCard(coach) {
    // Create a div element for the coach card
    const card = document.createElement('div');
    card.classList.add('coach-card');

    // Populate the card with coach information
    card.innerHTML = `
      <img src="${coach.profile_picture}" alt="Profile Picture">
      <h3>${coach.full_name}</h3>
      <p>Bio: ${coach.bio}</p>
      <p>Degree and Certs: ${coach.degree_and_certs}</p>
      <p>Experiences: ${coach.experiences}</p>
      <p>Specialty: ${coach.specialty}</p>
      <p>Preferred gym #1: ${coach.preferred_gym_1}</p>
      <p>Preferred gym #2: ${coach.preferred_gym_2}</p>
    `;

    return card;
  }
});