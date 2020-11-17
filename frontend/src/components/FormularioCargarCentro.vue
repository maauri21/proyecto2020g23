<template>
    <div>
        <form>
            <small>Nombre *</small>
            <b-form-input class="mb-3" type="text" maxlength="40" required v-model="nombre" :state="verificar_nombre"></b-form-input>

            <small>Dirección *</small>
            <b-form-input class="mb-3" type="text" maxlength="40" required v-model="direccion" :state="verificar_direccion"></b-form-input>

            <small>Teléfono *</small>
            <b-form-input class="mb-3" type="text" maxlength="20" required v-model="telefono" :state="verificar_telefono"></b-form-input>

            <small>Hora de apertura *</small>
            <b-form-input class="mb-3" type="time" required v-model="apertura" :state="verificar_apertura"></b-form-input>

            <small>Hora de cierre *</small>
            <b-form-input class="mb-3" type="time" required v-model="cierre" :state="verificar_cierre"></b-form-input>

            <small>Tipo *</small>
            <b-form-select class="mb-3" v-model="select" :options="frutas"></b-form-select>

            <small>Municipio *</small>
            <b-form-select class="mb-3" v-model="select_municipio">
                <option v-for="location in locations" :key="location" :value="location">{{location.name}}</option>
            </b-form-select>
            <small>Web</small>
            <b-form-input class="mb-3" type="text" maxlength="40" required v-model="web" :state="verificar_web"></b-form-input>

            <small>Email *</small>
            <b-form-input type="text" maxlength="40" required v-model="email" :state="verificar_email"></b-form-input>

            <b-btn class="mt-3" type="submit">Aceptar</b-btn>
        </form>

        <h2>{{select_municipio.name}}</h2>

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
            select_municipio: '',
            locations: [],
            frutas: [
                {value: 'Manzana', text: 'Manzana'},
                {value: 'Pera', text: 'Pera'},
                {value: 'Naranja', text: 'Naranja'}
            ],
        }
    },
    computed: {
        verificar_nombre() {
            return this.nombre.length > 2 ? true : false // + de 2 caracteres devuelve true, sino false
        },
    },
    created() {
        axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135')
            .then(response => {
            this.locations = response.data.data.Town;
            })
    }
}
</script>