<template>
  <tr class="text-light">
    <td>{{ comment.content }}</td>
    <td class="table-title" @click="goToReview">{{ review_content }}</td>
    <td>{{ format_date(comment.created_at) }}</td>
  </tr>
</template>

<script>
import axios from "axios"
import moment from 'moment'

export default {
  name: 'ProfileComment',
  data: function () {
    return {
      review_content: null,
    }
  },
  props: {
    comment: {
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
    goToReview: function () {
      this.$router.push({name: 'ReviewDetail', params: {reviewId: this.comment.review}})
    }
  },
  created: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/community/${this.comment.review}/`,
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
        this.review_content=res.data.title
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