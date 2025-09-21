// referencing express for routing
const express = require('express');
// getting the router (express.js)
const router = express.Router();

// referencing user controller and auth middleware
const User = require('../models/User');
const {protect} = require('../middleware/authMiddleware');

// me route to get the profile of the logged-in user
router.get('/me', protect, async (req, res) => {
    try {
        // retrieves a user doc from the database by searching for the users ID. the findById method is an async call provided by Mongoose
        // await is used to pause this execution until the database returns this result
        // we exclude the password from the user object - prevents the users hashed password from being sent to the client
        const user = await User.findById(req.user._id).select('-password');
        if (!user) return res.status(404).json({msg: "User not found"});
        res.json(user);
    } catch (err) {
        res.status(500).json({msg: err.message});
    }
});

// posting a new user
router.post('/', async (req, res) => {
    const newUser = new User(req.body);
    const savedUser = await newUser.save();
    res.json(savedUser);
});

// exporting the module (router object) so other files can use it
module.exports = router;