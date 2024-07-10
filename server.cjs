const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const cors = require('cors'); // Import CORS middleware
const app = express();
const port = 3000;
// const port = 5173;
const jwt = require('jsonwebtoken')

const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser'); // Import cookie-parser


app.use(bodyParser.json());
app.use(cors({
  origin: 'http://localhost:5173', // Adjust this to match your frontend's URL
  credentials: true // Allow credentials (cookies) to be sent
}));
app.use(cookieParser()); // Use cookie-parser middleware

// Example mongoose connection
mongoose.connect('mongodb://localhost:27017/crypto_api_db');

// Example mongoose schema and model
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
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
  // console.log('Request Body:', req.body); // Log the request body

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
      password: signupPassword,
      created_at: new Date(),
      updated_at: new Date()
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

// POST route for sign-in
app.post('/api/signin', async (req, res) => {
  try {
    const { email, password } = req.body;
    // console.log("Login credentials:", email, password);

    // Find user by email
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Compare hashed passwords
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

     // Generate JWT for user session
    // console.log('User object:', user); // Log the user object to inspect its content
    const token = jwt.sign({password: user.password, email: user.email }, 'replace_this_key', {expiresIn: '1h'});
    // console.log('Generated token:', token); // Log the generated token

    res.cookie('token', token, {
      httpOnly: true,
      // secure: false, // Set to true in production
      // sameSite: 'lax'
    });

    console.log('Set-Cookie Header:', res.getHeaders()['set-cookie']); // Log Set-Cookie header

    // Passwords match - User authenticated
    res.status(200).json({ message: 'User signed in successfully' });

  } catch (error) {
    console.error('Error signing in:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
