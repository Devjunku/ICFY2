<template>
  <div class="container">
    <br>
    <br>
    <div class="d-flex">
      <button class="btn btn-warning" @click="goBack"> 영화 정보 </button>
    </div>
    <h1 class="d-flex justify-content-center my-5">Community</h1>
    <div class="row">
      <!-- Board -->
      <section class="col-12 col-lg-12 ps-4">
        <div class="d-none d-lg-block">
          <table class="table">
            <thead>
            <tr class="table-light">
              <th scope="col">글 제목</th>
              <th scope="col">작성자</th>
              <th scope="col">작성 시간</th>
            </tr>
            </thead>
            <tbody>
            <ReviewPageItem
              v-for="(review, idx) in reviews" 
              :key="idx+'a'"
              :review="review"
            />  
            </tbody>
          </table>
        </div>
      
        <div class="d-lg-none mt-5 me-3">
          <article>
            <div class="list-group">
              <ReviewPageArticle
              v-for="(review, idx) in reviews" 
              :key="idx+'b'"
              :review="review"
              />  
            </div>
          </article>
        </div>

      </section>        
    </div>
    <button class="btn btn-warning mt-3" @click="goWriteReview">리뷰 쓰기</button>
  </div>


</template>

<script>
import axios from 'axios'

import ReviewPageItem from '@/components/ReviewPageItem'
import ReviewPageArticle from '@/components/ReviewPageArticle'


export default {
  name: 'ReviewPage',
  components: {
    ReviewPageItem,
    ReviewPageArticle
  },
  data: function () {
    return {
      reviews: null,
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
    goBack: function () {
      this.$router.push({name: 'MovieDetail', params: { movieId: this.$route.params.movieId }})
    },
    requestReviews: function () {
      axios({
        url: 'http://127.0.0.1:8000/movies/' + this.$route.params.movieId +'/community/',
        method: 'get',
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
        this.reviews = res.data
      })
      .catch(err => {
          console.log(err)
          this.$router.push({name: 'Login' , params: { case: 1}})
        })
    },
    goWriteReview: function () {
      this.$router.push({name: 'CreateReview', params: { movieId: this.$route.params.movieId }})
    },
  },
  created: function () {
    this.requestReviews()
    this.$store.dispatch('reviewPageGuide')
  },

}
</script>

<style>

</style>