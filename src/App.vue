<template>
  <header>
    <div class="menu">
      <div class="title">Descr·ai·be</div>
      <div class="menu-buttons">
        <!-- <button type="button" class="menu-button">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="4 4 24 24" width="24" class="game-icon" data-testid="icon-help">
            <path fill="var(--color-tone-1)" d="M14.8333 23H17.1666V20.6667H14.8333V23ZM15.9999 4.33334C9.55992 4.33334 4.33325 9.56001 4.33325 16C4.33325 22.44 9.55992 27.6667 15.9999 27.6667C22.4399 27.6667 27.6666 22.44 27.6666 16C27.6666 9.56001 22.4399 4.33334 15.9999 4.33334ZM15.9999 25.3333C10.8549 25.3333 6.66659 21.145 6.66659 16C6.66659 10.855 10.8549 6.66668 15.9999 6.66668C21.1449 6.66668 25.3333 10.855 25.3333 16C25.3333 21.145 21.1449 25.3333 15.9999 25.3333ZM15.9999 9.00001C13.4216 9.00001 11.3333 11.0883 11.3333 13.6667H13.6666C13.6666 12.3833 14.7166 11.3333 15.9999 11.3333C17.2833 11.3333 18.3333 12.3833 18.3333 13.6667C18.3333 16 14.8333 15.7083 14.8333 19.5H17.1666C17.1666 16.875 20.6666 16.5833 20.6666 13.6667C20.6666 11.0883 18.5783 9.00001 15.9999 9.00001Z">
            </path>
          </svg>
        </button> -->
        <button type="button" @click="renderOverlay()" class="menu-button">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="4 4 24 24" width="24" class="game-icon" data-testid="icon-statistics">
            <path fill="var(--color-tone-1)" d="M20.6666 14.8333V5.5H11.3333V12.5H4.33325V26.5H27.6666V14.8333H20.6666ZM13.6666 7.83333H18.3333V24.1667H13.6666V7.83333ZM6.66659 14.8333H11.3333V24.1667H6.66659V14.8333ZM25.3333 24.1667H20.6666V17.1667H25.3333V24.1667Z">
            </path>
          </svg>
        </button>
        <!-- <button type="button" @click="clearStorage()" class="menu-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
            <path fill="var(--color-tone-1)" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
          </svg>
        </button> -->
      </div>
    </div>
  </header>
  <main class="main">
    <div class="pic">
      <img class="art" :src="art"/>
    </div>
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
        </div>
      </div>
    </div>
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
      <div class="status-text-color" id="statusText">
        GUESSES REMAINING: {{gameData.guessesRemaining}}
      </div>
      <div class="status-text-color">
        TIME TAKEN: {{ minutesTaken }}:{{ secondsTaken }}
      </div>
    </div>
    <div class="keyboard">
      <button class="key" data-key="Q" @click="keyClick">Q</button>
      <button class="key" data-key="W" @click="keyClick">W</button>
      <button class="key" data-key="E" @click="keyClick">E</button>
      <button class="key" data-key="R" @click="keyClick">R</button>
      <button class="key" data-key="T" @click="keyClick">T</button>
      <button class="key" data-key="Y" @click="keyClick">Y</button>
      <button class="key" data-key="U" @click="keyClick">U</button>
      <button class="key" data-key="I" @click="keyClick">I</button>
      <button class="key" data-key="O" @click="keyClick">O</button>
      <button class="key" data-key="P" @click="keyClick">P</button>
      <div class="space-0asda"></div>
      <button class="key" data-key="A" @click="keyClick">A</button>
      <button class="key" data-key="S" @click="keyClick">S</button>
      <button class="key" data-key="D" @click="keyClick">D</button>
      <button class="key" data-key="F" @click="keyClick">F</button>
      <button class="key" data-key="G" @click="keyClick">G</button>
      <button class="key" data-key="H" @click="keyClick">H</button>
      <button class="key" data-key="J" @click="keyClick">J</button>
      <button class="key" data-key="K" @click="keyClick">K</button>
      <button class="key" data-key="L" @click="keyClick">L</button>
      <div class="space"></div>
      <button class="key large hidden"></button>
      <button class="key" data-key="Z" @click="keyClick">Z</button>
      <button class="key" data-key="X" @click="keyClick">X</button>
      <button class="key" data-key="C" @click="keyClick">C</button>
      <button class="key" data-key="V" @click="keyClick">V</button>
      <button class="key" data-key="B" @click="keyClick">B</button>
      <button class="key" data-key="N" @click="keyClick">N</button>
      <button class="key" data-key="M" @click="keyClick">M</button>
      <button class="key large hidden" @click="keyClick"></button>
    </div>
  </main>
</template>


<script>
import Chart from 'chart.js/auto'
import PromptData from '@/data.json'

export default {
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
      gameDateOrigin: 19344
    }
  },
  mounted() {
    this.initializeGame()
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
    min-height: 90vh;
    flex-direction: column; 
    justify-content: center; 
    align-items: center;
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
    margin-top: 1.5rem;
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
