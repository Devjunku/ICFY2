<template>
  <div class="container">
    <br>
    <h1>Signup</h1>
    <div class="input-group justify-content-center">
      <div class="mb-3">      
          <input type="text" class="form-control" id="username" v-model="username" placeholder="아이디를 입력하세요">
      </div>
    </div>
    <button class="btn btn-success mb-3 greenBtn" @click="checkId">아이디 중복 확인</button>
    <div v-if="this.username">
      <div v-if="unchecked" class="text-danger mb-2" v-text="checkText"></div>
      <div v-else class="text-success mb-2" v-text="checkText"></div>
    </div>
    <div class="input-group justify-content-center">
      <div class="mb-3">
        <input type="password" class="form-control" id="password" v-model="password" placeholder="비밀번호를 입력하세요">
      </div>
    </div>
    <div class="input-group justify-content-center">
      <div>
        <input type="password" class="form-control" id="passwordConfirmation" v-model="passwordConfirmation" placeholder="비밀번호를 재입력하세요">
      </div>
    </div>
    <div v-if="different" class="text-danger mt-3">두 비밀번호가 일치하지 않습니다.</div>
    <div class="mt-3">
      <button class="btn btn-warning yellowBtn" @click="signup">회원가입</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Signup',
  data: function () {
    return {
      username: null,
      password: null,
      passwordConfirmation: null,
      different: false,
      unchecked: true,
      checkText: "아이디 중복 확인이 되지 않았습니다.",
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
    storeUserInfo: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/profile/${this.username}/`,
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res.data)
        this.$store.dispatch('storeUserInfo', res.data)
      })
      .catch(err => {
        console.log(err)
      })
    },
    signup: function () {
      if (this.unchecked === false) {
        if (this.password === this.passwordConfirmation) {
          axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/accounts/signup/',
            data: {
              username: this.username,
              password: this.password,
              passwordConfirmation: this.passwordConfirmation,
            }
          })
            .then(res => {
              console.log(res)
              // 회원 가입 후 자동 로그인
              axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
                data: {
                  username: this.username,
                  password: this.password
                },
              })
                .then(res => {
                  localStorage.setItem('jwt', res.data.token)
                this.$store.dispatch('storeUsername', this.username)
                this.$emit('login')
                this.$router.push({ name: 'Movies' })
                this.storeUserInfo()
                })
                .catch(err => {
                  console.log(err)
                })
            })
            .catch(err => {
              console.log(err)
            })
          this.different = false
        }
        else {
          this.different = true
        }
      }
    },
    checkId: function () {
      this.unchecked = true
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/check/${this.username}/`,
      })
      .then(res => {
        console.log(res.data)
        // 아이디가 중복된다.
        this.checkText = "이미 존재하는 아이디입니다."
      })
      .catch(err => {
        console.log(err)
        // 404 에러가 나오면 중복된 아이디가 없는 것이다.
        this.unchecked = false
        this.checkText = "사용할 수 있는 아이디입니다."
      })
    },
  },
  // 입력이 바뀌면 바로 false로 만들기
  watch: {
    username: function () {
      this.unchecked = true
      this.checkText = "아이디 중복 확인이 되지 않았습니다."
    }
  }
}
</script>


<style>
.yellowBtn:hover {
  border: solid 2px goldenrod;
}

.greenBtn:hover {
  border: solid 1px #00e054;
}

</style>