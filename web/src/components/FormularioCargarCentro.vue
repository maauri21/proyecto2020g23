<template>
    <div>

        <l-map @click="addMarker"
        :zoom.sync="zoom"
        :center="center"
        style="height: 300px; width: 100%"
        >
        <l-tile-layer
            :url="url"
        />

        <l-marker :lat-lng="coordenadas(latitud, longitud)">
            <l-popup>
            <div>
                <b-button class="mt-2" size="sm" variant="primary">Solicitar turno</b-button>
            </div>
            </l-popup>
        </l-marker>

        </l-map>
        <br/>
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
                <input name="apertura" autocomplete="off" class="form-control" v-validate="'required|apertura9'" v-model="apertura" type="time" />
                <div class="invalid-feedback">
                    {{errors.first('apertura')}}
                </div>
            </div>

            <div class="form-group">
                <div>Hora de cierre *</div>
                <input name="cierre" autocomplete="off" class="form-control" v-validate="'required|cierre16'" v-model="cierre" type="time" />
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
        <h2>{{latitud}}</h2>
        <h2>{{longitud}}</h2>
        <h2>{{select_tipo.text}}</h2>

    </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import axios from 'axios';

export default {
    name: 'FormularioCargarCentro',
    components: {
        LMap,
        LTileLayer,
        LMarker,
        LPopup
    },
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
            // Mapa
            zoom: 13,
            center: latLng(-34.9187, -57.956),
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            currentZoom: 11.5,
            currentCenter: latLng(-34.9187, -57.956),
            showParagraph: false,
            mapOptions: {
                zoomSnap: 0.5
            },
            latitud: '',
            longitud: '',

        }
    }, methods: {
		enviar_centro() {
            if (this.latitud == '') {
                alert("Debes seleccionar una ubicación en el mapa")
            }
			this.$validator.validate() // VeeValidete tiene el validate dentro de $validator. Devuelve una promesa y al resolverse trae un booleano
				.then(esValido => {
					if (esValido) {
                        alert("bien")
                    //    const centro = { nombre: this.nombre };
                    //    axios.post("http://localhost:5000/api/v1/centros", centro)
                    //        .then(response => this.centroid = response.data.id);
					}
				});
        },
        coordenadas(lat, lng) {
            return latLng(lat, lng)
        },
        addMarker(event) {
            this.latitud = event.latlng.lat,
            this.longitud = event.latlng.lng
        },
    },
    computed: {

    },
    created() {
        axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135')
            .then(response => {
            this.municipios = response.data.data.Town;
            })

        // Validador personalizado para las horas
        let self = this
        this.$validator.extend('apertura9', {
        getMessage() {
            return 'El horario de apertura debe ser menor a las 09:00'
        },
        validate() {
            return self.apertura <= '09:00'
        }
        })

        this.$validator.extend('cierre16', {
        getMessage() {
            return 'El horario de cierre debe ser mayor a las 16:00'
        },
        validate() {
            return self.cierre >= '16:00'
        }
        })

    }
}
</script>