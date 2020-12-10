import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    centros: [],
    loading: false,
  },
  mutations: {
    mostrarLoading(state) {
      state.loading = true
    },
    ocultarLoading(state) {
      state.loading = false
    }
  },
  actions: {
  },
  modules: {
  }
})
