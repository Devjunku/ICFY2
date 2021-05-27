<template>
  <!-- col-8로 폭을 줄였다. -->
  <div v-if="review" class="container col-8">
    <br>
      <h3>{{ review.title }}</h3>
    <hr>
    <div class="d-flex flex-row-reverse">
      <h5 class="ms-3">평점: {{ review.review_score }}</h5>
      <div v-if="review.created_at===review.updated_at" class="d-flex flex-row-reverse">
        <h5>수정되지 않은 글</h5>
      </div>
      <div v-else>
        <h5>수정 시간: {{ format_date(review.updated_at) }}</h5>
      </div>
      <h5 class="me-3">작성 시간: {{ format_date(review.created_at) }}</h5>
      <h5 class="me-3 writer" @click="goToProfile">작성자 : {{ username }}</h5>
    </div>
    <hr>
    <h4>{{ review.content }}</h4>
    <hr>
    <br>
    <div class="d-flex flex-row-reverse" v-if="requestUser.id === review.user">
      <button class="btn btn-danger" @click="deleteReview">리뷰 삭제</button>
      <button class="btn btn-warning me-3" @click="updateReview">리뷰 수정</button>
    </div>
    <br>
    <div class="text-warning fw-bold">Comments</div>
    <br>
    <CommentItem
      v-for="(comment, idx) in comments" 
      :key="idx"
      :comment="comment"
      @delete-comment="showReviewDetail"
      @update-comment="showReviewDetail"
    />
    <br>
    <br>
    <div>
      <label class="text-warning fw-bold" for="content">댓글: </label>
      <input type="text" id="content" size="35" v-model="commentContent" @keyup.enter="createComment">
      <button class="ms-3 btn btn-warning" @click="createComment">댓글 쓰기</button>
    </div>
    <br>
    <br>
  </div>
</template>

<script>
import CommentItem from '@/components/CommentItem'

import axios from 'axios'
import moment from 'moment'


export default {
  name: 'ReviewDetail',
  components: {
    CommentItem
  },
  data: function () {
    return {
      review: null,
      comments: [],
      commentContent: null,
      username: null,
    }
  },
  methods: {
    format_date: function (value) {
        if (value) {
          return moment(String(value)).format('YYYY-MM-DD HH:mm')
        }
    },
    goToProfile:  function () {
      this.$router.push({name: 'SelectedProfile', params: { userId: this.review.user }})
    }, 
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    showReviewDetail: function () {
      axios({
        url: 'http://127.0.0.1:8000/movies/community/' + this.$route.params.reviewId,
        method: 'get',
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
        this.review = res.data
        this.comments = res.data.comment_set
        axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/find/${this.review.user}/`,
        headers: this.setToken(),
       })
        .then(res => {
        this.username = res.data.username
      })
      .catch(err => {
        console.log(err)
      })  
      })
    },
    deleteReview: function () {
      axios({
        url: 'http://127.0.0.1:8000/movies/community/' + this.$route.params.reviewId +'/'+ this.review.review_score + '/',
        method: 'delete',
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.$router.push( {name: 'ReviewPage', params: {movieId: res.data.movie_id} })
        })
        .catch((err) => {
          console.log(err)
        })
    },

    // 이 리뷰를 중앙 저장소에 저장하겠다.
    updateReview: function () {
      this.$store.dispatch('updateReview', this.review)
      this.$router.push( {name: 'UpdateReview'})
    },
    
    createComment: function () {
      // 빈 값이 아니라면
      if (this.commentContent) {

        axios({
          method: 'post',
        url: 'http://127.0.0.1:8000/movies/community/'+ this.review.id +'/',
        data: {
        content: this.commentContent,
        },
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.showReviewDetail()
          // 빈 칸으로 만들기
          this.commentContent =""
        })
        .catch(err => {
          console.log(err)
        })
      }
    },
  },
  computed: {
    requestUser: function () {
      return this.$store.state.userinfo
    }
  },
  created: function () {
    this.showReviewDetail()
    this.$store.dispatch('reviewDetailGuide')
  },
}
</script>

<style>

.writer:hover {
  border: 2px solid #00e054;
  cursor: pointer;
}
</style>