<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>

    <div v-if="this.loading" class="loader">
      <b-alert variant="success" show>Cargando</b-alert>
    </div>

    <ve-histogram :data="chartData" :settings="chartSettings"></ve-histogram>
  </div>
</template>

<script>

import axios from 'axios';
import { mapState } from "vuex";
import { mapMutations } from "vuex";

export default {
  name: "MunicipiosMasConcurridos",
  data() {
    this.chartSettings = {
      metrics: ['cantidad']
    }
    return {
        error: false,
        chartData: [],
    };
  },
  methods: {
    ...mapMutations(['mostrarLoading', 'ocultarLoading']),
  },
  computed: {
    ...mapState(['loading'])
  },
  created() {
    this.mostrarLoading()
    axios.get(`https://admin-grupo23.proyecto2020.linti.unlp.edu.ar/api/v1/estadisticas/municipios_mas_concurridos`)
        .then(response => {
        this.chartData = response.data;
        this.ocultarLoading();
    })
    .catch(error => {
        console.log(error)
        this.error = true
    })
  }
};
</script>