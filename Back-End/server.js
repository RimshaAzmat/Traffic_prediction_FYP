// server.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON body
app.use(express.json());

// Define a route to handle simulation requests
app.post('/run_simulation', (req, res) => {
    // Placeholder for simulation logic
    // Process form data
    const formData = req.body;
    console.log('Received form data:', formData);

    // Execute SUMO simulation (placeholder)
    // For now, just send a success response
    res.send('Simulation request received');
});


// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something went wrong!');
});

// Define a route to handle simulation requests
app.post('/run_simulation', (req, res) => {
    try {
        // Placeholder for simulation logic
        // Process form data
        const formData = req.body;
        console.log('Received form data:', formData);

        // Execute SUMO simulation (placeholder)
        // For now, just send a success response
        res.send('Simulation request received');
    } catch (error) {
        // Handle errors and send an error response
        console.error(error);
        res.status(500).send('Internal server error');
    }
});
