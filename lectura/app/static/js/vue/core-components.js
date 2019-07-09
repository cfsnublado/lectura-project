const ClickOutsideMixin = {
  methods: {
    onCloseOutside() {
      console.log('clicked outside')
    },
    closeOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.onCloseOutside()
      }
    },
    addClickOutsideHandler() {
      window.addEventListener('click', this.closeOutside)
    },
    removeClickOutsideHandler() {
      window.removeEventListener('click', this.closeOutside)
    }
  },
  created() {
    this.addClickOutsideHandler()
  },
  beforeDestroy() {
    this.removeClickOutsideHandler()
  }
}

const BaseMessage = {
  props: {
    messageType: {
      type: String,
      default: 'success'
    },
    messageText: {
      type: String,
      default: ''
    },
    initAutoClose: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      isOpen: true,
      timerId: null,
      timerDelay: 3000,
      autoClose: this.initAutoClose
    }
  },
  methods: {
    close() {
      clearTimeout(this.timerId)
      this.isOpen = false
    },
    load() {
      if (this.autoClose) {
        this.timerId = setTimeout(()=>{
          this.close()
        }, this.timerDelay) 
      }
    }
  },
  created() {
    this.load()
  },
}

const BaseDropdown = {
  mixins: [ClickOutsideMixin],
  props: {
    id: String,
    dropdownClasses: String,
    dropup: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isOpen: false,
    }
  },
  methods: {
    toggle(manual) {
      this.$emit('toggle')
      if (manual === true || manual === false) {
        this.isOpen = manual
      } else {
          this.isOpen = !this.isOpen
      }
    },
    onCloseOutside() {
      this.isOpen = false
    }
  }
}