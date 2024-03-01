// /your-project-folder/frontend/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Section 1: Member Login
    const memberLoginButton = document.getElementById('member-login');
    const memberLoginFields = document.getElementById('member-login-fields');
    const signupLink = document.getElementById('signup-link');
  
    // Add click event listeners
    memberLoginButton.addEventListener('click', showMemberLoginFields);
    signupLink.addEventListener('click', redirectToSignup);
  
    // Functions for button clicks
    function showMemberLoginFields() {
      // Hide other login options
      memberLoginButton.style.display = 'none';
  
      // Show member login fields
      memberLoginFields.style.display = 'block';
    }
  
    function redirectToSignup() {
      window.location.href = 'signup.html';
    }
  });
  
  document.addEventListener('DOMContentLoaded', function () {
    // Section 2: Coach Signup
    const coachOption = document.querySelector('input[name="signup-type"][value="coach"]');
    const coachUploadSection = document.getElementById('coach-upload-section');
  
    // Add change event listener
    coachOption.addEventListener('change', toggleCoachUploadSection);
  
    // Function to toggle the coach upload section
    function toggleCoachUploadSection() {
      // Show the upload section if the user is a coach, hide otherwise
      coachUploadSection.style.display = coachOption.checked ? 'block' : 'none';
    }
  
    // Initialize the state on page load
    toggleCoachUploadSection();
  
    // Get the member option and add event listener
    const memberOption = document.querySelector('input[name="signup-type"][value="member"]');
    memberOption.addEventListener('change', toggleCoachUploadSection);
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