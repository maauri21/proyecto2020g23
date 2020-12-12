<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>



    <div v-if="this.loading" class="loader">
      <b-modal ref="my-modal" hide-footer hide-header>
        <div class="d-block text-center">
          <h3>Cargando centros</h3><b-spinner variant="primary" label="Spinning"></b-spinner>
        </div>
      </b-modal>
    </div>
    <l-map
      :zoom.sync="zoom"
      :center="center"
      style="height: 500px; width: 100%"
    >
      <l-tile-layer
        :url="url"
      />

      <div v-for="i in total" :key="i">
        <l-marker v-for="(centro, index) in centros[i-1]" :key="index" :lat-lng="coordenadas(centro.latitud, centro.longitud)">
          <l-popup>
            <div>
              <b>Nombre:</b> {{centro.nombre}}<br/>
              <b>Dirección:</b> {{centro.direccion}}<br/>
              <b>Teléfono:</b> {{centro.telefono}}<br/>
              <b>Horario:</b> {{centro.hora_apertura.slice(0, -3)}} - {{centro.hora_cierre.slice(0, -3)}}<br/>
              <b-button class="mt-2"  size="sm" @click="$router.push({ name: 'CargarTurno', params: { id: centro.id } })" variant="primary">Solicitar turno</b-button>
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
import { mapMutations } from "vuex";

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
    ...mapMutations(['mostrarLoading', 'ocultarLoading']),

    coordenadas(lat, lng) {
      return latLng(lat, lng)
    },
    showModal() {
      this.$refs['my-modal'].show()
    },
    hideModal() {
      this.$refs['my-modal'].hide()
    }
  },
  computed: {
    ...mapState(['centros', 'loading'])
  },
  mounted() {
    this.showModal();
  },
  created() {
      this.mostrarLoading()
      axios.get('https://admin-grupo23.proyecto2020.linti.unlp.edu.ar/api/v1/centros?num_pag=1')
      .then(response => {
        this.total = response.data.total;
        for (var i = 1; i <= this.total; i++) {
          axios.get(`https://admin-grupo23.proyecto2020.linti.unlp.edu.ar/api/v1/centros?num_pag=${i}`)
          .then(response => {
            this.centros.push(response.data.centros);
            this.ocultarLoading();
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