<template>
  <div class="container-fluid auth-screen">
    <div class="row justify-content-center align-items-center vh-100">
      <div class="center-box p-4 col-sm-3 shadow-lg">
        <router-view />
      </div>
    </div>
  </div>
</template>
<style scoped>
.auth-screen {
  background: #a7a9ab3b;
}

.center-box {
  background: #fff !important;
  max-width: 460px;
}

input {
  background: inherit;
}
</style>
