document.addEventListener('DOMContentLoaded', function() {
    const signInButton = document.getElementById('signin');
    
    signInButton.addEventListener('click', function() {
        console.log('Sign-in button clicked'); // Add this line
        // Your existing sign-in logic here
    });
});

  document.addEventListener('DOMContentLoaded', function() {
    var signinBtn = document.getElementById('signin-btn');
    var signinBox = document.getElementById('signin-box');

    signinBtn.addEventListener('click', function() {
        // Calculate the position of the sign-in button
        var btnRect = signinBtn.getBoundingClientRect();

        // Set the position of the sign-in box below the button with some space
        signinBox.style.top = btnRect.bottom + 10 + 'px';
        signinBox.style.left = btnRect.left + 'px';

        // Toggle the display of the sign-in box
        if (signinBox.style.display === 'block') {
            signinBox.style.display = 'none';
        } else {
            signinBox.style.display = 'block';
        }
    });
});



// the inner sign in button *****************************************************************************************
document.addEventListener('DOMContentLoaded', function () {
    const signInButton = document.getElementById('signin');

    signInButton.addEventListener('click', function () {
        // Retrieve user input (phone number and password)
        const phoneNumber = document.getElementById('phone-number').value;
        const password = document.getElementById('password').value;

        console.log('Phone number:', phoneNumber); // Print the phone number value
        console.log('Password:', password); // Print the password value

        // Send a POST request to the Flask backend
        fetch('/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ phone_number: phoneNumber, password: password })
        })
        .then(response => {
            console.log('Response:', response); // Print the response object

            if (response.ok) {
                // Redirect based on user type
                window.location.href = response.url;  // Redirect to the URL specified in the response
            } else {
                throw new Error('Failed to sign in');
            }
        })
        .catch(error => {
            console.error('Sign-in failed:', error);
            // Handle sign-in failure (e.g., display error message)
            console.log('Sign-in failed'); // Print a message indicating sign-in failure
        });
    });
});







const carousel = document.getElementById('testimonial-carousel');
const slides = document.querySelectorAll('.testimonial-slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let slideIndex = 0;

function showSlides() {
  slides.forEach((slide) => {
    slide.style.display = 'none';
  });

  if (slideIndex >= slides.length) {
    slideIndex = 0;
  }

  if (slideIndex < 0) {
    slideIndex = slides.length - 1;
  }

  slides[slideIndex].style.display = 'block';
}

function nextSlide() {
  slideIndex++;
  showSlides();
}

function prevSlide() {
  slideIndex--;
  showSlides();
}

prevBtn.addEventListener('click', () => {
  prevSlide();
});

nextBtn.addEventListener('click', () => {
  nextSlide();
});

showSlides();