import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Axios
import axios from 'axios'
import VueAxios from 'vue-axios'

// Bootstrap
import { BootstrapVue } from 'bootstrap-vue'

// VeeValidate
import es from 'vee-validate/dist/locale/es'
import VeeValidate, { Validator } from "vee-validate";

// Leaflet
import 'leaflet/dist/leaflet.css';

// Axios
Vue.use(VueAxios, axios)

// VeeValidate
Vue.use(VeeValidate, {
  classes: true, // Usar clases de bootstrap is-valid y is-invalid en el formulario
	classNames: {
		valid: "is-valid",
		invalid: "is-invalid",
	},
});
Validator.localize("es", es);

// Bootstrap
Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
