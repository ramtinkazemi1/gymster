const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/gymsterDB', { useNewUrlParser: true, useUnifiedTopology: true });

// Middleware to check user type and redirect accordingly
const redirectBasedOnUserType = (req, res, next) => {
  const userType = req.userType; // Assuming you store user type in req.userType after login

  // Redirect based on user type
  if (userType === 'coach') {
    res.redirect('/coach-dashboard');
  } else if (userType === 'customer') {
    res.redirect('/customer-dashboard');
  } else {
    // Handle other user types or unauthorized access
    res.status(403).json({ error: 'Unauthorized access' });
  }
};

// Protected route
app.use('/protectedRoute', redirectBasedOnUserType);

// Create a user schema
const userSchema = new mongoose.Schema({
  firstName: String,
  lastName: String,
  phoneNumber: { type: String, unique: true },
  email: String,
  password: String, // Hashed password
  userType: String,
  // Other fields as needed
});

// Create a model based on the schema
const User = mongoose.model('User', userSchema);

// Handle user registration
app.post('/register', async (req, res) => {
  try {
    // Extract data from the request
    const { firstName, lastName, phoneNumber, email, password, userType } = req.body;

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create a new user
    const newUser = new User({
      firstName,
      lastName,
      phoneNumber,
      email,
      password: hashedPassword,
      userType,
    });

    // Save the user to the database
    await newUser.save();

    // Send a success response
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
