const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors'); // Import CORS middleware
const app = express();
const port = 3000;

// Middleware to enable CORS
app.use(cors());

// Example mongoose connection
mongoose.connect('mongodb://localhost:27017/myapp', { useNewUrlParser: true, useUnifiedTopology: true });

// Example mongoose schema and model
const userSchema = new mongoose.Schema({
  email: String,
  password: String,
});

const User = mongoose.model('User', userSchema);

// Example POST route for sign-up
app.post('/api/signup', async (req, res) => {
  try {
    // Assuming req.body contains { email, password, confirmPassword }
    const { email, password, confirmPassword } = req.body;

    // Validate password, etc. here if needed

    // Create new user
    const newUser = new User({
      email,
      password,
    });

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
