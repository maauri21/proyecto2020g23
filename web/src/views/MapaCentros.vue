<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Mapa Centros</div>
                            <div class="card-body">
                                <Mapa/>
                            </div>
                          </div>
                      </div>
                  </div>
              </b-container>
        </main>
    </div>
</template>

<script>
import Mapa from '@/components/Mapa.vue'

export default {
  name: 'MapaCentros',
  components: {
    Mapa
  }
}
</script>