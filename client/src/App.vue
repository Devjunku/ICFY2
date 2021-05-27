<template>
  <div id="app">
    <nav class="navbar transparent8 navbar-expand fixed-top navbar-dark d-flex justify-content-between">
      
      <div class="d-flex ">
        <div class="nav-left">
          <div class="ms-3">
            <router-link :to="{ name: 'Movies'}" class="navbar-brand">
              <img src="./assets/logo3.png" alt="logo image" height="40">
            </router-link>  
          </div>
        </div>
        <div class="p-2">
          <input class="form-control" type="text" v-model.trim="search" @keyup.enter="showMap" placeholder="영화를 검색하세요!">
        </div>
      </div>
      
      <div v-if="showGuide" class="d-none d-lg-block" v-text="guide"></div>

      <div>

        <ul v-if="isLogin" class="navbar-nav">
          <i v-if="posterMode" class="far fa-newspaper fa-2x" @click="modeToggle"></i>
          <i v-else class="fas fa-portrait fa-2x" @click="modeToggle"></i>

          <li v-if="userinfo.is_superuser" class="nav-item mx-2">
            <div @click="goToAdmin" class="nav-link text-decoration-none fw-bold text-light" @mouseover="makeBlue" @mouseleave="makeWhite">관리자 모드</div>
          </li>
          <li class="nav-item mx-2">
            <router-link :to="{ name: 'MyProfile'}" class="nav-link text-decoration-none fw-bold text-light" @mouseover.native="makeBlue" @mouseleave.native="makeWhite">내 프로필</router-link>
          </li>
          <li class="nav-item mx-2">
            <router-link @click.native="logout" to="#" class="nav-link text-decoration-none fw-bold text-light" @mouseover.native="makeBlue" @mouseleave.native="makeWhite">로그아웃</router-link>
          </li>
        </ul>

        <ul v-else class="navbar-nav">
          <i v-if="posterMode" class="far fa-newspaper fa-2x" @click="modeToggle"></i>
          <i v-else class="fas fa-portrait fa-2x" @click="modeToggle"></i>

          <li class="nav-item mx-2">
            <router-link :to="{ name: 'Signup'}" class="nav-link text-decoration-none fw-bold text-light" @mouseover.native="makeBlue" @mouseleave.native="makeWhite">회원가입</router-link>
          </li>
          <li class="nav-item mx-2">
            <router-link :to="{ name: 'Login', params: { case: 1}}" class="nav-link text-decoration-none fw-bold text-light" @mouseover.native="makeBlue" @mouseleave.native="makeWhite">로그인</router-link>
          </li>
        </ul>

      </div>
    </nav>
    <br>
    <br>
    <router-view @login="isLogin = true"/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data: function() {
    return {
      isLogin: false,
      search: null,
    }
  },
  methods: {
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Movies' })
    },
    goToAdmin: function () {
      window.open(
        'http://127.0.0.1:8000/admin/',
        '_blank'
      );
    },
    makeBlue: function (event) {
      event.target.classList.replace("text-light","text-primary")
    },
    makeWhite: function (event) {
      event.target.classList.replace("text-primary","text-light")
    },
    // 중앙에 저장하겠다.
    modeToggle: function () {
      this.$store.dispatch('modeToggle')
    },
    showMap: function () {
      this.$router.push({ name: 'SearchResult',  params: { searchKeyword: this.search }, query: { t: new Date().getTime()} })
      this.search = ''
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
    }
  },
  computed: {
    userinfo: function () {
      return this.$store.state.userinfo
    },
    posterMode: function () {
      return this.$store.state.posterMode
    },
    guide: function () {
      return this.$store.state.guide
    },
    showGuide: function () {
      return this.$store.state.showGuide
    },
    signal: function () {
      return this.$store.state.signal
    },
    delete: function () {
      return this.$store.state.delete
    },
  },
  watch: {
    isLogin: function () {
      if (this.isLogin === true) {
        this.$store.dispatch('loginGuide')
      }
      else {
        this.$store.dispatch('logoutGuide')
      }
    },
    signal: function () {
      this.logout()
      this.$router.push({name: 'Login' , params: { case: 2}})
    },
    delete: function () {
      this.logout()
    },
  },
}
</script>


<style>
#app {
  font-family: 'Nanum Gothic', 'Noto Sans KR';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  background-color: #222425;
}

#nav {
  padding: 30px;

}

#nav a {
  font-weight: bold;
  color: #ffffff;
}

#nav a.router-link-exact-active {
  color: #d0d6d4;
}

.navbar {
  /* 어떤 색으로 할지 정해야 한다. */
  background-color: rgb(44, 43, 43);
  box-shadow: 0px 0px;
}

.transparent8 {
  zoom: 1;
 /* ie 5,6,7 bug fix */
  filter: alpha(opacity=100);
  opacity: 0.8; }


#guide {
  padding: 5px;
}

i:hover {
  color: skyblue; 
  cursor: pointer;
}

.nav-left {
  display: flex;
}
</style>