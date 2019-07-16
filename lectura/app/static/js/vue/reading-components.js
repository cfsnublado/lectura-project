const Projects = {
  mixins: [
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
  },
  created() {
    this.getProjects()
  }
}