<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-10">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Home</div>
                            <div class="card-body">
                                <h2>Bienvenidos al Portal del Covid de la Provincia de Buenos Aires</h2>
                                <h5>Este portal fue creado con el propósito de simplificarle la informacion de los centros de ayuda disponibles en la provincia de Buenos Aires, poniendo a disposición una serie de operaciones para los visitantes que se describirán abajo.</h5>
                                <br/>
                                <button type="button" class="btn btn-primary btn-md"  @click="$router.push('centros/agregar')" data-toggle="button">Agregar Centro</button>
                                 Agregar centros de ayuda social donde se recibirán donaciones de cualquier tipo
                            </div>
                            <div class="card-body">
                                <button type="button" class="btn btn-primary btn-md"  @click="$router.push('/centros/')" data-toggle="button">Ver Centros </button>
                                 Visualizar un mapa con todos los centros activos que se encuentran en funcionamiento
                            </div>
                            
                            <div class="card-body">
                                <button type="button" class="btn btn-primary btn-md"  @click="$router.push('#')" data-toggle="button">Ver Estadisticas </button>
                                 Visualizar una serie de estadísticas
                            </div>
                            
                          </div>
                      </div>
                  </div>
              </b-container>
        </main>
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
