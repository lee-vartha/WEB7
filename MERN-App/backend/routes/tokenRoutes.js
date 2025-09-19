// referencing express.js for routing
const express = require('express');
// importing functions from token controller and auth middleware
const {earnTokens, spendTokens} = require('../controllers/tokenController');
// importing protect from auth middleware to protect certain routes
const {protect} = require('../middleware/authMiddleware');

// getting the router (express.js)
const router = express.Router();

// getting the routes for earning and spending tokens, both protected by auth middleware
router.post('/earn', protect, earnTokens);
router.post('/spend', protect, spendTokens);

// exporting router to be used in other files
module.exports = router;