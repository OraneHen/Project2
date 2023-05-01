<script setup>
import { ref } from "vue";
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";


let token = ref("");

</script>

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <AppHeader />

  <main>
    <RouterView />
  </main>
  
</template>

<style>
body {
  padding-top: 75px;
}
</style>