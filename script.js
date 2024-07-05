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
        const url = 'http://127.0.0.1:8001/prediccion';  // Asegúrate de que esta URL sea correcta

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

        // Mostrar los resultados de la predicción en la interfaz
        const resultadoDiv = document.getElementById('resultado');
        resultadoDiv.innerHTML = `
            <h2>Resultado de la Predicción</h2>
            <p>Probabilidad de ser 1: ${resultado[0]['Probabilidad de ser 1']}</p>
        `;
        const distanceDiv = document.getElementById('distance');
        distanceDiv.innerHTML = `
            <h2>Distancia de la Predicción</h2>
            <p>Distancia en millas: ${resultado[0]['Distancia']}</p>
        `;

        // Obtener coordenadas del CSV o JSON para origen y destino
        const originCoords = await getAirportCoordinates(origin);
        const destinationCoords = await getAirportCoordinates(destination);

        // Dibujar la ruta en el mapa
        const route = L.polyline([originCoords, destinationCoords], {
            color: 'blue',
            dashArray: '10, 10', // Estilo de línea discontinua
            weight: 3
        }).addTo(map);

        map.fitBounds([originCoords, destinationCoords]); // Ajustar el mapa para mostrar la ruta completa

    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al enviar los datos al servidor.');
    }
}

