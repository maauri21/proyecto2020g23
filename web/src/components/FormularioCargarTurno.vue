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
                <input name="dia" autocomplete="off" class="form-control" v-validate="'required'" v-model="dia" @change="traer_horarios()" type="date" />
                <div class="invalid-feedback">
                    {{errors.first('dia')}}
                </div>
           </div>
                        
            <div class="form-group">
                <div>Hora *</div>
                <select class="form-control" v-validate="'required'" v-model="select_hora" name="hora">
                    <option v-for="(hora, index) in horarios" :key="index" :value="hora.hora_inicio">
                        {{hora.hora_inicio}}
                    </option>
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
            horarios: [],
            select_hora: '',
            id_centro: this.$route.params.id,
        }
    }, methods: {
		enviar_turno() {
			this.$validator.validate() // VeeValidete tiene el validate dentro de $validator. Devuelve una promesa y al resolverse trae un booleano
				.then(esValido => {
					if (esValido) {
                        alert ('bien')
                        //const turno = { email_donante: this.email, hora_inicio: this.select_hora, fecha: this.dia };
                        //axios.post(`http://localhost:5000/api/v1/centros/${this.id_centro}/reserva`, turno)
                        //    .then(response => this.centroid = response.data.id);
					}
				});
        },
        traer_horarios() {
            axios.get(`http://localhost:5000/api/v1/centros/${this.id_centro}/turnos_disponibles/?fecha=${this.dia}`)
                .then(response => {
                this.horarios = response.data.turnos;
                })
        }
    }
}    
</script>