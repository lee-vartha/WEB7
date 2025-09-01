// refering middleware (json web tokens & user model)
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// creating 'protect', which is used to protect routes which require auth
const protect = async (req, res, next) => {
    // requesting the authorization token
    let token = req.headers.authorization;
    // if theres no token at all or theres no token that includes bearer, create error
    if (!token || !token.startsWith('Bearer ')) {
        return res.status(401).json({msg: "No token, authorization denied"});
    }
    
    
    try {
        
        const decoded = jwt.verify(token.split(' ')[1], process.env.JWT_SECRET);
        req.user = await User.findById(decoded.id).select('-password');
        next();
    } catch (err) {
        res.status(401).json({msg: "Token isnt valid"});
    }
};

module.exports = {protect}
