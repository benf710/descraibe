<template>
  <div class="answer-section">
  <div class="prompt">
    <div class="word" v-for="wordLength of promptSpaces">
      <div class="letter-holder"  v-for="index in wordLength" :key="index">
        <div class="letter"></div>
        <div class="bar status-background-color"></div>
      </div>
      <div class="space"></div>
    </div>
  </div>
</div>
</template>


<script>

</script>


<style scoped>

</style>