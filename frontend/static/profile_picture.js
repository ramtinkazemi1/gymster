document.addEventListener('DOMContentLoaded', function() {
    // Select the button and file input
    const changePictureButton = document.getElementById('change-picture-button');
    const profilePictureInput = document.getElementById('profile-picture-input');

    // Add event listener to the button
    changePictureButton.addEventListener('click', function() {
        // Trigger click event on the file input
        profilePictureInput.click();
    });

    // Add event listener to the file input
    profilePictureInput.addEventListener('change', function() {
        // Submit the form when a file is selected
        document.getElementById('profile-picture-form').submit();
    });
});