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
    <div class="status-text-color" id="statusText">
      Guesses Remaining: {{guesses_remaining}}
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
</template>

<script>
import { vModelCheckbox } from 'vue';

// TODO: Stats
export default {
  props: {
    prompt: String
  },
  computed: {
    promptSpaces(){
      const promptWordsLengths = [];
      let nextWordLength = "";
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
    }
  },
  data() {
    return {
      guesses_remaining: 6,
      guessClassMap: {
        5: "status-five",
        4: "status-four",
        3: "status-three",
        2: "status-two",
        1: "status-one"
      },
      game_active: true
    }
  },
  mounted() {
    document.addEventListener("keydown", this.keypress)
  },
  methods: {
    keyClick(event){
      let keyClicked = event.target.dataset.key.toUpperCase()
      this.checkGuess(keyClicked)
    },
    keypress(event) {
      let keyClicked = event.key
      if (keyClicked.match(/^[a-z]$/)){
        this.checkGuess(keyClicked.toUpperCase())
      }
    },
    checkGuess(char){
      if (!this.game_active) return
      const keyboardKey = document.querySelector(`.key[data-key="${char}"]`)
      if (keyboardKey.dataset.checked == "true"){
        return
      }
      keyboardKey.dataset.checked = "true"
      let nextRemainingSpace = document.querySelector('.letter:not([data-valueset="true"])')
      if (!nextRemainingSpace) {
          this.game_active = false;
          return
        }

      if (this.prompt.includes(char)) {
        keyboardKey.classList.add("correct")
        this.revealLetters(char);
      } else {
        keyboardKey.classList.add("wrong")
        this.subtractGuess()
      }
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
      const statusText = document.getElementById("statusText")
      if (this.guesses_remaining > 1) {
        const chars = document.getElementsByClassName("bar")
        statusText.classList.remove(this.guessClassMap[this.guesses_remaining])
        this.guesses_remaining = this.guesses_remaining - 1
        statusText.classList.add(this.guessClassMap[this.guesses_remaining])
        for (const char of chars){
          char.classList.remove(this.guessClassMap[this.guesses_remaining - 1])
          char.classList.add(this.guessClassMap[this.guesses_remaining])
        }
      } else {
        statusText.textContent = "Game over!"
        this.game_active = false
      }
    }
  }
}
</script>

<style>
  .status-text-color {
    color: hsl(var(--statusHue, 110), 50%, 50%);
    font-size: 1.5em;
  }
  .status-background-color {
    background-color: hsl(var(--statusHue, 110), 50%, 50%);
  }
  .status-five {
    --statusHue: 88;
  }
  .status-four {
    --statusHue: 66;
  }
  .status-three {
    --statusHue: 44
  }
  .status-two {
    --statusHue: 22
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
    gap: .1em;
  }
  .word {
    display: inherit;
  }
  .letter-holder {
    height: 2.25em;
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
  }
  .letter {
    width: auto;
    height:1.8em;
    font-size: 1.5em;
    font-weight: bold;
    color: white;
    text-align: center;
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
  }
  .bar {
    width: 1.25em;
    height: .1em;
    margin: .1em;
  }
  .space {
    width: .5em;

  }
  *, *::after, *::before {
  box-sizing: border-box;
}
.keyboard {
  display: grid;
  grid-template-columns: repeat(20, minmax(auto, 1.25em));
  grid-auto-rows: 3em;
  gap: .25em;
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
