<template>
    <div>
        <main class="py-4">
            <b-container>
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card border-primary">
                            <div class="card-header text-white bg-primary">Cargar Turno</div>
                            <div class="card-body">
                                <FormularioCargarTurno/>
                            </div>
                          </div>
                      </div>
                  </div>
              </b-container>
        </main>
    </div>
</template>

<script>
import FormularioCargarTurno from '@/components/FormularioCargarTurno.vue'

export default {
  name: 'CargarTurno',
  title: 'Cargar Turno',
  components: {
    FormularioCargarTurno
  }
}
</script>