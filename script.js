const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let airports = {};

// Cargar los datos de los aeropuertos desde el archivo JSON
fetch('iata-icao.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(airport => {
            airports[airport.iata] = [parseFloat(airport.latitude), parseFloat(airport.longitude)];
        });
    })
    .catch(error => console.error('Error al cargar los datos de los aeropuertos:', error));

function getAirportCoordinates(iataCode) {
    return new Promise((resolve, reject) => {
        const coordinates = airports[iataCode];
        if (coordinates) {
            resolve(coordinates);
        } else {
            reject(`No se encontraron datos para el código IATA: ${iataCode}`);
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
    // Eliminar rutas anteriores
    removePreviousRoutes();

    const originCode = document.getElementById('origin').value.toUpperCase();
    const destinationCode = document.getElementById('destination').value.toUpperCase();

    try {
        const origin = await getAirportCoordinates(originCode);
        const destination = await getAirportCoordinates(destinationCode);

        // Calcular puntos intermedios
        const points = [
            origin,
            [(origin[0] + destination[0]) / 2, (origin[1] + destination[1]) / 2], // Punto intermedio
            destination
        ];

        // Dibujar la ruta con una polilínea y personalizar el estilo
        const route = L.polyline(points, {
            color: 'blue',
            weight: 3
        }).addTo(map);

        map.fitBounds([origin, destination]); // Ajustar el mapa para mostrar la ruta completa
    } catch (error) {
        alert(error);
    }
}

