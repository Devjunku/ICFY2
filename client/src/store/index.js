import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate"


Vue.use(Vuex)

const MOVIES_LIST_URL = 'http://127.0.0.1:8000/movies/'

export default new Vuex.Store({
  // state를 브라우저에 저장해두기
  // 새로고침해도 정보가 남아있다.
  plugins: [
    createPersistedState(),
  ],
  state: {
    movies: [],
    review: null,
    username: null,
    userinfo: [],
    posterMode: true,
    guide: "도움말: 로그인을 하면 맞춤 영화 추천을 받을 수 있고 영화에 대한 리뷰를 볼 수도 있어요!",
    showGuide: true,
    signal: false,
    delete: false,
  },
  mutations: {
    CREATE_MOVIES: function (state, movies) {
      state.movies = movies
    },
    UPDATE_REVIEW:function (state, review) {
      state.review = review
    },
    STORE_USERNAME: function (state, username) {
      state.username = username
    },
    STORE_USERINFO: function (state, userInfo) {
    state.userinfo = userInfo
    },
    MODE_TOGGLE: function (state) {
      if (state.posterMode === true) {
        state.posterMode = false
      } else {
        state.posterMode = true
      }
    },
    LOGIN_GUIDE: function (state) {
      state.guide = "도움말: 오른쪽의 아이콘을 클릭하면 영화의 레이아웃을 변경할 수 있습니다."
    },
    LOGOUT_GUIDE: function (state) {
      state.guide = "도움말: 로그인을 하면 맞춤 영화 추천을 받을 수 있고 영화에 대한 리뷰를 볼 수도 있어요!"
    },
    MY_PROFILE_GUIDE: function (state) {
      state.guide = "도움말: 초록색 버튼을 눌러 도움말 버튼을 끌 수 있습니다."
    },
    OTHER_PROFILE_GUIDE: function (state) {
      state.guide = "도움말: 파란색 버튼을 눌러 다른 사람을 팔로우할 수 있습니다."
    },
    REVIEW_PAGE_GUIDE: function (state) {
      state.guide = "도움말: 제목을 클릭하면 리뷰를, 작성자를 클릭하면 프로필을 볼 수 있습니다."
    },
    REVIEW_DETAIL_GUIDE: function (state) {
      state.guide = "도움말: 댓글은 작성하고 수정, 삭제할 수 있습니다."
    },
    CREATE_REVIEW_GUIDE: function (state) {
      state.guide = "도움말: 별을 클릭해서 0점부터 10점까지 평점을 줄 수 있습니다."
    },
    MOVIE_DETAIL_GUIDE: function (state) {
      state.guide = "도움말: 영화를 보고 싶다면 보라색 버튼을 눌러볼까요?"
    },
    MAIN_GUIDE: function (state) {
      state.guide = "도움말: 오른쪽의 아이콘을 클릭하면 영화의 레이아웃을 변경할 수 있습니다."
    },
    GUIDE_TOGGLE: function (state) {
      state.showGuide = !state.showGuide
    },
    CHANGE_SIGNAL: function (state) {
      state.signal = !state.signal
    },
    DELETE_USER: function (state) {
      state.delete = !state.delete
    },
  },
  actions: {
    createMovies: function ({commit}) {
      axios.get(MOVIES_LIST_URL)
      .then(res => {
        // console.log(res)
        commit('CREATE_MOVIES', res.data)
      })
      .catch(err => {
        console.log(err)
      })
    },
    updateReview: function ({ commit }, review) {
      commit('UPDATE_REVIEW', review)
    },
    storeUsername: function ({ commit }, username) {
      commit('STORE_USERNAME', username)
    },
    storeUserInfo: function ({ commit }, userInfo) {
      commit('STORE_USERINFO', userInfo)
    },
    modeToggle: function ({ commit }) {
      commit('MODE_TOGGLE')
    },
    loginGuide: function ({ commit }) {
      commit('LOGIN_GUIDE')
    },
    logoutGuide: function ({ commit }) {
      commit('LOGOUT_GUIDE')
    },
    myProfileGuide: function ({ commit }) {
      commit('MY_PROFILE_GUIDE')
    },
    otherProfileGuide: function ({ commit }) {
      commit('OTHER_PROFILE_GUIDE')
    },
    reviewPageGuide: function ({ commit }) {
      commit('REVIEW_PAGE_GUIDE')
    },
    reviewDetailGuide: function ({ commit }) {
      commit('REVIEW_DETAIL_GUIDE')
    },
    createReviewGuide: function ({ commit }) {
      commit('CREATE_REVIEW_GUIDE')
    },
    movieDetailGuide: function ({ commit }) {
      commit('MOVIE_DETAIL_GUIDE')
    },
    mainGuide: function ({ commit }) {
      commit('MAIN_GUIDE')
    },
    guideToggle: function ({ commit }) {
      commit('GUIDE_TOGGLE')
    },
    changeSignal:  function ({ commit }) {
      commit('CHANGE_SIGNAL')
    },
    deleteUser: function ({ commit }) {
      commit('DELETE_USER')
    },
  },
  modules: {
  }
})
