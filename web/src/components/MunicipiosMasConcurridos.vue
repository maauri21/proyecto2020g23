<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>

    <ve-histogram :data="chartData" :settings="chartSettings"></ve-histogram>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: "MunicipiosMasConcurridos",
  data() {
    this.chartSettings = {
      metrics: ['cantidad']
    }
    return {
        error: false,
        chartData: '',
    };
  },
  created() {
    axios.get(`http://localhost:5000/api/v1/estadisticas/municipios_mas_concurridos`)
        .then(response => {
        this.chartData = response.data;
    })
    .catch(error => {
        console.log(error)
        this.error = true
    })
  }
};
</script>