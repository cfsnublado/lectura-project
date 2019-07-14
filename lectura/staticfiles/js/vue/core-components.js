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

const BaseFileUploader = {
  props: {
    initUploadUrl: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      uploadUrl: this.initUploadUrl,
      file: '',
      processing: false
    }
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0]
      // Set the input text.
      this.$refs.filename.innerHTML = this.file.name
    },
    submitFile() {
      if (this.validateFile()) {
        this.processing = true
        let formData = new FormData()
        formData.append('file', this.file);

        axios.post(
          this.uploadUrl,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        .then(response => {
          console.log(this.file)
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
        .finally(() => {
          this.processing = false
        })
      }
    },
    validateFile() {
      return true
    }
  },
  template: `
    <div class="file has-name is-fullwidth">

    <label class="file-label">

    <input 
    class="file-input" 
    type="file" 
    ref="file" 
    name="resume"
    @change="handleFileUpload"
    :disabled="processing"
    >

    <span class="file-cta">

    <span class="file-icon">
    <i class="fas fa-upload"></i>
    </span>

    <span class="file-label">
    <slot name="label-select-file">
    Choose a file
    </slot>
    </span>

    </span>

    <span class="file-name" ref="filename">
    </span>

    </label>

    <button 
    class="button is-primary"
    v-bind:class="[{ 'is-loading': processing }]"
    @click.prevent="submitFile"
    :disabled="file == ''"
    >

    <slot name="label-submit">
    Submit
    </slot>
    
    </button>

    </div>
  `
}