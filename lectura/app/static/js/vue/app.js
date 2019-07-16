Vue.component('alert-message', AlertMessage)
Vue.component('navbar-dropdown', NavbarDropdown)
Vue.component('audio-file-uploader', AudioFileUploader)
Vue.component('audio-player', AudioPlayer)

// Reading components
Vue.component('projects', Projects)
Vue.component('project', Project)

VueScrollTo.setDefaults({
    container: "body",
    duration: 500,
    easing: "ease",
    offset: 0,
    force: true,
    cancelable: true,
    onStart: false,
    onDone: false,
    onCancel: false,
    x: false,
    y: true
})

// Instantiate main app instance.
const vm = new Vue({
  el: '#app-container',
  delimiters: ['[[', ']]'],
  data: {
    appSessionUrl: appSessionUrl,
    showSidebar: sidebarExpanded,
    sidebarOpenClass: 'sidebar-expanded',
    showNavbarMenu: false,
    navbarMenuOpenClass: 'is-active',
    windowWidth: 0,
    windowWidthSmall: 640,
    windowResizeTimer: null,
  },
  computed: {
    smallWindow: function() {
      return this.windowWidth <= this.windowWidthSmall
    }
  },
  methods: {
    toggleSidebar(manual) {
      // If manual is set to true or false, override toggle.
      if (manual === true || manual === false) {
        this.showSidebar = manual
      } else {
        this.showSidebar = !this.showSidebar
      }
  
      if (this.showSidebar) {
        document.body.classList.add(this.sidebarOpenClass)
      } else {
        document.body.classList.remove(this.sidebarOpenClass)
      }
    },
    toggleNavbarMenu(manual) {
      // If manual is set to true or false, override toggle.
      if (manual === true || manual === false) {
        this.showNavbarMenu = manual
      } else {
        this.showNavbarMenu = !this.showNavbarMenu
      }
  
      if (this.showNavbarMenu) {
        this.$refs.navbarMenu.classList.add(this.navbarMenuOpenClass)
      } else {
        this.$refs.navbarMenu.classList.remove(this.navbarMenuOpenClass)
      }
    },
    windowResize() {
      // Fire event after window resize completes.
      clearTimeout(this.windowResizeTimer)
      this.windowResizeTimer = setTimeout(()=>{
        this.windowWidth = document.documentElement.clientWidth
        if (this.smallWindow) {
          console.log('small')
        } else {
        }
      }, 250);
    }
  },
  mounted() {
    this.$nextTick(function() {
      window.addEventListener('resize', this.windowResize);
      this.windowResize()
    })
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.windowResize);
  }
})