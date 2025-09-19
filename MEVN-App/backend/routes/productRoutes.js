// referencing express
const express = require('express');
const {addProduct, getProducts} = require('../controllers/productController');
// referencing the protect middleware to secure the routes
const {protect} = require('../middleware/authMiddleware');

// getting the router (express.js)
const router = express.Router();

// post route for adding a product, get route for getting all products
router.post('/', protect, addProduct);
router.get('/', getProducts);

// exporting the router
module.exports = router;