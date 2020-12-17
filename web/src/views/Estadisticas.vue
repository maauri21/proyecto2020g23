<template>
    <div>
        <main class="py-4">
            <b-container>

                <b-card
                    border-variant="primary"
                    header="Tipos de Centro más utilizados"
                    header-bg-variant="primary"
                    header-text-variant="white"
                    align="center"
                >
                    <b-card-text><TiposMasUtilizados/></b-card-text>
                </b-card>

              </b-container>
        </main>
    </div>
</template>

<script>
// import VeLine from 'v-charts/lib/line.common'
import TiposMasUtilizados from '@/components/TiposMasUtilizados.vue'

export default {
    name: 'Estadisticas',
    title: 'Estadísticas',
    components: {
//      VeLine
        TiposMasUtilizados
    },
    data () {
        this.chartSettings = {
            showMA: true,
            labelMap: {
            MA5: 'ma5'
            },
        }
        

      return {
        chartData: {
          columns: ['fecha', 'costo', 'ganancia', 'ratio de crecimiento', 'personas'],
          rows: [
            { 'costo': 1523, 'fecha': '01/01', 'ganancia': 1523, 'ratio de crecimiento': 0.12, 'personas': 100 },
            { 'costo': 1223, 'fecha': '01/02', 'ganancia': 1523, 'ratio de crecimiento': 0.345, 'personas': 100 },
            { 'costo': 2123, 'fecha': '01/03', 'ganancia': 1523, 'ratio de crecimiento': 0.7, 'personas': 100 },
            { 'costo': 4123, 'fecha': '01/04', 'ganancia': 1523, 'ratio de crecimiento': 0.31, 'personas': 100 },
            { 'costo': 3123, 'fecha': '01/05', 'ganancia': 1523, 'ratio de crecimiento': 0.12, 'personas': 100 },
            { 'costo': 7123, 'fecha': '01/06', 'ganancia': 1523, 'ratio de crecimiento': 0.65, 'personas': 100 }
          ]
        },
        chartData2: {
          columns: ['date', 'cost', 'profit'],
          rows: [
            { 'date': '01/01', 'cost': 123, 'profit': 3 },
            { 'date': '01/02', 'cost': 1223, 'profit': 6 },
            { 'date': '01/03', 'cost': 2123, 'profit': 90 },
            { 'date': '01/04', 'cost': 4123, 'profit': 12 },
            { 'date': '01/05', 'cost': 3123, 'profit': 15 },
            { 'date': '01/06', 'cost': 7123, 'profit': 20 }
          ]
        }
        }
    }
    
  
    
}
</script>
