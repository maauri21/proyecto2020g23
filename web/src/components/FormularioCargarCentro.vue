<template>
    <div>
        <form>
            <small>Nombre *</small>
            <b-form-input class="mb-3" type="text" maxlength="40" required v-model="nombre"></b-form-input>

            <small>Dirección *</small>
            <b-form-input class="mb-3" type="text" maxlength="40" required v-model="direccion"></b-form-input>

            <small>Teléfono *</small>
            <b-form-input class="mb-3" type="text" maxlength="20" required v-model="telefono"></b-form-input>

            <small>Hora de apertura *</small>
            <b-form-input class="mb-3" type="time" required v-model="apertura"></b-form-input>

            <small>Hora de cierre *</small>
            <b-form-input class="mb-3" type="time" required v-model="cierre"></b-form-input>

            <small>Tipo *</small>
            <b-form-select class="mb-3" required v-model="select" :options="tipos"></b-form-select>

            <small>Municipio *</small>
            <b-form-select class="mb-3" required v-model="select_municipio">
                <option v-for="municipio in municipios" :key="municipio" :value="municipio">{{municipio.name}}</option>
            </b-form-select>
            <small>Web</small>
            <b-form-input class="mb-3" type="text" maxlength="40" v-model="web"></b-form-input>

            <small>Email *</small>
            <b-form-input type="email" maxlength="40" required v-model="email"></b-form-input>

            <b-btn class="mt-3" type="submit">Aceptar</b-btn>
        </form>

        <h2>{{select_municipio.name}}</h2>
        <h2>{{nombre}}</h2>

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
            select_municipio: '',
            tipos: [
                {value: 'Merendero', text: 'Merendero'},
                {value: 'Institución religiosa', text: 'Institución religiosa'}
            ],
            municipios: [],
            web: '',
            email: '',
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