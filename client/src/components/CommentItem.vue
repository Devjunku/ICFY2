<template>
  <div>
    <div v-if="isClicked">
      <label class="text-warning fw-bold me-3" for="content">댓글 내용: </label>
      <input type="text" id="content" v-model="newComment" @keyup.enter="updateComment">
      <button class="btn btn-warning btn-sm ms-3" @click="updateComment">댓글 저장</button>
    </div>
    <div v-else>
      <span class="text-warning fs-5 fw-bold user-name" @click="goToProfile">{{ username }} </span>
      <span class="fx-5 fw-bold mx-1"> : </span>
      <span class="text-warning fs-5 fw-bold">{{ comment.content }}</span>
      <div class="d-flex flex-row-reverse">
      <button class="btn btn-danger btn-sm" v-if="requestUser.id === comment.user" @click="deleteComment">댓글 삭제</button> 
      <button class="btn btn-warning btn-sm me-3" v-if="requestUser.id === comment.user" @click="makeInput">댓글 수정</button>
      </div>
    </div>
      
      <div class="d-flex flex-row-reverse">
        <div>작성 시간: {{ format_date(comment.created_at) }}</div>
      </div>
        <!--수정되었을 경우에만 수정 시간을 보여준다. -->
      <div class="d-flex flex-row-reverse">
        <div v-if="comment.created_at !== comment.updated_at">수정 시간: {{ format_date(comment.updated_at) }}</div>
        <div v-else> [수정되지 않은 댓글] </div>
      </div>
      <hr>
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'


export default {
  name: 'CommentItem',
  data: function () {
    return {
      isClicked: false,
      newComment: this.comment.content,
      username: null,
    }
  },
  props: {
    comment: {
      type: Object
    }
  },
  methods: {
    goToProfile:  function () {
      this.$router.push({name: 'SelectedProfile', params: { userId: this.comment.user }})
    }, 
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
    // updateComment: function () {
    
    // },
    deleteComment: function () {
      axios({
        url: 'http://127.0.0.1:8000/movies/comments/' + this.comment.id +'/',
        method: 'delete',
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.$emit('delete-comment')
        })
        .catch((err) => {
          console.log(err)
        })
    },
    makeInput: function () {
      this.isClicked= true
    },
    updateComment:  function () {
      axios({
        url: 'http://127.0.0.1:8000/movies/comments/' + this.comment.id +'/',
        method: 'put',
        data: {
          content: this.newComment
        },
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.$emit('update-comment')
          // 다시 댓글들이 보이도록
          this.isClicked= false
        })
        .catch((err) => {
          console.log(err)
        })
    },
    searchUserName: function() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/find/${this.comment.user}/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.username = res.data.username
      })
      .catch(err => {
        console.log(err)
      })  
    },
 
  },
  computed: {
    requestUser: function () {
      return this.$store.state.userinfo
    }
  },
  created: function () {
    this.searchUserName()
  }
}
</script>

<style>
.user-name:hover {
  border: 2px solid #00e054;
}

.user-name {
  cursor: pointer;
}

</style>