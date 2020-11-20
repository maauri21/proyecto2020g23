<template>
  <div id="app">

    <b-navbar toggleable="md" class="navbar navbar-expand-md navbar-light bg-white shadow-sm">
      <b-container>
        
        <b-navbar-brand :to="{name: 'Home'}">Portal COVID</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse is-nav id="nav-collapse">
          <b-navbar-nav class="navbar-nav ml-auto">
            <b-nav-item :to="{name: 'Home'}" active-class="active" exact>Home</b-nav-item>
            <b-nav-item :to="{name: 'MapaCentros'}" active-class="active" exact>Mapa Centros</b-nav-item>
            <b-nav-item :to="{name: 'CargarTurno'}" active-class="active" exact>Solicitar Turno</b-nav-item>
            <b-nav-item :to="{name: 'CargarCentro'}" active-class="active" exact>Cargar Centro</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
    
    <router-view/>

    <footer id="sticky-footer" class="py-2 bg-primary text-white">
      <div class="container text-center">
        <small>Copyright &copy; 2020</small>
      </div>
    </footer>

  </div>
</template>