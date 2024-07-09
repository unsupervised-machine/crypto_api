const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const cors = require('cors'); // Import CORS middleware
const app = express();
const port = 3000;

const bodyParser = require('body-parser');
app.use(bodyParser.json()); // Parse JSON bodies

// Middleware to enable CORS
app.use(cors());

// Example mongoose connection
mongoose.connect('mongodb://localhost:27017/crypto_api_db', { useNewUrlParser: true, useUnifiedTopology: true });

// Example mongoose schema and model
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  const user = this;
  if (!user.isModified('password')) return next();

  try {
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(user.password, salt);
    user.password = hashedPassword;
    next();
  } catch (error) {
    return next(error);
  }
});


const User = mongoose.model('User', userSchema, 'users');

// Example POST route for sign-up
app.post('/api/signup', async (req, res) => {
  console.log('Request Body:', req.body); // Log the request body

  try {
    // Assuming req.body contains { signupEmail, signupPassword, signupConfirmPassword }
    const { signupEmail, signupPassword, signupConfirmPassword } = req.body;

    // Validate that email and password are present
    if (!signupEmail || !signupPassword || !signupConfirmPassword) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    // Validate that passwords match
    if (signupPassword !== signupConfirmPassword) {
      return res.status(400).json({ error: 'Passwords do not match' });
    }

    const existingUser = await User.findOne({ email: signupEmail });
    if (existingUser) {
      return res.status(400).json({ error: 'Email already exists' });
    }

    // Create new user
    const newUser = new User({
      email: signupEmail,
      password: signupPassword
    });


    // Print the user object to console before saving
    console.log('New User Object:', newUser);
    // Save user to MongoDB
    await newUser.save();

    // Send success response
    res.status(201).json({ message: 'User signed up successfully' });
  } catch (error) {
    // Handle error
    console.error('Error signing up:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
