<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-30">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Home</div>
                            <div class="card-body">
                                <h2>Bienvenidos al portal del covid de la Provincia de Buenos Aires</h2>
                                <h5>Este portal fue creado con el proposito de simplificarle la informacion de los centros de ayuda disponibles en la provincia de Buenos Aires, poniendo a disposicion una serie de operaciones para los visitantes que se describiran abajo.
 
                                 </h5><hr>
                                <h6> <button type="button" class="btn btn-primary btn-md"  @click="$router.push('centros/agregar')" data-toggle="button" aria-pressed="false" autocomplete="off">Agregar Centro</button>
                                 Mediante esta opcion los visitantes podran agregar centros de ayuda social donde se recibiran donaciones de cualquier tipo</h6>
                            </div><hr>
                            <div class="card-body">
                                <h6> <button type="button" class="btn btn-primary btn-md"  @click="$router.push('#')" data-toggle="button" aria-pressed="false" autocomplete="off">Ver Centros </button>
                                 Mediante esta opcion los visitantes podran visualizar un mapa con todos los centros activos que se encuentran en funcionamiento</h6>
                            </div><hr>
                            
                            <div class="card-body">
                                <h6> <button type="button" class="btn btn-primary btn-md"  @click="$router.push('#')" data-toggle="button" aria-pressed="false" autocomplete="off">Ver Estadisticas </button>
                                 Mediante esta opcion los visitantes podran visualizar una serie de estadisticas </h6>
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
  components: {
  }
}
</script>
