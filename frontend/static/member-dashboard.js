const radiusInput = document.getElementById('radius');
const radiusOutput = document.getElementById('radius-value');

// Add an event listener to the range input element
radiusInput.addEventListener('input', function() {
    // Update the content of the output element with the current value of the range input
    radiusOutput.textContent = this.value;
});

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');

    // Add event listener to the search button
    const searchButton = document.getElementById('search-button');
    searchButton.addEventListener('click', function(event) {
        event.preventDefault();
        searchCoaches();
    });

    function searchCoaches() {
        // Retrieve the user's zipcode and selected radius from the form
        const zipcode = document.getElementById('zipcode').value;
        const radius = document.getElementById('radius').value;

        // Check if zipcode and radius are not empty
        if (zipcode && radius) {
            // Make AJAX request to the server to search for coaches
            fetch('/search_coaches', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ zipcode: zipcode, radius: radius })
            })
            .then(response => response.json())
            .then(data => {
              // Clear previous search results
              searchResults.innerHTML = '';
          
              // Display search results
              data.coaches.forEach(coach => {
                  const distance = coach.distance; // Assuming the server sends the distance along with coach data
                  const coachCard = createCoachCard(coach, distance);
                  searchResults.appendChild(coachCard);
              });
          })
            .catch(error => {
                console.error('Error searching for coaches:', error);
            });
        } else {
            console.error('Error: Zipcode or radius is null or empty');
        }
    }
});

function createCoachCard(coach, distance) {
  // Create a div element for the coach card
  const card = document.createElement('div');
  card.classList.add('coach-card');

  // Create a div element for the coach information
  const infoDiv = document.createElement('div');
  infoDiv.classList.add('info');

  // Create an image element for the profile picture
  const img = document.createElement('img');
  img.src = coach.profile_picture;
  img.alt = 'Profile Picture';

  // Create a div element for the phone, zipcode, and book button
  const phoneZipcodeBookDiv = document.createElement('div');
  phoneZipcodeBookDiv.classList.add('phone-zipcode-book');

  // Create a heading element for the coach's name
  const nameHeading = document.createElement('h3');
  nameHeading.textContent = `${coach.first_name} ${coach.last_name}`;

  // Create a paragraph element for the coach's phone number
  const phoneParagraph = document.createElement('p');
  phoneParagraph.textContent = `Phone: ${coach.phone_number}`;

  // Create a paragraph element for the coach's zipcode
  const zipcodeParagraph = document.createElement('p');
  zipcodeParagraph.textContent = `Zipcode: ${coach.zipcode}`;

  // Create a button element for booking
  const bookButton = document.createElement('button');
  bookButton.textContent = 'Book';
  bookButton.classList.add('book-button');

  // Append the phone, zipcode, and book button to phoneZipcodeBookDiv
  phoneZipcodeBookDiv.appendChild(phoneParagraph);
  phoneZipcodeBookDiv.appendChild(zipcodeParagraph);
  phoneZipcodeBookDiv.appendChild(bookButton);

  // Append phoneZipcodeBookDiv to infoDiv
  infoDiv.appendChild(nameHeading);
  infoDiv.appendChild(phoneZipcodeBookDiv);

  // Create a paragraph element for the coach's distance from user
  const distanceParagraph = document.createElement('p');
  distanceParagraph.textContent = `${distance} miles away`;
  distanceParagraph.classList.add('distance');

  // Append the image, infoDiv, and distanceParagraph to the card
  card.appendChild(img);
  card.appendChild(infoDiv);
  card.appendChild(distanceParagraph);

  return card;
}
