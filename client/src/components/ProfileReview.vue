<template>
  <tr class="text-light">
    <td class="table-title" @click="showMovieDetail">{{ movie_title }}</td>
    <td class="table-title" @click="showReviewDetail">{{ review.title }}</td>
    <td >{{ review.review_score }}</td>
    <td>{{ format_date(review.created_at) }}</td>
  </tr>
</template>

<script>
import axios from "axios"
import moment from 'moment'


export default {
  name: 'ReviewPageItem',
  data: function () {
    return {
      movie_title: null
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
    showMovieDetail: function () {
      this.$router.push({name: 'MovieDetail', params: {movieId: this.review.movie}})
    }
  },
  created: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.review.movie}/`,
        headers: this.setToken(),
      })
      .then(res => {
        // console.log(res)
        this.movie_title = res.data.title
      })
      .catch(err => {
        console.log(err)
      })
    },
}
</script>

<style scoped>

.table-title:hover {
  border: 1.5px solid gold;
  color: gold;
}

.table-title {
  cursor: pointer;
}

.table-writer:hover {
  border: 1px solid gold;
}

.table-writer {
  cursor: pointer;
}

</style>