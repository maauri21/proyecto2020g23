<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Cargar centro</div>
                            <div class="card-body">
                                <FormularioCargarCentro/>
                            </div>
                          </div>
                      </div>
                  </div>
              </b-container>
        </main>
    </div>
</template>

<script>
import FormularioCargarCentro from '@/components/FormularioCargarCentro.vue'

export default {
  name: 'CargarCentro',
  components: {
    FormularioCargarCentro
  }
}
</script>