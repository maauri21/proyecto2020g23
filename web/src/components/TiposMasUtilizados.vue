<template>

  <div>

    <section v-if="error">
      <p>No es posible obtener la información en este momento, intente nuevamente más tarde</p>
    </section>

    {{tiposmasutilizados[0]}}
    <ve-pie :data="chartData"></ve-pie>

    {{this.tiposmasutilizados[0].tipo}}

  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: "TiposMasUtilizados",
  data() {
    return {
        tiposmasutilizados: [],
        error: false,
        chartData: {
          columns: ['tipo', 'cant'],
          rows: [
            { 'tipo': this.tiposmasutilizados[0].tipo, 'cant': 123 },
            { 'tipo': 'Instu', 'cant': 1223 },
          ]
        }
    };
  },
  created() {
    axios.get(`http://localhost:5000/api/v1/estadisticas/tipos_mas_utilizados`)
        .then(response => {
        this.tiposmasutilizados = response.data.tiposmasutilizados;
    })
    .catch(error => {
        console.log(error)
        this.error = true
    })
  }
};
</script>