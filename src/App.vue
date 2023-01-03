<template>
  <page-header/>
  <main class="main">
    <div class="status">
        <div class="status-box status-text-color" id="statusText">
          GUESSES: {{gameData.guessesRemaining}}
        </div>
        <div class="status-box status-text-color">
          TIME: {{ minutesTaken }}:{{ secondsTaken }}
        </div>
      </div>
    <div class="pic">
      <img class="art" :src="art"/>
    </div>
    <!-- End screen dimmer? -->
    <answer-section/>
    <game-keyboard/>
  </main>
</template>


<script>
import Chart from 'chart.js/auto'
import PromptData from '@/data.json'
import PageHeader from '@/components/PageHeader.vue'
import AnswerSection from '@/components/AnswerSection.vue'
import GameKeyboard from '@/components/GameKeyboard.vue'

export default {
  components: {
    PageHeader,
    AnswerSection,
    GameKeyboard
  },
  computed: {
    promptSpaces(){
      const promptWordsLengths = [];
      let nextWordLength = 0;
      for (const char of this.prompt){
        if (char == " "){
          promptWordsLengths.push(nextWordLength)
          nextWordLength = 0
        } else {
          nextWordLength += 1
        }
      }
      promptWordsLengths.push(nextWordLength)
      return promptWordsLengths
    },
    prompt() {
      let promptIndex = this.getToday() - this.gameDateOrigin
      return this.promptMap[promptIndex].prompt.toUpperCase()
    },
    art() {
      let promptIndex = this.getToday() - this.gameDateOrigin
      return "/" + this.promptMap[promptIndex].image
    }
  },
  data() {
    return {
      promptMap: PromptData,
      startingGuesses: 3,
      timer: undefined,
      minutesTaken: "--",
      secondsTaken: "--",
      guessClassMap: {
        3: "status-three",
        2: "status-two",
        1: "status-one",
        0: "status-one"
      },
      gameData: {
        active: true,
        history: [],
        startTime: undefined,
        guessesRemaining: 3,
        guesses: [],
        currentStreak: 0,
        maxStreak: 0
      },
      showOverlay: false,
      gameDateOrigin: 19344,
      timeToNextGame: "--:--:--"
    }
  },
  mounted() {
    this.initializeGame()
    this.trackTimeToNextGame()
    document.addEventListener("keydown", this.keypress)
  },
  methods: {
    keyClick(event){
      let keyClicked = event.target.dataset.key.toUpperCase()
      this.registerKeyPress(keyClicked)
    },
    keypress(event) {
      let keyClicked = event.key
      if (keyClicked.match(/^[a-z]$/)){
        this.registerKeyPress(keyClicked.toUpperCase())
      }
    },
    registerKeyPress(char){
      // Game is already over
      if (!this.gameData.active) return

      
      // Already guessed this letter
      const keyboardKey = document.querySelector(`.key[data-key="${char}"]`)
      if (keyboardKey.dataset.checked == "true"){
        return
      }

      this.gameData.guesses.push(char)

      this.checkGuess(char)

      if (this.checkGameOver()){
        this.endGame()
      }
    },
    checkGuess(char){
      const keyboardKey = document.querySelector(`.key[data-key="${char}"]`)
      // Disable this key
      keyboardKey.dataset.checked = "true"

      if (this.prompt.includes(char)) {
        keyboardKey.classList.add("correct")
        this.revealLetters(char)
      } else {
        keyboardKey.classList.add("wrong")
        this.subtractGuess()
        this.removePreviousStatusColorClass()
        this.addCurrentStatusColorClass()
      }

      this.saveGameData()
    },
    revealLetters(char) {
      const promptNoSpace = this.prompt.replaceAll(" ", "")
      for (let i = 0; i < promptNoSpace.length; i++) {
        if (char === promptNoSpace[i]) {
          let revealChar = document.querySelectorAll("div.letter")[i]
          revealChar.dataset.valueset = "true"
          revealChar.textContent = char
        }
      }
    },
    subtractGuess(){
      this.gameData.guessesRemaining = this.gameData.guessesRemaining - 1
    },
    removePreviousStatusColorClass() {
      const elements = document.querySelectorAll(".status-background-color, .status-text-color")
      elements.forEach(element => {
        element.classList.remove(this.guessClassMap[this.gameData.guessesRemaining + 1])
      })
    },
    addCurrentStatusColorClass() {
      const elements = document.querySelectorAll(".status-background-color, .status-text-color")
      elements.forEach(element => {
        element.classList.add(this.guessClassMap[this.gameData.guessesRemaining])
      })
    },
    checkGameWon() {
      let nextRemainingSpace = document.querySelector('.letter:not([data-valueset="true"])')
      return (nextRemainingSpace === null)
    },
    checkGameLost() {
      if (this.gameData.guessesRemaining === 0) return true
    },
    checkGameOver() { 
      if (this.checkGameLost()) return true
      if (this.checkGameWon()) return true
    },
    endGame() {
      let gameWon = this.checkGameWon()
      this.gameData.active = false
      this.gameData.timeTaken = Number(this.secondsTaken) + (Number(this.minutesTaken) * 60)
      this.stopTimer()

      // Add game to game history
      this.gameData.history.push({
        gameWon: gameWon,
        timeTaken: this.gameData.timeTaken,
        date: this.getToday()
      })

      // Update streaks
      if (gameWon) {
        this.gameData.currentStreak += 1
        if (this.gameData.maxStreak < this.gameData.currentStreak) {
          this.gameData.maxStreak = this.gameData.currentStreak
        } else {
          this.gameData.currentStreak = 0
        }
      }

      this.renderOverlay()
      this.saveGameData()
    },
    initializeGame() {
      const gameData = JSON.parse(localStorage.getItem("descraibe-game-data"))
      if (gameData){
        if (gameData.currentStreak !== undefined) this.gameData.currentStreak = gameData.currentStreak
        if (gameData.maxStreak !== undefined) this.gameData.maxStreak = gameData.maxStreak
        if (gameData.history){
          this.gameData.history = gameData.history
          let todayGame = gameData.history.find(obj => obj.date === this.getToday())
          if (todayGame) {
            if (gameData.active !== undefined) this.gameData.active = gameData.active
            if (gameData.startTime !== undefined) this.gameData.startTime = gameData.startTime
            if (gameData.timeTaken !== undefined) this.gameData.timeTaken = gameData.timeTaken

            if (gameData.guesses !== undefined) {
              this.gameData.guesses = gameData.guesses
              gameData.guesses.forEach(char => {
                this.checkGuess(char)
              })
          }
        } 
        }
      }
      
      if (this.gameData.active) {
        this.startTimer()
      } else {
        this.secondsTaken = Math.floor(this.gameData.timeTaken % 60).toString().padStart(2, "0")
        this.minutesTaken = Math.floor(this.gameData.timeTaken / 60).toString().padStart(2, "0")
        this.renderOverlay()
      }
    },
    startTimer() {
      if (!this.gameData.startTime) this.gameData.startTime = Date.now()
      let msTaken = Date.now() - this.gameData.startTime
      this.secondsTaken = Math.floor((msTaken / 1000) % 60).toString().padStart(2, "0")
      this.minutesTaken = Math.floor((msTaken / 1000) / 60).toString().padStart(2, "0")
      this.saveGameData()
      this.timer = setInterval(() => {
        const msTaken = Date.now() - this.gameData.startTime
        this.secondsTaken = Math.floor((msTaken / 1000) % 60).toString().padStart(2, "0")
        this.minutesTaken = Math.floor((msTaken / 1000) / 60).toString().padStart(2, "0")
      }, 1000)
    },
    stopTimer() {
      clearInterval(this.timer)
    },
    saveGameData() {
      localStorage.setItem("descraibe-game-data", JSON.stringify(this.gameData))
    },
    closeOverlay(event) {
      if (event.target === document.querySelector(".end-screen-dimmer")) this.showOverlay = false
    },
    renderOverlay(){
      this.showOverlay = true
    },
    renderChart(){
      const chrt = document.getElementById('timeDistChart')
      if (this.gameData.history.length >= 0){
        new Chart(chrt, {
          type: 'line',
          data: {
            datasets: [{
              data: [1, 2, 3, 10, 100, 1000]
            }]
          },
          options: {
            scales: {
              timeTaken: {
                type: 'logarithmic',
                position: 'left'
              }
            }
          }
        })
      }
    },
    getGamesPlayed() {
      return this.gameData.history.length
    },
    getWinPercentage() {
      const gamesWon = this.gameData.history.filter(obj => obj.gameWon === true).length
      const gamesPlayed = this.getGamesPlayed()
      if (gamesPlayed === 0) return 0
      return Math.floor((gamesWon / gamesPlayed) * 100)
    },
    getAvgTime() {
      let sum = 0
      this.gameData.history.forEach(game => {
        sum += game.timeTaken
      })
      if (this.gameData.history.length > 0) {
        return Math.round(sum / this.gameData.history.length)
      }
      return 0
    },
    getStreak() {
      return this.gameData.currentStreak
    },
    getMaxStreak() {
      return this.gameData.maxStreak
    },
    clearStorage(){
      localStorage.removeItem("descraibe-game-data")
    },
    getToday(){
      return Math.floor(Date.now() / 1000 / 60 / 60 / 24)
    },
    trackTimeToNextGame() {
      let msToMidnight = this.msTillNextUtcDay()
      let hour = Math.floor(msToMidnight / 1000 / 60 / 60).toString().padStart(2, "0")
      let minute = Math.floor(msToMidnight / 1000 / 60 % 60).toString().padStart(2, "0")
      let second = Math.floor(msToMidnight / 1000 % 60).toString().padStart(2, "0")
      this.timeToNextGame = `${hour}:${minute}:${second}`
      setInterval(() => {
        msToMidnight = this.msTillNextUtcDay()
        hour = Math.floor(msToMidnight / 1000 / 60 / 60).toString().padStart(2, "0")
        minute = Math.floor(msToMidnight / 1000 / 60 % 60).toString().padStart(2, "0")
        second = Math.floor(msToMidnight / 1000 % 60).toString().padStart(2, "0")
      this.timeToNextGame = `${hour}:${minute}:${second}`
      }, 1000)
    },
    msTillNextUtcDay() {
      const msInDay = 86400000; // 24 * 60 * 60 * 1000
      const date = Date.now() // time since midnight on January 1, 1970, UTC (ecmascript epoch)
      const msNextDay = Math.ceil(date/msInDay) * msInDay; //gets the time of in ms of the start of the next utc day in ecmascript epoch "format"
      return msNextDay - date; //Subtracts current time from start of next day
    }
  }
}
</script>


<style>
  .title {
    color: var(--color-tone-1);
    text-align: center;
    font-size: 1.25em;
    margin-bottom: .25em;
    font-weight: bold;
    flex-grow: 2;
  }
  .main {
    display: flex; 
    min-height: 75vh;
    flex-direction: column; 
    justify-content: center; 
    align-items: center;
  }
  .pic {
    flex-grow: 1;
  }
  .art {
    max-width: 80%;
    height: auto;
    display:block;
    margin-left:auto;
    margin-right:auto;
  }
  .menu {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    flex-wrap: nowrap;
    border-bottom: 1px solid var(--color-tone-1);
    margin-bottom: 2em;
    
  }
  .menu-buttons {
    display: flex;
    justify-content: flex-end;
  }
  .menu-button {
    background: none;
    border: none;
    cursor: pointer;
  }
  .end-screen-dimmer {
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
    left: 0;
    top: 0;
    overflow: auto;
    background-color: hsl(1, 0%, 10%, 80%);
    width: 100%;
    height: 100%;
  }
  .end-modal {
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 80%;
    margin: auto;
    border: 1px solid var(--color-tone-1);
    background-color: var(--background-color);
    color: var(--color-tone-1);
    border-radius: .25em;
  }
  .modal-container {
    margin-left: 2em;
    margin-right: 2em;
    margin: 0em 2em 2em 2em;
  }
  .modal-title {
    text-align: center;
    margin-bottom: 2em;
    margin-top: 2.25em;
  }
  .modal-close {
    cursor: pointer;
    margin-left: auto;
    margin-right: .5em;
    font-size: 2em;
  }
  .general-stats {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }
  .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 1.5em;
    margin: 0em .3em 1em .3em;
  }
  .stat-label {
    display: flex;
    text-align: center;
    font-size: .4em;
    max-width: 80%;
  }
  .status {
    display: flex;
    flex-direction: row;
    margin-bottom: 1em;
  }
  .status-box {
    padding: 0em 1em 0em 1em;
    border: 1px solid var(--color-tone-1);
  }
  .status-text-color {
    color: hsl(var(--statusHue, 110), 33%, 50%);
    font-size: 1.5em;
  }
  .status-background-color {
    background-color: hsl(var(--statusHue, 110), 33%, 50%);
  }
  .status-two {
    --statusHue: 66
  }
  .status-one {
    --statusHue: 0
  }
  .answer-section {
    display: flex;
    flex-direction: column;
    justify-content: center; 
    align-items: center;
    margin-bottom: 1.5rem;
    gap: 1.5rem;
    justify-content: center; 
    align-items: center;
    flex-grow: 1;
  }
  .prompt {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: .9em;
  }
  .word {
    display: inherit;
  }
  .letter-holder {
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
  }
  .letter {
    width: auto;
    height:1em;
    font-size: 2em;
    font-weight: bold;
    color: var(--color-tone-1);
    text-align: center;
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
  }
  .bar {
    width: 1em;
    height: 3px;
    margin: .2em;
  }
  .space {
    width: .5em;

  }
  *, *::after, *::before {
  box-sizing: border-box;
}
.keyboard {
  display: grid;
  grid-template-columns: repeat(20, minmax(auto, 2em));
  grid-auto-rows: 3em;
  gap: .3em;
  justify-content: center;
}
.key {
  font-size: inherit;
  grid-column: span 2;
  border: none;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: hsl(
    var(--hue, 200), 
    var(--saturation, 1%), 
    calc(var(--lightness-offset, 0%) + var(--lightness, 51%))
  );
  color: white;
  fill: white;
  text-transform: uppercase;
  border-radius: .25em;
  cursor: pointer;
  user-select: none;
}
.key.large {
  grid-column: span 3;
}
.hidden {
  visibility: hidden;
}
.key > svg {
  width: 1.75em;
  height: 1.75em;
}
.key:hover, .key:focus {
  --lightness-offset: 10%;
}
.key.wrong {
  --lightness: 23%;
}
.key.correct {
 --hue: 115;
 --saturation: 29%;
 --lightness: 43%;
}
</style>
