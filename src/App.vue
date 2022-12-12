<script setup>
import AnswerSection from './components/AnswerSection.vue';
</script>

<template>
  <div class="main">
    <main>
      <h1 class="title">Descr·ai·be</h1>
      <div class="pic">
        <img class="art" src="/art.png"/>
      </div>
      <AnswerSection prompt="MAN AND HIS BEST FRIEND"/>
    </main>
  </div>
</template>

<style>
  .title {
    color: white;
    text-align: center;
  }
  .main {
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center;
  }
  .art {
    max-width: 100%;
    height: auto;
    display:block;
    margin-left:auto;
    margin-right:auto;
  }
</style>
