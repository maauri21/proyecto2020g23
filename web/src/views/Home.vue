<template>
    <div>
        <b-container>
        <main class="py-4">
                <div class="row justify-content-center">
                    <div class="col-md-12">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Bienvenidos al Portal del Covid de la Provincia de Buenos Aires</div>
                            <div class="card-body">
                                <h2></h2>
                                <h5>Este portal fue creado con el propósito de brindar la informacion de los centros de ayuda disponibles en la provincia de Buenos Aires, poniendo a disposición una serie de operaciones para los visitantes que se describirán a continuacion.</h5>
                            </div>
                          </div>
                      </div>
                  </div>
        </main>

        <b-row class="mb-3">

            <b-col cols="12" md="4">
                <b-card
                    img-src="cargar.jpg"
                    img-top
                    class="mb-2"
                    border-variant="primary"
                >
                    <b-card-text>
                    Cargar centros de ayuda social donde se recibirán donaciones
                    </b-card-text>

                    <b-button @click="$router.push('centros/agregar')" variant="primary">Cargar centro</b-button>
                </b-card>
            </b-col>

            <b-col cols="12" md="4">
                <b-card
                    img-src="mapa.jpg"
                    img-top
                    class="mb-2"
                    border-variant="primary"
                >
                    <b-card-text>
                    Visualizar un mapa con todos los centros que se encuentran activos
                    </b-card-text>

                    <b-button  @click="$router.push('/centros')" variant="primary">Ver centros</b-button>
                </b-card>
            </b-col>

            <b-col cols="12" md="4">
                <b-card
                    img-src="estadisticas.jpg"
                    img-top
                    class="mb-2"
                    border-variant="primary"
                >
                    <b-card-text>
                    Visualizar una serie de estadísticas relacionadas con los centros
                    </b-card-text>

                    <b-button @click="$router.push('/estadisticas')" variant="primary">Ver estadísticas</b-button>
                </b-card>
            </b-col>

            
        </b-row>
        </b-container>


    </div>
</template>

<script>

export default {
  name: 'Home',
  title: 'Home',
  components: {
  }
}
</script>
