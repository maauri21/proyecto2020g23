<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>

    <l-map
      :zoom.sync="zoom"
      :center="center"
      style="height: 500px; width: 100%"
    >
      <l-tile-layer
        :url="url"
      />

      <div v-for="i in this.total" :key="i">
        <l-marker v-for="(centro, index) in centros[i]" :key="index" :lat-lng="coordenadas(centro.latitud, centro.longitud)">
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
      </div>

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
import { mapState } from "vuex";

export default {
  name: "MapaCentrosCargados",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data() {
    return {
      total: '',
      error: false,
      zoom: 13,
      center: latLng(-34.9187, -57.956),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      ll: latLng(-34.9323859290129, -57.940950393676765),
    };
  },
  methods: {
    coordenadas(lat, lng) {
      return latLng(lat, lng)
    }
  },
  computed: {
    ...mapState(['centros'])
  },
  created() {
      axios.get('http://localhost:5000/api/v1/centros?num_pag=1')
      .then(response => {
        this.total = response.data.total;
        for (var i = 1; i <= this.total; i++) {
          axios.get(`http://localhost:5000/api/v1/centros?num_pag=${i}`)
          .then(response => {
            this.centros.push(response.data.centros);
          })
          .catch(error => {
            console.log(error)
            this.error = true
          })
        }
      })
      .catch(error => {
        console.log(error)
        this.error = true
      })
  }
};
</script>