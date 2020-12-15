<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Estadísticas</div>
                            <div class="card-body">
                                <h2 class="text-center">TP</h2>
                                <ve-pie :data="chartData" :settings="chartSettings"></ve-pie>
                            </div>
                          </div>
                      </div>
                  </div>
              </b-container>
        </main>
    </div>
</template>

<script>
// import VeLine from 'v-charts/lib/line.common'

export default {
    name: 'Estadisticas',
    title: 'Estadísticas',
    components: {
//      VeLine
    },
    data() {
        this.chartSettings = {
            dataType: 'percent'
        }
        return {
            chartData: {
                columns: ['date', 'profit'],
                rows: [
                    { 'date': 'mb', 'cost': 123, 'profit': 0.099 },
                    { 'date': 'lmuertinez', 'cost': 1223, 'profit': 0.001 },
                ]
            }
        }
    },
}
</script>
