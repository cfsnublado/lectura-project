const UserSearch = {
  mixins: [
    BaseSearch
  ],
  methods: {
    setResult(result) {
      this.searchTerm = result
      this.isOpen = false
      if (this.searchOnSelect) {
        this.search()
      }
    },
    search() {
      clearTimeout(this.searchTimerId)
      url = this.searchUrl + "?username=" + encodeURIComponent(this.searchTerm)
      window.location.assign(url)
    }
  }
}
const Project = {
  mixins: [
    AdminMixin,
    VisibleMixin,
    MarkdownMixin
  ],
  props: {
    initProject: {
      type: Object,
      required: true
    },
    initViewUrl: {
      type: String,
      default: ''
    },
    initEditUrl: {
      type: String,
      default: ''
    },
    initDeleteUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      project: this.initProject,
      viewUrl: this.initViewUrl,
      editUrl: this.initEditUrl,
      deleteUrl: this.initDeleteUrl,
      idPlaceholder: '0',
      slugPlaceholder: 'zzz'
    }
  },
  methods: {
    view() {
      if (this.viewUrl) {
        window.location.assign(this.viewUrl)
      }
    },
    edit() {
      if (this.editUrl) {
        window.location.assign(this.editUrl)
      }
    },
    remove() {
      this.$emit('delete-project', this.project.id)
    }
  },
  created() {
    if (this.initViewUrl) {
      this.viewUrl = this.initViewUrl
        .replace(this.idPlaceholder, this.project.id)
        .replace(this.slugPlaceholder, this.project.slug)   
    }

    if (this.initEditUrl) {
      this.editUrl = this.initEditUrl
        .replace(this.idPlaceholder, this.project.id)
        .replace(this.slugPlaceholder, this.project.slug)   
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(this.idPlaceholder, this.project.id)
    }
  }
}

const Projects = {
  components: {
    'project': Project
  },
  mixins: [
    AdminMixin,
    AjaxProcessMixin,
    PaginationMixin
  ],
  props: {
    projectsUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      projects: null
    }
  },
  methods: {
    getProjects(page=1) {
      this.process()

      params = {
        page: page
      }

      axios.get(this.projectsUrl, {
        params: params
      })
      .then(response => {
        this.projects = response.data.results
        this.setPagination(
          response.data.previous,
          response.data.next,
          response.data.page_num,
          response.data.count,
          response.data.num_pages
        )
        VueScrollTo.scrollTo({
          el: '#projects-scroll-top',
        })
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
      .finally(() => {
        this.complete()
      })
    },
    onDeleteProject(index) {
      this.$delete(this.projects, index)
    }
  },
  created() {
    this.getProjects()
  }
}

const ProjectMember = {
  mixins: [
    AdminMixin,
    VisibleMixin
  ],
  props: {
    initProjectMember: {
      type: Object,
      required: true
    },
    initViewUrl: {
      type: String,
      default: ''
    },
    initEditUrl: {
      type: String,
      default: ''
    },
    initDeleteUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      projectMember: this.initProjectMember,
      viewUrl: this.initViewUrl,
      editUrl: this.initEditUrl,
      deleteUrl: this.initDeleteUrl,
      idPlaceholder: '0',
      slugPlaceholder: 'zzz'
    }
  },
  methods: {
    view() {
      if (this.viewUrl) {
        window.location.assign(this.viewUrl)
      }
    },
    edit() {
      if (this.editUrl) {
        window.location.assign(this.editUrl)
      }
    },
    remove() {
      this.$emit('delete-project-member', this.projectMember.id)
      console.log(this.projectMember.id)
      console.log('delete project member')
    }
  },
  created() {
    if (this.initViewUrl) {
      this.viewUrl = this.initViewUrl
        .replace(this.idPlaceholder, this.projectMember.id)
    }

    if (this.initEditUrl) {
      this.editUrl = this.initEditUrl
        .replace(this.idPlaceholder, this.projectMember.id)
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(this.idPlaceholder, this.projectMember.id)
    }
  }
}

const ProjectMembers = {
  components: {
    'project-member': ProjectMember
  },
  mixins: [
    AdminMixin,
    AjaxProcessMixin,
    PaginationMixin
  ],
  props: {
    projectMembersUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      projectMembers: null
    }
  },
  methods: {
    getProjectMembers(page=1) {
      this.process()

      params = {
        page: page
      }

      axios.get(this.projectMembersUrl, {
        params: params
      })
      .then(response => {
        this.projectMembers = response.data.results
        this.setPagination(
          response.data.previous,
          response.data.next,
          response.data.page_num,
          response.data.count,
          response.data.num_pages
        )
        VueScrollTo.scrollTo({
          el: '#project-members-scroll-top',
        })
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
      .finally(() => {
        this.complete()
      })
    },
    onDeleteProjectMember(index) {
      console.log("FUCK")
      this.$delete(this.projectMembers, index)
    }
  },
  created() {
    this.getProjectMembers()
  }
}


const Post = {
  mixins: [
    AdminMixin,
    VisibleMixin,
    MarkdownMixin
  ],
  props: {
    initPost: {
      type: Object,
      required: true
    },
    initViewUrl: {
      type: String,
      default: ''
    },
    initEditUrl: {
      type: String,
      default: ''
    },
    initDeleteUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      post: this.initPost,
      viewUrl: this.initViewUrl,
      editUrl: this.initEditUrl,
      deleteUrl: this.initDeleteUrl,
      idPlaceholder: '0',
      slugPlaceholder: 'zzz'
    }
  },
  methods: {
    view() {
      if (this.viewUrl) {
        window.location.assign(this.viewUrl)
      }
    },
    edit() {},
    remove() {
      this.$emit('delete-post', this.post.id)
    }
  },
  created() {
    if (this.initViewUrl) {
      this.viewUrl = this.initViewUrl
        .replace(this.idPlaceholder, this.post.id)
        .replace(this.slugPlaceholder, this.post.slug)
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(this.idPlaceholder, this.post.id)
    }
  }
}

const Posts = {
  components: {
    'post': Post
  },
  mixins: [
    AdminMixin,
    AjaxProcessMixin,
    PaginationMixin
  ],
  props: {
    postsUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      posts: null
    }
  },
  methods: {
    getPosts(page=1) {
      this.process()

      params = {
        page: page
      }

      axios.get(this.postsUrl, {
        params: params
      })
      .then(response => {
        this.posts = response.data.results
        console.log(this.posts)
        this.setPagination(
          response.data.previous,
          response.data.next,
          response.data.page_num,
          response.data.count,
          response.data.num_pages
        )
        VueScrollTo.scrollTo({
          el: '#posts-scroll-top',
        })
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
      .finally(() => {
        this.complete()
      })
    },
    onDeletePost(index) {
      this.$delete(this.posts, index)
    }
  },
  created() {
    this.getPosts()
  }
}

const PostAudio = {
  mixins: [
    AdminMixin,
    VisibleMixin,
    MarkdownMixin
  ],
  props: {
    initAudio: {
      type: Object,
      required: true
    },
    initViewUrl: {
      type: String,
      default: ''
    },
    initEditUrl: {
      type: String,
      default: ''
    },
    initDeleteUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      audio: this.initAudio,
      viewUrl: this.initViewUrl,
      editUrl: this.initEditUrl,
      deleteUrl: this.initDeleteUrl,
      idPlaceholder: '0'
    }
  },
  methods: {
    edit() {
      if (this.editUrl) {
        window.location.assign(this.editUrl)
      }
    },
    remove() {
      this.$emit('delete-post-audio', this.audio.id)
    }
  },
  created() {
    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(this.idPlaceholder, this.audio.id)
    }

    if (this.initEditUrl) {
      this.editUrl = this.initEditUrl
        .replace(this.idPlaceholder, this.audio.id)
      console.log(this.editUrl)
    }
  }
}

const PostAudios = {
  components: {
    'post-audio': PostAudio
  },
  mixins: [
    AdminMixin,
    AjaxProcessMixin,
    PaginationMixin
  ],
  props: {
    postAudiosUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      postAudios: null
    }
  },
  methods: {
    getPostAudios(page=1) {
      this.process()

      params = {
        page: page
      }

      axios.get(this.postAudiosUrl, {
        params: params
      })
      .then(response => {
        this.postAudios = response.data.results
        this.setPagination(
          response.data.previous,
          response.data.next,
          response.data.page_num,
          response.data.count,
          response.data.num_pages
        )
        VueScrollTo.scrollTo({
          el: '#post-audios-scroll-top',
        })
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
      .finally(() => {
        this.complete()
      })
    },
    onDeletePostAudio(index) {
      this.$delete(this.postAudios, index)
    }
  },
  created() {
    this.getPostAudios()
  }
}

const PostAudioPlayer = {
  mixins: [
    AudioPlayer,
    AjaxProcessMixin,
  ],
  props: {
    audiosUrl: {
      type: String,
      required: true
    },
    playlistOpenClass: {
      type: String,
      default: 'playlist-open'
    }
  },
  data() {
    return {
      audios: null,
      selectedAudio: null,
      selectedAudioIndex: null,
      showPlaylist: false
    }
  },  
  methods: {
    getAudios() {
      if (this.audiosUrl) {
        this.process()

        axios.get(this.audiosUrl)
        .then(response => {
          this.audios = response.data

          if (this.audios.length > 0) {
            this.selectAudio(0)
          }

          this.success()
        })
        .catch(error => {
          if (error.response) {
            console.error(error.response)
          } else if (error.request) {
            console.error(error.request)
          } else {
            console.error(error.message)
          }
          console.error(error.config)
        })
        .finally(() => {
          this.complete()
        })
      }
    },
    selectAudio(index) {
      this.audioLoaded = false
      this.selectedAudio = this.audios[index]
      this.selectedAudioIndex = index
      this.audio.src = this.selectedAudio.audio_url
      this.togglePlaylist(false)
    },
    togglePlaylist(boolVal) {
      if (boolVal === true || boolVal === false) {
        this.showPlaylist = boolVal
      }
      else {
        this.showPlaylist = !this.showPlaylist
      }
      
      if (this.showPlaylist) {
        this.$el.classList.add(this.playlistOpenClass)
      } 
      else {
        this.$el.classList.remove(this.playlistOpenClass)
      }
    }
  },
  created() {
    this.loop = this.initLoop
    this.getAudios()
  },
}