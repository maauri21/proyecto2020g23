<template>
    <div>
        <form>

            <div class="form-group">
                <div>Nombre *</div>
                <input name="nombre" autocomplete="off" maxlength="40" class="form-control" v-validate="'required|min:5'" v-model="nombre" type="text" />
                <div class="invalid-feedback">
                    {{errors.first('nombre')}}
                </div>
            </div>

            <div class="form-group">
                <div>Dirección *</div>
                <input name="direccion" autocomplete="off" maxlength="40" class="form-control" v-validate="'required|min:5'" v-model="direccion" type="text" />
                <div class="invalid-feedback">
                    {{errors.first('direccion')}}
                </div>
            </div>

            <div class="form-group">
                <div>Teléfono *</div>
                <input name="telefono" autocomplete="off" maxlength="20" class="form-control" v-validate="'required|min:10'" v-model="telefono" type="text" placeholder="Formato 221-4808080" />
                <div class="invalid-feedback">
                    {{errors.first('telefono')}}
                </div>
            </div>

            <div class="form-group">
                <div>Hora de apertura *</div>
                <input name="apertura" autocomplete="off" class="form-control" v-validate="'required'" v-model="apertura" type="time" />
                <div class="invalid-feedback">
                    {{errors.first('apertura')}}
                </div>
            </div>

            <div class="form-group">
                <div>Hora de cierre *</div>
                <input name="cierre" autocomplete="off" class="form-control" v-validate="'required'" v-model="cierre" type="time" />
                <div class="invalid-feedback">
                    {{errors.first('cierre')}}
                </div>
            </div>

            <div class="form-group">
                <div>Tipo *</div>
                <select class="form-control" v-validate="'required'" v-model="select_tipo" name="tipo">
                    <option v-for="(tipo, index) in tipos" :key="index" :value="tipo">
                        {{ tipo.text }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <div>Municipio *</div>
                <select class="form-control" v-validate="'required'" v-model="select_municipio" name="municipio">
                    <option v-for="(municipio, index) in municipios" :key="index" :value="municipio">
                        {{municipio.name}}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <div>Web</div>
                <input name="web" autocomplete="off" maxlength="40" class="form-control" v-model="web" type="text" />
                <div class="invalid-feedback">
                    {{errors.first('web')}}
                </div>
            </div>

            <div class="form-group">
                <div>Email *</div>
                <input name="email" autocomplete="off" maxlength="40" class="form-control" v-validate="'required|email'" v-model="email" type="email" />
                <div class="invalid-feedback">
                    {{errors.first('email')}}
                </div>
            </div>

            <b-button variant="primary" @click="enviar_centro">Aceptar</b-button>
        </form>

        <h2>{{select_municipio.name}}</h2>
        <h2>{{nombre}}</h2>
        <h2>{{select_tipo.text}}</h2>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'FormularioCargarCentro',
    data() {
        return {
            nombre: '',
            direccion: '',
            telefono: '',
            apertura: '',
            cierre: '',
            select_tipo: '',
            select_municipio: '',
            tipos: [
                {value: 'Merendero', text: 'Merendero'},
                {value: 'Institución religiosa', text: 'Institución religiosa'}
            ],
            municipios: [],
            web: '',
            email: '',
        }
    }, methods: {
		enviar_centro() {
			this.$validator.validate() // VeeValidete tiene el validate dentro de $validator. Devuelve una promesa y al resolverse trae un booleano
				.then(esValido => {
					if (esValido) {
                        const centro = { nombre: this.nombre };
                        axios.post("http://localhost:5000/api/v1/centros", centro)
                            .then(response => this.centroid = response.data.id);
					}
				});
		}
    },
    computed: {

    },
    created() {
        axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135')
            .then(response => {
            this.municipios = response.data.data.Town;
            })
    }
}
</script>