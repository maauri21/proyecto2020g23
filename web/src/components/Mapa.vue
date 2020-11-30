<template>

  <div>
    <l-map
      :zoom.sync="zoom"
      :center="center"
      style="height: 500px; width: 100%"
    >
      <l-tile-layer
        :url="url"
      />

      <l-marker v-for="(centro, index) in centros" :key="index" :lat-lng="coordenadas(centro.latitud, centro.longitud)">
        <l-popup>
          <div>
            <b>Nombre:</b> {{centro.nombre}}<br/>
            <b>Dirección:</b> {{centro.direccion}}<br/>
            <b>Teléfono:</b> {{centro.telefono}}<br/>
            <b>Horario:</b> {{centro.hora_apertura.slice(0, -3)}} - {{centro.hora_cierre.slice(0, -3)}}<br/>
            <b-button class="mt-2"  size="sm" @click="$router.push({ name: 'CargarTurno', params: { id: centro.id } })" variant="primary " >Solicitar turno</b-button>
          </div>
        </l-popup>
      </l-marker>

    </l-map>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";

// Para que se vean los iconos
import { Icon } from 'leaflet';

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

import axios from 'axios';

export default {
  name: "Mapa",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data() {
    return {
      centros: [],
      zoom: 13,
      center: latLng(-34.9187, -57.956),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      ll: latLng(-34.9323859290129, -57.940950393676765),
      currentZoom: 11.5,
      currentCenter: latLng(-34.9187, -57.956),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      },
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    coordenadas(lat, lng) {
      return latLng(lat, lng)
    }
  },
  created() {
      axios.get('http://localhost:5000/api/v1/centros/?num_pag=1')
          .then(response => {
          this.centros = response.data.centros;
          })
  }
};
</script>