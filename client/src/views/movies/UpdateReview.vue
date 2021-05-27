<template>
   <div>
    <br>
    <h1>리뷰 수정</h1>
    <div>
      <br>
      <label for="title me-3">리뷰 제목</label>
    </div>
    <br>  
    <input v-if="review" type="text" id="title" size="60" v-model="review.title">
    <br>
    <br>
    <div>
      <label for="content">리뷰 내용</label>
    </div>
    <br>
    <div>
      <textarea v-model="review.content" cols="60" rows="10"></textarea>
    </div>
    <br>
    <div>
       <i v-if="value1" @click="star1" class="far fa-star fa-2x star"></i>
      <i v-else @click="star1" class="fas fa-star fa-2x star"></i>
      <i v-if="value2" @click="star2" class="far fa-star fa-2x star"></i>
      <i v-else @click="star2" class="fas fa-star fa-2x star"></i>
      <i v-if="value3" @click="star3" class="far fa-star fa-2x star"></i>
      <i v-else @click="star3" class="fas fa-star fa-2x star"></i>
      <i v-if="value4" @click="star4" class="far fa-star fa-2x star"></i>
      <i v-else @click="star4" class="fas fa-star fa-2x star"></i>
      <i v-if="value5" @click="star5" class="far fa-star fa-2x star me-2"></i>
      <i v-else @click="star5" class="fas fa-star fa-2x star me-2"></i>
      <i v-if="value6" @click="star6" class="far fa-star fa-2x star"></i>
      <i v-else @click="star6" class="fas fa-star fa-2x star"></i>
      <i v-if="value7" @click="star7" class="far fa-star fa-2x star"></i>
      <i v-else @click="star7" class="fas fa-star fa-2x star"></i>
      <i v-if="value8" @click="star8" class="far fa-star fa-2x star"></i>
      <i v-else @click="star8" class="fas fa-star fa-2x star"></i>
      <i v-if="value9" @click="star9" class="far fa-star fa-2x star"></i>
      <i v-else @click="star9" class="fas fa-star fa-2x star"></i>
      <i v-if="value10" @click="star10" class="far fa-star fa-2x star"></i>
      <i v-else @click="star10" class="fas fa-star fa-2x star"></i>
    </div>
    <br>
    <button class="btn btn-warning fw-bold" @click="submit">리뷰 수정</button>
  </div>
</template>


<script>
import axios from "axios"

export default {
  name: "UpdataReview",
  data: function () {
    return {
      // 평점 변경 시 기존 점수를 빼기 위해서
      storage: 0,
      reviewScore: 0,
      value1 : true,
      value2 : true,
      value3 : true,
      value4 : true,
      value5 : true,
      value6 : true,
      value7 : true,
      value8 : true,
      value9 : true,
      value10 : true,
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
    
    submit: function () {
      if (this.review.title && this.review.content) {

        axios({
        method: 'put',
        url: 'http://127.0.0.1:8000/movies/community/'+ this.$route.params.reviewId +'/',
        data: {
        title: this.review.title,
        content: this.review.content,
        review_score: this.reviewScore,
        storage: this.storage
        },
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.$router.push({ name: 'ReviewPage', params: { movieId: this.review.movie } })
        })
        .catch(err => {
          console.log(err)
        })
      }
    },
    star1: function () {
      if (this.value1 === true) {
        this.value1 = false
        this.reviewScore = 1
      } else {
        this.value1 = true
        this.reviewScore = 0
      }
      this.value2 = true
      this.value3 = true
      this.value4 = true
      this.value5 = true
      this.value6 = true
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star2: function () {
      if (this.value2 === true) {
        this.value1 = false
        this.value2 = false
        this.reviewScore = 2
      } else {
        this.value1 = true
        this.value2 = true
        this.reviewScore = 0
      }
      this.value3 = true
      this.value4 = true
      this.value5 = true
      this.value6 = true
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star3: function () {
      if (this.value3 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.reviewScore = 3

      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.reviewScore = 0
      }
      this.value4 = true
      this.value5 = true
      this.value6 = true
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star4: function () {
      if (this.value4 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.reviewScore = 4
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.reviewScore = 0
      }
      this.value5 = true
      this.value6 = true
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star5: function () {
      if (this.value5 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.reviewScore = 5
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.reviewScore = 0
      }
      this.value6 = true
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
     star6: function () {
      if (this.value6 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.value6 = false
        this.reviewScore = 6
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.value6 = true
        this.reviewScore = 0
      }
      this.value7 = true
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star7: function () {
      if (this.value7 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.value6 = false
        this.value7 = false
        this.reviewScore = 7
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.value6 = true
        this.value7 = true
        this.reviewScore = 0
      }
      this.value8 = true
      this.value9 = true
      this.value10 = true
    },
    star8: function () {
      if (this.value8 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.value6 = false
        this.value7 = false
        this.value8 = false
        this.reviewScore = 8
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.value6 = true
        this.value7 = true
        this.value8 = true
        this.reviewScore = 0
      }
      this.value9 = true
      this.value10 = true
    },
    star9: function () {
      if (this.value9 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.value6 = false
        this.value7 = false
        this.value8 = false
        this.value9 = false
        this.reviewScore = 9
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.value6 = true
        this.value7 = true
        this.value8 = true
        this.value9 = true
        this.reviewScore = 0
      }
      this.value10 = true
    },
    star10: function () {
      if (this.value10 === true) {
        this.value1 = false
        this.value2 = false
        this.value3 = false
        this.value4 = false
        this.value5 = false
        this.value6 = false
        this.value7 = false
        this.value8 = false
        this.value9 = false
        this.value10 = false
        this.reviewScore = 10
      } else {
        this.value1 = true
        this.value2 = true
        this.value3 = true
        this.value4 = true
        this.value5 = true
        this.value6 = true
        this.value7 = true
        this.value8 = true
        this.value9 = true
        this.value10 = true
        this.reviewScore = 0
      }
    },
  },
  computed: {
    review: function () {
      return this.$store.state.review
    }
  },
  created: function () {
    this.storage = this.review.review_score
    if (this.review.review_score === 1) {
      this.star1()
    } else if (this.review.review_score === 2) {
      this.star2()
    } else if (this.review.review_score === 3) {
      this.star3()
    } else if (this.review.review_score === 4) {
      this.star4()
    } else if (this.review.review_score === 5) {
      this.star5()
    } else if (this.review.review_score === 6) {
      this.star6()
    } else if (this.review.review_score === 7) {
      this.star7()
    } else if (this.review.review_score === 8) {
      this.star8()
    } else if (this.review.review_score === 9) {
      this.star9()
    } else if (this.review.review_score === 10) {
      this.star10()
    }
  }
}
</script>
<style scoped>
.star {
  color: gold;
}

</style>