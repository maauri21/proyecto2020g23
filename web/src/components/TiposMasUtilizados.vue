<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>

    <ve-pie :data="chartData"></ve-pie>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: "TiposMasUtilizados",
  data() {
    return {
        error: false,
        chartData: []
    };
  },
  created() {
    axios.get(`https://admin-grupo23.proyecto2020.linti.unlp.edu.ar/api/v1/estadisticas/tipos_mas_utilizados`)
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