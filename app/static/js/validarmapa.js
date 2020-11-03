let map;
let marker;

// Crea el mapa
const initializeMap = (selector) => {

    // traigo las coordenadas 
    var js = $('script[src*=validarmapa]');
    var lat = js.attr('lat');   
    var lng = js.attr('lng');  

    // Arranco donde está el punto
    map = L.map(selector).setView([lat, lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').
    addTo(map);
    
    // Marco el punto
    marker = L.marker([lat, lng]).addTo(map);
}

// Cuando el documento html termina de cargar
window.onload = () => {
    initializeMap('mapid');
};