import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Estadisticas from '../views/Estadisticas.vue'
import CargarCentro from '../views/CargarCentro.vue'
import MapaCentros from '../views/MapaCentros.vue'
import CargarTurno from '../views/CargarTurno.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: Estadisticas
  },
  {
    path: '/centros/agregar',
    name: 'CargarCentro',
    component: CargarCentro
  },
  {
    path: '/centros/',
    name: 'MapaCentros',
    component: MapaCentros
  },
  {
    path: '/centros/:id/reserva',
    name: 'CargarTurno',
    component: CargarTurno
  }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
