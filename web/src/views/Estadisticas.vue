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

                <b-card
                    border-variant="primary"
                    header="Municipios más concurridos"
                    header-bg-variant="primary"
                    header-text-variant="white"
                    align="center"
                    class="mt-4"
                >
                    <b-card-text><MunicipiosMasConcurridos/></b-card-text>
                </b-card>

                <b-card
                    border-variant="primary"
                    header="Porcentaje de municipios en cada fase"
                    header-bg-variant="primary"
                    header-text-variant="white"
                    align="center"
                    class="mt-4"
                >
                    <b-card-text><MunicipiosPorFase/></b-card-text>
                </b-card>

              </b-container>
        </main>
    </div>
</template>

<script>
import TiposMasUtilizados from '@/components/TiposMasUtilizados.vue'
import MunicipiosMasConcurridos from '@/components/MunicipiosMasConcurridos.vue'
import MunicipiosPorFase from '@/components/MunicipiosPorFase.vue'

export default {
    name: 'Estadisticas',
    title: 'Estadísticas',
    components: {
        TiposMasUtilizados,
        MunicipiosMasConcurridos,
        MunicipiosPorFase
    },
    data () {

      return {

        }
    }
    
  
    
}
</script>
