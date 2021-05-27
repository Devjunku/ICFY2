<template>
  <div class="container">
    <br>
    <br>
    <h1>{{this.username}}님의 프로필</h1>
    <div class="d-flex justify-content-evenly">
      
      <div>
        <div class="p-1">
          <p @click="clickFollower" id="fwe">팔로워: {{followers_num}}</p>
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
          <p @click="clickFollowing" id="fwi">팔로잉: {{followings_num}}</p>
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

      <div>
        <button v-if="flag" @click="clickBtn" class="btn btn-primary"> 언팔로우하기 </button> 
        <button v-else @click="clickBtn" class="btn btn-primary"> 팔로우하기 </button> 
      </div>
    </div>

    <hr>
    <h3 class="d-flex justify-content-start">{{this.username}}님이 좋아하는 영화들</h3>
    <br>
    <div class="container">
      <div v-if="posterMode" class="row row-cols-1 row-cols-md-6 g-4">
        <MoviesList
        v-for="(movie, idx) in likedMovies" 
            :key="idx+'c'"
            :movie="movie"
        />
      </div>
      <div v-else>
        <MoviesArticle
        v-for="(movie, idx) in likedMovies" 
            :key="idx+'d'"
            :movie="movie"
        />
      </div>

    </div>
    <br>
    <hr>
    <h3 class="d-flex justify-content-start">{{this.username}}님의 리뷰</h3>
      <section class="col-12 col-lg-12 ps-4 pt-4">
        <div class="d-none d-lg-block">
          <table class="table">
            <thead>
            <tr class="table-light">
              <th scope="col">영화</th>
              <th scope="col">리뷰 제목</th>
              <th scope="col">{{this.username}}님의 점수</th>
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
    <h3 class="d-flex justify-content-start">{{this.username}}님의 댓글</h3>
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
  name: 'SelectedProfile',
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
    username: null,
    likedMovies: [],
    flag: null,
    }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    // 리뷰 댓글 정보 불러오기
    searchInfo: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/profile/${this.$route.params.userId}/`,
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
    // 팔로우 토글
    clickBtn: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/follow/${this.$route.params.userId}/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.followings = res.data.followings
        this.followers = res.data.followers
        this.followings_num = res.data.followings_num
        this.followers_num = res.data.followers_num
        this.flag = !this.flag
      })
      .catch(err => {
        console.log(err)
      })  
    },
    // 팔로우 정보 받아오기 (처음에)
    searchFollow: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/followinfo/${this.$route.params.userId}/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.followings = res.data.followings
        this.followers = res.data.followers
        this.followings_num = res.data.followings_num
        this.followers_num = res.data.followers_num
        if (res.data.flag===1) {
          this.flag = true
        } else {
          this.flag = false
        }
        console.log(res.data)
      })
      .catch(err => {
        console.log(err)
      })  
    },

    // 프로필 유저네임 받아오기
    searchUserName: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/find/${this.$route.params.userId}/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.username = res.data.username
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
    toggleHeart:  function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/like/show/${this.$route.params.userId}/`,
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res.data)
        this.likedMovies = res.data
      })
      .catch(err => {
        console.log(err)
      })
    },
  },
  computed:  {
    userinfo: function () {
      return this.$store.state.userinfo
    },
    posterMode: function () {
      return this.$store.state.posterMode
    },
  },
  created: function () {
    this.searchInfo()
    this.searchFollow()
    this.searchUserName()
    this.toggleHeart()
    this.$store.dispatch('otherProfileGuide')
  },
}
</script>

<style>

</style>