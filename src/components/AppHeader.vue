<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <span class="logo_container" @click="likePost(post.id)"><i class="icons logo_style 	fa fa-camera"></i><a class="navbar-brand" href="/">Photogram</a></span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto navbr">
            <li v-if="token" class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li v-if="token" class="nav-item">
              <RouterLink class="nav-link" to="/" @click="logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";

let token = ref("");

async function setToken() {
  token.value = localStorage.getItem('user-token')
}

onMounted(() => {
  setToken()
})

function logout() {
  localStorage.removeItem('user-token')
  localStorage.removeItem('username')
  token.value = null
  window.location.reload()
}

</script>

<style>
.navbr{
  margin: 0 0 0 auto !important;
}

.logo_style{
  font-size: 20px !important ;
  margin-right: 3px;
  margin-left: 3px;
  color:white;
}

</style>