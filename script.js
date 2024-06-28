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

    const origin = document.getElementById('origin').value.toUpperCase();
    const destination = document.getElementById('destination').value.toUpperCase();
    const mes = document.getElementById('mes').value;
    const dia = document.getElementById('dia').value;
    const horaSalida = document.getElementById('hora_salida').value;
    const horaLlegada = document.getElementById('hora_llegada').value;

    try {
        // Objeto con los datos a enviar
        const datos = {
            origen: origin,
            destino: destination,
            mes: parseInt(mes),
            dia: parseInt(dia),
            hora_salida: parseInt(horaSalida),
            hora_llegada: parseInt(horaLlegada)
        };

        // URL del servidor FastAPI
        const url = 'http://127.0.0.1:8000/prediccion';  // Asegúrate de que esta URL sea correcta

        // Enviar datos al servidor usando fetch
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) {
            throw new Error('Error al enviar los datos');
        }

        // Procesar la respuesta del servidor
        const resultado = await response.json();
        console.log('Respuesta del servidor:', resultado);

        // Aquí puedes añadir código para mostrar el resultado en tu aplicación si lo deseas
        alert('Predicción realizada con éxito. Revisa la consola para ver los resultados.');

    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al enviar los datos al servidor.');
    }
}

