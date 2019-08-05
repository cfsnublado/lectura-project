const DbxFile = {
  props: {
    initFile: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      file: this.initFile
    }
  },
  methods: {
    selectFile(file) {
      this.$emit('select-file', file)
    }
  }
}

const DbxUserFiles = {
  components: {
    'dbx-file': DbxFile
  },
  mixins: [AjaxProcessMixin],
  props: {
    filesUrl: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      files: '',
    }
  },
  methods: {
    getFiles() {
      this.files = []
      this.process()
      
      axios.get(this.filesUrl)
      .then(response => {
        this.files = response.data.files
        console.log(this.files)
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
        this.complete()
      })
    },
    selectFile(path) {
      this.$emit('select-file', path)
    },
  },
}

const DbxAudioFileUploader = {
  mixins: [
    AudioFileUploader
  ],
  data() {
    return {
      fileMetadata: ''
    }
  },
  methods: {
    success(response) {
      this.fileMetadata = response.data['file_metadata']
      this.$emit('upload-file', this.fileMetadata)
    }
  },
  template: `
    <div>
    
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

    </div>
  `
}

const Dbx = {
  mixins: [AjaxProcessMixin],
  components: {
    'dbx-user-files': DbxUserFiles,
    'dbx-audio-file-uploader': DbxAudioFileUploader,
  },
  props: {
    sharedLinkUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      processing: false
    }
  },
  methods: {
    getSharedLink(dbxPath) {
      this.processing = true

      console.log(dbxPath)
      
      axios.post(
        this.sharedLinkUrl,
        {'dbx_path': dbxPath}
      )
      .then(response => {
        if (response.data['shared_link']) {
          this.$refs['audio-url'].value = response.data['shared_link'].replace('dl=0', 'dl=1')
        }
      })
      .catch(error => {
        if (error.response) {
          console.log(error.response)
        } else if (error.request) {
          console.log(error.request)
        } else {
          console.log(error)
        }
        console.log(error.config)
      })
      .finally(() => {
        this.processing = false
      })
    },
    onUploadFile(dbxPath) {
      this.getSharedLink(dbxPath)
      this.$refs['dbx-user-files'].getFiles()
      console.log("SHITTT")
    }
  },
}