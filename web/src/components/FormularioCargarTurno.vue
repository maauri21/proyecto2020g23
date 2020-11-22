<template>
     <form>

            <div class="form-group">
                <div>Email *</div>
                <input name="email" autocomplete="off" maxlength="40" class="form-control" v-validate="'required|email'" v-model="email" type="email" />
                <div class="invalid-feedback">
                    {{errors.first('email')}}
                </div>
            </div>

            <div class="form-group">
                <div>Dia *</div>
                <input name="dia" autocomplete="off" class="form-control" v-validate="'required'" v-model="hora" type="date" />
                <div class="invalid-feedback">
                    {{errors.first('dia')}}
                </div>
           </div>
                        
             <div class="form-group">
                <div>Hora *</div>
                <select class="form-control" v-validate="'required'" v-model="select_municipio" name="hora">
                    
                </select>
            </div>  

           <b-button variant="primary" @click="enviar_turno">Aceptar</b-button>

        </form>    
</template>

<script>
import axios from 'axios';

export default {
    name: 'FormularioCargarTurno',
    data() {
        return {
            email: '',
            dia: '',
            hora: '',
            
        }
    }, methods: {
		enviar_turno() {
			this.$validator.validate() // VeeValidete tiene el validate dentro de $validator. Devuelve una promesa y al resolverse trae un booleano
				.then(esValido => {
					if (esValido) {
                        const turno = { email: this.email, dia: this.dia, hora: this.hora };
                        axios.post("http://localhost:5000//api/v1/centros/${centro_id}/turnos_disponibles?fecha=${fecha}", turno)
                            .then(response => this.centroid = response.data.id);
					}
				});
		}
    },
    computed: {

    }
}    
</script>    