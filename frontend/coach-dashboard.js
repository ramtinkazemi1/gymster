document.addEventListener('DOMContentLoaded', function () {
  const availabilitySelection = document.getElementById('availability-selection');
  const saveAvailabilityButton = document.getElementById('save-availability-button');
  const availabilityDisplay = document.getElementById('availability-display');

  if (saveAvailabilityButton) {
    saveAvailabilityButton.addEventListener('click', saveAvailability);
  } else {
    console.error('Save Availability button not found.');
  }

  initializeAvailabilityInputs();

  function initializeAvailabilityInputs() {
    const currentWeekDays = getCurrentWeekDays();
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    currentWeekDays.forEach((date, index) => {
      const dayContainer = document.createElement('div');
      dayContainer.classList.add('availability-day-container');

      const label = document.createElement('label');
      label.textContent = `${daysOfWeek[index]} ${date.toLocaleString('en-us', { month: 'short' })} ${date.getDate()}: `;
      dayContainer.appendChild(label);

      const dropdown = document.createElement('select');
      dropdown.classList.add('availability-dropdown'); // Added class for selection
      dropdown.id = `availability-dropdown-${daysOfWeek[index].toLowerCase()}`;
      ['Not Available', 'Available'].forEach((option) => {
        const optionElement = document.createElement('option');
        optionElement.value = option.toLowerCase();
        optionElement.textContent = option;
        dropdown.appendChild(optionElement);
      });
      dayContainer.appendChild(dropdown);

      const timeInputsContainer = document.createElement('div');
      timeInputsContainer.classList.add('time-inputs-container');

      const startTimeInputContainer = document.createElement('div');
      startTimeInputContainer.classList.add('time-input-container');

      const startTimeLabel = document.createElement('label');
      startTimeLabel.textContent = 'Start Time:';
      startTimeInputContainer.appendChild(startTimeLabel);

      const startTimeInput = document.createElement('input');
      startTimeInput.type = 'time';
      startTimeInput.classList.add('start-time-input');
      startTimeInput.step = 900; // Set step to 15 minutes (900 seconds)
      startTimeInputContainer.appendChild(startTimeInput);

      timeInputsContainer.appendChild(startTimeInputContainer);

      const endTimeInputContainer = document.createElement('div');
      endTimeInputContainer.classList.add('time-input-container');

      const endTimeLabel = document.createElement('label');
      endTimeLabel.textContent = 'End Time:';
      endTimeInputContainer.appendChild(endTimeLabel);

      const endTimeInput = document.createElement('input');
      endTimeInput.type = 'time';
      endTimeInput.classList.add('end-time-input');
      endTimeInput.step = 900; // Set step to 15 minutes (900 seconds)
      endTimeInputContainer.appendChild(endTimeInput);

      timeInputsContainer.appendChild(endTimeInputContainer);

      const errorContainer = document.createElement('div');
      errorContainer.classList.add('error-container');
      errorContainer.textContent = 'End time should be after start time';
      errorContainer.style.color = 'red';
      errorContainer.style.display = 'none';
      timeInputsContainer.appendChild(errorContainer);

      dayContainer.appendChild(timeInputsContainer);
      availabilitySelection.appendChild(dayContainer);

      timeInputsContainer.style.display = 'none';

      dropdown.addEventListener('change', function () {
        timeInputsContainer.style.display = this.value === 'available' ? 'block' : 'none';
        errorContainer.style.display = 'none';
      });
    });
  }

  function getCurrentWeekDays() {
    const today = new Date();
    const currentDay = today.getDay();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - currentDay);

    const days = [];
    for (let i = 0; i <= 6; i++) {
      const currentDate = new Date(startOfWeek);
      currentDate.setDate(startOfWeek.getDate() + i);
      days.push(currentDate);
    }

    return days.filter(date => date >= today);
  }

  function saveAvailability() {
    const availabilityStatus = {};
    const availabilityTimes = {};
    let isValid = true;

    document.querySelectorAll('.availability-day-container').forEach((dayContainer) => {
      const dayDropdown = dayContainer.querySelector('.availability-dropdown');
      const startTimeInput = dayContainer.querySelector('.start-time-input');
      const endTimeInput = dayContainer.querySelector('.end-time-input');
      const errorContainer = dayContainer.querySelector('.error-container');

      if (dayDropdown && startTimeInput && endTimeInput) {
        const day = dayDropdown.id.replace('availability-dropdown-', '');
        const status = dayDropdown.value;
        availabilityStatus[day] = status;

        const startTime = status === 'available' ? startTimeInput.value : '';
        const endTime = status === 'available' ? endTimeInput.value : '';
        availabilityTimes[day] = { startTime, endTime };

        if (status === 'available' && endTime < startTime) {
          isValid = false;
          errorContainer.style.display = 'block';
        } else {
          errorContainer.style.display = 'none';
        }
      }
    });

    if (isValid) {
      displayAvailabilityTimes(availabilityTimes);

      document.querySelectorAll('.time-inputs-container').forEach((container) => {
        container.style.display = 'none';
      });
    }
  }

  function displayAvailabilityTimes(times) {
    availabilityDisplay.innerHTML = '';

    const displayBox = document.createElement('div');
    displayBox.classList.add('availability-display-box');
    for (const day in times) {
      const timeInfo = times[day];
      if (timeInfo.startTime && timeInfo.endTime) {
        const dayInfo = document.createElement('div');
        dayInfo.textContent = `${day}: ${timeInfo.startTime} - ${timeInfo.endTime}`;
        displayBox.appendChild(dayInfo);
      }
    }

    availabilityDisplay.appendChild(displayBox);
  }
});
