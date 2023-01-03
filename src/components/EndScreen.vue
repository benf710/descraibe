<template>
  <div class="end-screen-dimmer" @click="closeOverlay" v-if="showOverlay">
    <div class="end-modal">
      <div @click="showOverlay = false" class="modal-close">&times;</div>
      <div class="modal-container">
        <div class="modal-title">
          STATISTICS
        </div>
        <div class="general-stats">
          <div class="stat">
            {{ getGamesPlayed() }}
            <div class="stat-label">
              Played
            </div>
          </div>
          <div class="stat">
            {{ getWinPercentage() }}
            <div class="stat-label">
              Win %
            </div>
          </div>
          <div class="stat">
            {{ getAvgTime() }}
            <div class="stat-label">
              Avg Time
            </div>
          </div>
          <div class="stat">
            {{ getStreak() }}
            <div class="stat-label">
              Current Streak
            </div>
          </div>
          <div class="stat">
            {{ getMaxStreak() }}
            <div class="stat-label">
              Max Streak
            </div>
          </div>
        </div>
        <div class="modal-title">
          TIME DISTRIBUTION
        </div>
        <div class="modal-title">
          COMING SOON!
        </div>
        <div class="time-dist">
          <!-- <canvas id="timeDistChart"></canvas> -->
        </div>
        <div class="modal-title">
          Next Descr·ai·be in {{ timeToNextGame }}
        </div>
      </div>
    </div>
  </div>
</template>


<script>

export default {

}
</script>


<style scoped>

</style>