let map;
let marker;

const mapClickHandler = (e) => {
    addMarker(e.latlng);
};

const addMarker = ({ lat, lng }) => {
    if (marker) marker.remove();        // Si ya tengo un marcador, lo borro
    marker = L.marker([lat, lng]).addTo(map);   // Agrego el nuevo
};

// Crea el mapa
const initializeMap = (selector) => {
    // traigo las coordenadas 
    let lat = $('#lat').val();
    let lng = $('#lng').val();

    // Arranco donde está el punto
    map = L.map(selector).setView([lat, lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').
    addTo(map);

    addSearchControl(); // Plugin de busqueda
    
    // Marco el punto
    marker = L.marker([lat, lng]).addTo(map);
    map.on('click', mapClickHandler); // Manejador que recibe el evento
}

const addSearchControl = () => {
    L.control.scale().addTo(map);
    let searchControl = new L.esri.Controls.Geosearch().addTo(map);

    let results = new L.LayerGroup().addTo(map);

    searchControl.on('results', (data) => {
        results.clearLayers();

        if (data.results.length > 0) {
            addMarker(data.results[0].latlng);
        };
    });
};

const submitHandler = (event) => {
    latlng = marker.getLatLng();
    document.getElementById('lat').setAttribute('value', latlng.lat);
    document.getElementById('lng').setAttribute('value', latlng.lng);
};

// Cuando el documento html termina de cargar
window.onload = () => {
    initializeMap('mapid');
};