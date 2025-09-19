const User = require('../models/User'); // referencing user model
const jwt = require('jsonwebtoken'); // referencing jsonwebtoken
const bcrypt = require('bcryptjs'); // referencing bcryptjs

const generateToken = (id) => jwt.sign({id}, process.env.JWT_SECRET, {expiresIn: '7d'});

// registering a new user
exports.register = async (req, res) => {
    let {name, email, password, role} = req.body;

    // validation for any missing fields
    if (!name || !email || !password || !role) {
        return res.status(400).json({msg: "Missing fields"});
    }

    email = email.toLowerCase(); // converting email to lowercase so that there are no duplicates

    const existingUser = await User.findOne({email});
    if (existingUser) {
        return res.status(400).json({msg: "User already exists"});
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const startingBalance = role === 'beneficiary' ? 5: 0;

    const user = await User.create({
        name, email, password: hashedPassword, role, tokenBalance: startingBalance
    });

    res.json({
        token: generateToken(user._id),
        user: { id: user._id, name, email, role, tokenBalance: startingBalance}
    });
};


// logging in existing user
exports.login = async (req, res) => {
    const {email, password} = req.body;


    // finding the user by email
    const user = await User.findOne({email});
    // if theres not a user that matches the email then provide error
    if (!user) return res.status(400).json({msg: "Invalid credentials"});

    // match is comparing password from body to hashed password in the database
    const match = await bcrypt.compare(password, user.password);
    // if theres no match then the passwords incorrect and error is provided
    if (!match) return res.status(400).json({msg: "Invalid credentials"});

    // otherwise, generate a token and send back user data except password
    res.json({token: generateToken(user._id), user: {id: user._id, name: user.name, email, role: user.role}});
};

// getProfile is to get the user profile so that we can display it on the frontend
exports.getProfile = async (req, res) => {
    // finding the user by its ID
    const user = await User.findById(req.user.id).select('-password');
    res.json(user);
}