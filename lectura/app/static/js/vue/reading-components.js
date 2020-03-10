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
        window.location.replace(this.viewUrl)
      }
    },
    edit() {},
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
        window.location.replace(this.viewUrl)
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
    remove() {
      this.$emit('delete-post-audio', this.audio.id)
    }
  },
  created() {
    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(this.idPlaceholder, this.audio.id)
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
  },
  methods: {
    getAudios() {
      if (this.audiosUrl) {
        this.process()

        axios.get(this.audiosUrl)
        .then(response => {
          this.audios = response.data
          console.log(this.audios)
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
      }
    },
  },
  created() {
    this.loop = this.initLoop
    this.getAudios()
  },
}