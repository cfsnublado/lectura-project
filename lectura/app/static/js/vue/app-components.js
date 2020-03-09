const AjaxDelete = {
  mixins: [AjaxProcessMixin],
  props: {
    deleteConfirmId: {
      type: String,
      default: 'confirmation-modal'
    },
    deleteUrl: {
      type: String,
      default: '',
    },
    deleteRedirectUrl: {
      type: String,
      default: ''
    },
    initTimerDelay: {
      type: Number,
      default: 500
    },
    initData: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      timerId: null,
      timerDelay: this.initTimerDelay,
      data: this.initData
    }
  },
  methods: {
    confirmDelete() {
      this.$modal.showConfirmation(this.deleteConfirmId)
      .then(yes => {
        console.log(yes)
        this.onDelete()
      })
      .catch(no => {
        console.log(no)
      })
    },
    onDelete(event) {
      this.success()
      this.process()
      clearTimeout(this.timerId)
      this.timerId = setTimeout(()=>{
        axios.delete(this.deleteUrl, {data:this.data})
        .then(response => {
          if (this.deleteRedirectUrl) {
            window.location.replace(this.deleteRedirectUrl)
          }
          this.success()
        })
        .catch(error => {
          if (error.response) {
            console.log(error.response)
          } else if (error.request) {
            console.log(error.request)
          } else {
            console.log(error.message)
          }
          console.log(error.config)
        })
        .finally(() => this.complete())
      }, this.timerDelay)
    }
  }
}

const AlertMessage = {
  mixins: [BaseMessage],
  template: `
    <transition name="fade-transition-slow" v-on:after-enter="isOpen = true" v-on:after-leave="isOpen = false">

    <div v-show="isOpen" :class="[messageType, 'alert abs-alert']">

    <div class="alert-content">
    {{ messageText }}
    </div>

    <a href=""
    type="button" 
    class="close"
    @click.prevent="close"
    >
    <span aria-hidden="true">&times;</span>
    </a>

    </div>

    </transition>
  `

}

const Dropdown = {
  mixins: [BaseDropdown],
  template: `
    <div 
    v-bind:id="id" 
    class="dropdown" 
    v-bind:class="[{ 'is-active': isOpen }, dropdownClasses]"
    >

    <div class="dropdown-trigger">
    <a 
    class="button" 
    href="#" 
    @click.prevent="toggle"
    >
    <slot name="dropdown-label">
    Dropdown
    </slot>
    </a>
    </div>

    <div class="dropdown-menu">
    <div class="dropdown-content">

    <slot name="dropdown-content">
    <div class="dropdown-item">
    Dropdown content
    </div>
    </slot>

    </div>
    </div>

    </div>
  `  
}

const NavbarDropdown = {
  mixins: [Dropdown],
  template: `
    <div 
    v-bind:id="id" 
    class="navbar-item has-dropdown" 
    v-bind:class="[{ 'is-active': isOpen }, dropdownClasses]"
    >

    <a class="navbar-link" @click.prevent="toggle">

    <slot name="dropdown-label">
    Dropdown
    </slot>

    </a>

    <div class="navbar-dropdown is-right">

    <slot name="dropdown-content">
      Put something here, ideally a list of menu items.
    </slot>

    </div>   

    </div>
  `  
}

const FileUploader = {
  mixins: [BaseFileUploader]
}

const AudioFileUploader = {
  mixins: [BaseFileUploader],
  methods: {
    validateFile() {
      validated = false

      if (this.file.type == 'audio/mpeg') {
        validated = true
      } else {
        console.error('Invalid file type')
      }
      
      return validated
    }
  }
}

const convertTimeHHMMSS = (val) => {
  let hhmmss = new Date(val * 1000).toISOString().substr(11, 8)

  return hhmmss.indexOf("00:") === 0 ? hhmmss.substr(3) : hhmmss
}

const AudioPlayer = {
  props: {
    audioPlayerId: {
      type: String,
      default: 'audio-player'
    },
    audioFile: {
      type: String,
      default: null
    },
    autoPlay: {
      type: Boolean,
      default: false
    },
    initLoop: {
      type: Boolean,
      default: false
    },
    hasLoopBtn: {
      type: Boolean,
      default: true
    },
    hasStopBtn: {
      type: Boolean,
      default: true
    },
    hasMuteBtn: {
      type: Boolean,
      default: true
    },
    hasDownloadBtn: {
      type: Boolean,
      default: true
    },
    hasVolumeBtn: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      audio: null,
      seekBar: null,
      playing: false,
      dragging: false,
      loaded: false,
      currentSeconds: 0,
      durationSeconds: 0,
      loop: false,
      showVolume: false,
      previousVolume: 35,
      volume: 100,
      hasError: false,
    }
  },
  computed: {
    currentTime() {
      return convertTimeHHMMSS(this.currentSeconds)
    },
    durationTime() {
      return convertTimeHHMMSS(this.durationSeconds)
    },
    percentComplete() {
      return parseInt(this.currentSeconds / this.durationSeconds * 100)
    },
    muted() {
      return this.volume / 100 === 0
    }
  },
  watch: {
    playing(value) {
      if (value) {
        this.audio.play()
      } else {
        this.audio.pause()
      }
    },
    volume(value) {
      this.showVolume = false
      this.audio.volume = this.volume / 100
    }
  },
  methods: {
    download() {
      this.stop()
     // window.open(this.audioFile, 'download')
      window.location.assign(this.audioFile)
    },
    load() {
      if (this.audio.readyState >= 2) {
        this.loaded = true
        this.durationSeconds = parseInt(this.audio.duration)

        return this.playing = this.autoPlay
      }

      throw new Error('Failed to load sound file.')
    },
    mute() {
      if (this.muted) {
        return this.volume = this.previousVolume
      }

      this.previousVolume = this.volume
      this.volume = 0
    },
    seek(e) {
      this.playing = false
      
      const el = this.seekBar.getBoundingClientRect()
      const seekPos = (e.clientX - el.left) / el.width

      this.audio.currentTime = parseInt(this.audio.duration * seekPos)
    },
    stop() {
      this.playing = false
      this.audio.currentTime = 0
    },
    update() {
      this.currentSeconds = parseInt(this.audio.currentTime)
    },
    error() {
      this.hasError = true
      console.error('Error loading ' + this.audioFile)
    },
    onProgressMousedown(e) {
      this.dragging = true
    },
    onProgressMouseup(e) {
      if (this.dragging) {
        this.dragging = false
        this.seek(e)
        this.playing = true
      }
    },
    onProgressMousemove(e) {
      if (this.dragging) {
        this.seek(e)
      }
    }
  },
  created() {
    this.loop = this.initLoop
  },
  mounted() {
    this.audio = this.$el.querySelector('#' + this.audioPlayerId)
    this.audio.addEventListener('error', this.error)
    this.audio.addEventListener('play', () => { this.playing = true })
    this.audio.addEventListener('pause', () => { this.playing = false });
    this.audio.addEventListener('ended', this.stop)
    this.audio.addEventListener('timeupdate', this.update)
    this.audio.addEventListener('loadeddata', this.load)

    window.addEventListener('mouseup', this.onProgressMouseup)
    window.addEventListener('mousemove', this.onProgressMousemove)

    this.seekBar = this.$refs.audioPlayerSeekBar
  },
}


const Modal = {
  mixins: [BaseModal],
  created() {
    ModalPlugin.EventBus.$on(this.modalId, () => {
      this.show()
    })
  },
}

const ConfirmationModal = {
  mixins: [BaseModal],
  data() {
    return {
      yes: null,
      no: null
    }
  },
  methods: {
    confirm() {
      this.yes('yes')
      this.isOpen = false
    },
    close() {
      this.no('no')
      this.isOpen = false
    }
  },
  created() {
    ModalPlugin.EventBus.$on(this.modalId, (resolve, reject) => {
      this.show()
      this.yes = resolve
      this.no = reject
    })
  }
}