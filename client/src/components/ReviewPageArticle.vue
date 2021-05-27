<template>
<div>

  <!-- <div class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1 table-title" @click="showReviewDetail">{{ review.title }}</h5>
      <small class="table-writer" @click="goToProfile">{{ username }}</small>
    </div>
    <small>{{ format_date(review.created_at) }}</small>
  </div> -->
  
  
  <a href="#" class="list-group-item list-group-item-action" aria-current="true">
    <div class="d-flex w-100">
      <h5 class="mb-1 table-title" @click="showReviewDetail">제목: {{ review.title }}</h5>
    </div>
    <br>
    <div class="d-flex">
      <small class="table-writer me-3" @click="goToProfile">작성자: {{ username }}</small>
      <small>{{ format_date(review.created_at) }}</small>
    </div>
  </a>
</div>
</template>

<script>
import axios from "axios"
import moment from 'moment'


export default {
  name: 'ReviewPageArticle',
  data: function () {
    return {
      username: null
    }
  },
  props: {
    review: {
      type: Object
    }
  },
  methods: {
    format_date: function (value) {
        if (value) {
          return moment(String(value)).format('YYYY-MM-DD HH:mm')
        }
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    showReviewDetail: function () {
      this.$router.push({name: 'ReviewDetail', params: { reviewId: this.review.id}})
    },
    goToProfile:  function () {
      this.$router.push({name: 'SelectedProfile', params: { userId: this.review.user }})
    }, 
  },
  created: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/accounts/find/' + this.review.user + '/',
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
        this.username = res.data.username
      })
      .catch(err => {
        console.log(err)
      })
    },
}
</script>

<style scoped>

.table-title:hover {
  background: gold;
}

.table-title {
  cursor: pointer;
}

.table-writer:hover {
  background: gold;
}

.table-writer {
  cursor: pointer;
}

</style>