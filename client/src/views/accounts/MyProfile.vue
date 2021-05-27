<template>
  <div class="container">
    <br>
    <br>
    <h1>{{ userinfo.username }}의 프로필</h1>
    <br>
    <div class="d-flex justify-content-evenly align-items-baseline">
      <!-- 버튼들 -->
      <div>
        <div class="p-3">
          <div v-text="messageWarning" class="text-warning"></div>
          <button v-if="showGuide" class="btn btn-success me-3" @click="guideToggle">도움말 모드 끄기</button>
          <button v-else class="btn btn-success me-3" @click="guideToggle">도움말 모드 켜기</button>
          <button class="btn btn-warning me-3" @click="toggleForm">비밀번호 변경</button>
          <button class="btn btn-danger me-3" @click="deleteUserCheck">회원 탈퇴</button>
          <div v-text="message" class="text-warning mt-3"></div>
          <div v-if="check" class="p-2">
            <span class="d-flex justify-content-center">
              <div class="p-2">
                <input class="form-control" type="password" id="password" v-model="deleteUserPassword" placeholder="비밀번호를 입력하세요">
              </div>
              <div class="p-2">
                <button class="btn btn-danger" @click="deleteUser">확인</button>
              </div>
            </span>
            <hr>
          </div>
          <div v-if="passwordFlag">
            <div class="p-2">
              <input class="form-control" type="password" id="password" v-model="password" placeholder="비밀번호를 입력하세요">
            </div>
            <div class="p-2">
              <input class="form-control" type="password" id="password" v-model="newPassword" placeholder="새 비밀번호를 입력하세요">
            </div>
            <div class="p-2">
              <input class="form-control" type="password" id="passwordConfirmation" v-model="newPasswordConfirmation" placeholder="새 비밀번호를 재입력하세요">
            </div>
            <div>
              <button class="btn btn-warning" @click="passwordChange">확인</button>
            </div>
            <hr>
          </div>
        </div>
      </div>

      <!-- 팔로우 팔로워 -->
      <div class="d-flex justify-content-evenly">
        <div>
          <div class="p-1">
            <h4 @click="clickFollower" id="fwe">팔로워: {{followers_num}}</h4>
          </div>
          <div v-if="this.showFollower">
            <ul>
              <FollowItem
                v-for="(person, idx) in followers"
                :key="idx+'d'"
                :person="person"
              />
            </ul>
          </div>
        </div>
        <div>
          <div class="p-1">
            <h4 @click="clickFollowing" id="fwi">팔로잉: {{followings_num}}</h4>
          </div>
          <div v-if="this.showFollowing" class="d-inline-block">
            <ul>
              <FollowItem
                v-for="(person, idx) in followings"
                :key="idx+'c'"
                :person="person"
              />
            </ul>
          </div>
        </div>
      </div>
    </div>


      <br>
      <hr>
    <h3 class="d-flex justify-content-start">내가 좋아한 영화들</h3>
    <div class="container pt-4">
      <div v-if="posterMode" class="row row-cols-1 row-cols-md-6 g-4">
        <MoviesList
        v-for="(movie, idx) in likeMovies" 
            :key="idx+'c'"
            :movie="movie"
        />
      </div>
      <div v-else>
        <MoviesArticle
        v-for="(movie, idx) in likeMovies" 
            :key="idx+'d'"
            :movie="movie"
        />
      </div>
    </div>
    <hr>
    <h3 class="d-flex justify-content-start">내 리뷰</h3>
      <section class="col-12 col-lg-12 ps-4 pt-4">
        <div class="d-none d-lg-block">
          <table class="table">
            <thead>
            <tr class="table-light">
              <th scope="col">영화</th>
              <th scope="col">리뷰 제목</th>
              <th scope="col">내가 준 점수</th>
              <th scope="col">작성 시간</th>
            </tr>
            </thead>
            <tbody>
            <ProfileReview
                v-for="(review, idx) in reviews" 
                :key="idx+'a'"
                :review="review"
              />  
            </tbody>
          </table>
        </div>
      </section>
    <hr>
    <h3 class="d-flex justify-content-start">내 댓글</h3>
      <section class="col-12 col-lg-12 ps-4 pt-4">
        <div class="d-none d-lg-block">
          <table class="table">
            <thead>
            <tr class="table-light">
              <th scope="col">댓글 제목</th>
              <th scope="col">댓글이 작성된 리뷰</th>
              <th scope="col">작성 시간</th>
            </tr>
            </thead>
            <tbody>
              <ProfileComment
                  v-for="(comment, idx) in comments" 
                  :key="idx+'b'"
                  :comment="comment"
                />
            </tbody>
          </table>
        </div>
      </section>
  </div>
</template>

<script>
import axios from 'axios'

import ProfileReview from '@/components/ProfileReview'
import ProfileComment from '@/components/ProfileComment'
import FollowItem from '@/components/FollowItem'
import MoviesList from '@/components/MoviesList'
import MoviesArticle from '@/components/MoviesArticle'


export default {
  name: 'MyProfile',
   components: {
    ProfileReview,
    ProfileComment,
    FollowItem,
    MoviesList,
    MoviesArticle

  },
  data: function() {
    return {
    reviews: [],
    comments: [],
    followings: [],
    followers: [],
    followings_num: null,
    followers_num: null,
    showFollower: false,
    showFollowing: false,
    likeMovies: [],
    passwordFlag: false,
    password: null,
    newPassword: null,
    newPasswordConfirmation: null,
    message: "",
    check: false,
    deleteUserPassword: null,
    messageWarning: null,
    }
  },
  methods: {
    guideToggle: function () {
      this.$store.dispatch('guideToggle')
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    searchInfo: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/profile/${this.userinfo.id}/`,
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res.data)
        this.reviews = res.data.review
        this.comments = res.data.comment
      })
      .catch(err => {
        console.log(err)
      })  
    },
    toggleHeart:  function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/like/show/',
        headers: this.setToken(),
      })
      .then(res => {
        this.likeMovies = res.data
      })
      .catch(err => {
        console.log(err)
      })
    },
    clickFollower: function () {
      if (this.showFollower === true){
        this.showFollower = false
      }
      else {
        this.showFollower = true
      }
    },
    clickFollowing: function () {
       if (this.showFollowing === true){
        this.showFollowing = false
      }
      else {
        this.showFollowing = true
      }
    },
    // 팔로우 정보 받아오기 (처음에)
    searchFollow: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/followinfo/${this.userinfo.id}/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.followings = res.data.followings
        this.followers = res.data.followers
        this.followings_num = res.data.followings_num
        this.followers_num = res.data.followers_num
      })
      .catch(err => {
        console.log(err)
      })  
    },
    toggleForm: function () {
      this.passwordFlag = !this.passwordFlag
    },

    passwordChange: function () {
      if (this.newPassword === this.newPasswordConfirmation) {
        axios({
            method: 'put',
            url: 'http://127.0.0.1:8000/accounts/password/',
            data: {
              password: this.password,
              newPassword: this.newPassword,
            },
            headers: this.setToken(),
          })
            .then(res => {
              console.log(res)
              localStorage.setItem('jwt', res.data.token)
              this.password = ""
              this.newPassword = ""
              this.newPasswordConfirmation = ""
              this.message = res.data.message
              if (this.message === 1) {
                // case가 2면 다시 로그인하라는 메시지를 띄우겠다.
                // 자꾸 메인 화면으로 이동해서
                // 이번에는 여기 거쳐서 login으로 가겠다.
                this.$store.dispatch('changeSignal')
                }
                
            })
            .catch(err => {
              console.log(err)
            })
        }
      else {
        this.message = "바꿀 비밀번호 입력과 재입력이 일치하지 않습니다."
      }
    },
    deleteUserCheck: function () {
      this.check = !this.check
    },
    deleteUser: function () {
        axios({
            method: 'delete',
            url: 'http://127.0.0.1:8000/accounts/delete/',
            data: {
              password: this.deleteUserPassword
            },
            headers: this.setToken(),
          })
            .then(res => {
              console.log(res)
              if (res.data.message === 1) {
                this.$store.dispatch('deleteUser')
              }
              else {
                this.messageWarning = res.data.message
              }
            })
            .catch(err => {
              console.log(err)
            })
    }
  },
  computed:  {
    userinfo: function () {
      return this.$store.state.userinfo
    },
    showGuide: function () {
      return this.$store.state.showGuide
    }, 
    posterMode: function () {
      return this.$store.state.posterMode
    },
  },
  created: function () {
    this.searchInfo()
    this.searchFollow()
    this.toggleHeart()
    this.$store.dispatch('myProfileGuide')
  },
}
</script>

<style>
#fwi:hover {
  color: skyblue; 
  cursor: pointer;
}

#fwe:hover {
  color: skyblue; 
  cursor: pointer;
}
</style>