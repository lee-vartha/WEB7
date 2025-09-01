const Product = require('../models/Product'); // referencing product model

exports.addProduct = async (req, res) => {
    try {
        // if the user isnt a donor, then provide an error 
        if (req.user.role !== 'donor') return res.status(403).json({ msg: "Only donors can add products"});

        // get name, description, cost from req.body
        const { name, description, cost } = req.body;
        const product = await Product.create({name, description, cost, owner: req.user_id});

        // json response with product
        res.json(product);
    } catch (err) {
        res.status(500).json({msg: err.message});
    }
};

// get the products
exports.getProducts = async (req, res) => {
    try {
        // show owner details (name, email)
        const products = await Product.find().populate('owner', 'name email');
        // json response that returns all products
        res.json(products);
    } catch (err) {
        res.status(500).json({msg: err.message});
    }
}