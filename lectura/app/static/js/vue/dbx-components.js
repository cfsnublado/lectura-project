const Dbx = {
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
    }
  },
}


const DbxUserFiles = {
  props: {
    filesUrl: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      files: '',
      processing: false
    }
  },
  methods: {
    getFiles() {
      this.files = []
      this.processing = true
      
      axios.get(this.filesUrl)
      .then(response => {
        this.files = response.data.files
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
    },
    selectFile(file) {
      this.$emit('select-file', file)
    }
  },
  template: `
    <div>

    <button
    class="button is-primary"
    v-bind:class="[{ 'is-loading': processing }]"
    @click.prevent="getFiles"
    >
    Get User dbx files
    </button>

    <div class="menu">

    <ul class="menu-list">

    <li v-for="(file, index) in files">
    <a
    @click.prevent="selectFile(file)"
    > 
    {{ file.name }} 
    </a>
    </li>

    </ul>

    </div>

    </div>
  `
}

const DbxAudioFileUploader = {
  mixins: [AudioFileUploader],
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