// referencing express
const express = require('express');
// importing functions from user controller and auth middleware
const {register, login, getProfile} = require('../controllers/userController');
// importing protect from auth middleware to protect certain routes
const {protect} = require('../middleware/authMiddleware');

// getting the router (express.js)
const router = express.Router();

// auth routes for registering, logging in and gettingn user profile
router.post('/register', register);
router.post('/login', login);
router.get('/me', protect, getProfile);

// exporting the module so other files can use it
module.exports = router;