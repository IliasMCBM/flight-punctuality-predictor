const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let airports = {};

// Load airport data from JSON file
fetch('iata-icao.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(airport => {
            airports[airport.iata] = [parseFloat(airport.latitude), parseFloat(airport.longitude)];
        });
    })
    .catch(error => console.error('Error loading airport data:', error));

function getAirportCoordinates(iataCode) {
    return new Promise((resolve, reject) => {
        const coordinates = airports[iataCode];
        if (coordinates) {
            resolve(coordinates);
        } else {
            reject(`No data found for IATA code: ${iataCode}`);
        }
    });
}

function removePreviousRoutes() {
    map.eachLayer(layer => {
        if (layer instanceof L.Polyline) {
            map.removeLayer(layer);
        }
    });
}

async function drawRoute() {
    // Remove previous routes
    removePreviousRoutes();

    const origin = document.getElementById('origin').value.toUpperCase();
    const destination = document.getElementById('destination').value.toUpperCase();
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const departureTime = document.getElementById('departure_time').value;
    const arrivalTime = document.getElementById('arrival_time').value;
    // Validate IATA codes
        const isValid = true;
        const iataPattern = /^[A-Za-z]{3}$/;
        if (!iataPattern.test(origin)) {
            alert('Origin must be a three-letter IATA code.');
            isValid = false;
        }
        if (!iataPattern.test(destination)) {
            alert('Destination must be a three-letter IATA code.');
            isValid = false;
        }

        // Validate month
        if (isNaN(month) || month < 1 || month > 12) {
            alert('Month must be a number between 1 and 12.');
            isValid = false;
        }

        // Validate day of the week (1-7, where 1 is Monday)
        if (isNaN(day) || day < 1 || day > 7) {
            alert('Day must be a number between 1 and 7, where 1 is Monday.');
            isValid = false;
        }

        // Validate time in HHMM format
        const timePattern = /^([01]\d|2[0-3])[0-5]\d$/;
        if (!timePattern.test(departureTime)) {
            alert('Departure time must be in HHMM format.');
            isValid = false;
        }
        if (!timePattern.test(arrivalTime)) {
            alert('Arrival time must be in HHMM format.');
            isValid = false;
        }

        if (!isValid) {
                return;  // Stop the function if any validation fails
        }
    try {
        // Object with the data to send
        const data = {
            origin: origin,
            destination: destination,
            month: parseInt(month),
            day: parseInt(day),
            departure_time: parseInt(departureTime),
            arrival_time: parseInt(arrivalTime)
        };

        // FastAPI server URL
        const url = 'http://localhost:8000/prediction';  // Make sure this URL is correct

        // Send data to the server using fetch
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Error sending data');
        }

        // Process the server's response
        const result = await response.json();
        console.log('Server response:', result);

        // Display the prediction results in the interface
        const resultDiv = document.getElementById('result');
        const probability = (result[0]['Probability of being 1'] * 100).toFixed(2);
        resultDiv.innerHTML = `
            <h2>Prediction Result</h2>
            <p>Probability of delay greater than 15 minutes: ${probability}%</p>
        `;
        const distanceDiv = document.getElementById('distance');
        distanceDiv.innerHTML = `
            <h2>Prediction Distance</h2>
            <p>Distance in miles: ${result[0]['Distance']}</p>
        `;

        // Get coordinates from CSV or JSON for origin and destination
        const originCoords = await getAirportCoordinates(origin);
        const destinationCoords = await getAirportCoordinates(destination);

        // Draw the route on the map
        const route = L.polyline([originCoords, destinationCoords], {
            color: 'blue',
            dashArray: '10, 10', // Dashed line style
            weight: 3
        }).addTo(map);

        map.fitBounds([originCoords, destinationCoords]); // Adjust the map to show the full route

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while sending data to the server.');
    }
}
