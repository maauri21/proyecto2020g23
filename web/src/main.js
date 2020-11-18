import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { BootstrapVue } from 'bootstrap-vue'
import es from 'vee-validate/dist/locale/es'
import VeeValidate, { Validator } from "vee-validate";

Vue.use(VueAxios, axios)
Vue.use(VeeValidate, {
  classes: true, // Usar clases de bootstrap is-valid y is-invalid en el formulario
	classNames: {
		valid: "is-valid",
		invalid: "is-invalid",
	},
});
Validator.localize("es", es);

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
