const Projects = {
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
      projects: []
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
  },
  created() {
    this.getProjects()
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
      this.isVisible = false
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

const Readings = {
  mixins: [
    AdminMixin,
    AjaxProcessMixin,
    PaginationMixin
  ],
  props: {
    readingsUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      readings: []
    }
  },
  methods: {
    getReadings(page=1) {
      this.process()

      params = {
        page: page
      }

      axios.get(this.readingsUrl, {
        params: params
      })
      .then(response => {
        this.readings = response.data.results
        this.setPagination(
          response.data.previous,
          response.data.next,
          response.data.page_num,
          response.data.count,
          response.data.num_pages
        )
        VueScrollTo.scrollTo({
          el: '#readings-scroll-top',
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
  },
  created() {
    this.getReadings()
  }
}

const Reading = {
  mixins: [
    AdminMixin,
    VisibleMixin,
    MarkdownMixin
  ],
  props: {
    initReading: {
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
      reading: this.initReading,
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
      this.isVisible = false
    }
  },
  created() {
    if (this.initViewUrl) {
      this.viewUrl = this.initViewUrl
        .replace(0, this.reading.id)
        .replace('zzz', this.reading.slug)
    }

    if (this.initDeleteUrl) {
      this.deleteUrl = this.initDeleteUrl
        .replace(0, this.reading.id)
    }
  }
}