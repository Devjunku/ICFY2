<template>
  <div v-if="movie">
    <br>
    <p class="fw-bold">{{ movie.title }}</p>
    <figure class="figure me-4">
      <img class="rounded" :src="moviePosterPath" alt="poster">
      <div class="justify-content-center">
        <div class="container col-6">
          <br>
          <div>
            <p style="text-align:justify; box-sizing: border-box;">{{ movie.overview }}</p>
          </div>
        </div>
      </div>
    </figure>
    <div class="text-warning">
      평점: {{ movie.vote_average }} / 참여자 수 : {{ movie.vote_count }}
    </div>
    <span class="d-flex justify-content-center">
      <div class="p-2">
        <p>{{ similarity.similar }}</p>
      </div>
      <div class="p-2">
        <i :class="heartClass" @click="toggleHeart"></i>
      </div>
    </span>
    <div class="m-4">
      <button class="btn btn-warning reviewBtn" @click="goToReview">리뷰보기</button>
    </div>
    
    <div class="mb-3">
      <a :href="'https://www.justwatch.com/kr/검색?q='+movie.title" target="_blank">
        <button class="btn btn-light watchBtn">어디서 볼 수 있나요?</button>
      </a>
    </div>
    <div>
      <a :href="'https://www.youtube.com/results?search_query='+movie.title" target="_blank">
        <button class="btn btn-danger youtubeBtn">관련된 유튜브 동영상 보기</button>
      </a>
    </div>
    <br>
    <hr>
    <p> 이 영화는 어떠신가요? </p>
    <div class="container">
      <div v-if="posterMode" class="row row-cols-1 row-cols-md-6 g-4">
        <MoviesList
          v-for="(movie, idx) in recommend_movies" 
          :key="idx+'a'"
          :movie="movie"
        />
      </div>
      <div v-else>
        <MoviesArticle
          v-for="(movie, idx) in recommend_movies" 
          :key="idx+'b'"
          :movie="movie"
        />  
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MoviesList from '@/components/MoviesList'
import MoviesArticle from '@/components/MoviesArticle'
export default {
  name: 'MovieDetail',
  components: {
    MoviesList,
    MoviesArticle
  },
  data: function () {
    return {
      movie: null,
      moviePosterPath: null,
      heartClass: "far fa-2x fa-heart heart",
      recommend_movies: [],
      similarity: null,
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
    showMovieDetail: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/' + this.$route.params.movieId,
        headers: this.setToken(),
      })
      .then(res => {
        // console.log(res)
        this.movie = res.data
        this.moviePosterPath = `https://image.tmdb.org/t/p/w500${this.movie.poster_path}`
      })
      .catch(err => {
        console.log(err)
        // 도움말에 적기
        this.$router.push({name: 'Login', params: { case: 1}})
      })
    },
    goToReview: function () {
      this.$router.push({name: 'ReviewPage', params: { movieId: this.movie.id}})
    },
    toggleHeart:  function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/like/' + this.$route.params.movieId +'/',
        headers: this.setToken(),
      })
      .then(res => {
        if ( res.data.flag === 1) {
          this.heartClass = "fas fa-2x fa-heart heart"
        } else {
          this.heartClass = "far fa-2x fa-heart heart"
        }
        this.movie.vote_count = res.data.vote_count
        this.similarIdx()
      })
      .catch(err => {
        console.log(err)
      })
    },
    recommend: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.$route.params.movieId}/recommend`,
      })
      .then(res => {
        // console.log(res)
        this.recommend_movies = res.data
      })
      .catch(err => {
        console.log(err)
      })
    },
    similarIdx: function () {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.$route.params.movieId}/similarity/`,
        data: this.$store.state.userinfo,
        headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
        this.similarity = res.data
      })
      .catch(err => {
        console.log(err)
      })
    },
    // 하트가 체크되었는지 확인하기
    checkHeart: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/checkheart/' + this.$route.params.movieId +'/',
        headers: this.setToken(),
      })
      .then(res => {
        // 좋아요가 있다면
        if ( res.data.flag === 1) {
          this.heartClass = "fas fa-2x fa-heart heart"
        } else {
          this.heartClass = "far fa-2x fa-heart heart"
        }
      })
      .catch(err => {
        console.log(err)
      })
    },
  },
  computed: {
    posterMode: function () {
      return this.$store.state.posterMode
    },
    signal: function () {
      return this.$route.params.movieId
    }
  },
  watch: {
    signal: function () {
      this.showMovieDetail()
      this.recommend()
      this.similarIdx()
      this.$store.dispatch('movieDetailGuide')
      this.checkHeart()
      // 이렇게 하면 클릭한 위치에 화면이 있어서 올려야 한다.
      window.scrollTo(0,0) 
    }
  },
  created: function () {
    this.showMovieDetail()
    this.recommend()
    this.similarIdx()
    this.$store.dispatch('movieDetailGuide')
    this.checkHeart()
  },
}
</script>

<style scoped>
.heart {
  color: crimson;
}

.watchBtn {
  color:white;
  background-color: rebeccapurple;
  border: black;
}

.watchBtn:hover {
  border: solid 1px #e000c2;
}

.reviewBtn {
  font-weight: 700;
}


</style>
