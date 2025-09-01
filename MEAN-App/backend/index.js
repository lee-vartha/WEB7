const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
dotenv.config();

const app = express();

// middleware
app.use(cors());
app.use(express.json());

// the reference for routes
const authRoutes = require('./routes/authRoutes');
const productRoutes = require('./routes/productRoutes');
const tokenRoutes = require('./routes/tokenRoutes');

// using the reference for api
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/tokens', tokenRoutes);

mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
    .then(() => {
        console.log('MongoDB connected');
        app.listen(process.env.PORT || 5000, () => 
        console.log(`Server running on port ${process.env.PORT || 5000}`)
    );
    })
    .catch(err => console.log(err));