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
      deleteUrl: this.initDeleteUrl
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
        .replace(0, this.project.id)
        .replace('zzz', this.project.slug)   
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(0, this.project.id)
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
      default: ''
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
      deleteUrl: this.initDeleteUrl
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
        .replace(0, this.post.id)
        .replace('zzz', this.post.slug)
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(0, this.post.id)
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

