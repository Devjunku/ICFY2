<template>
  <div class="bg-dark.bg-gradient">
    <br>
    <div class="container">
      <div class="row row-cols-1 row-cols-md-6 g-4">
        <MoviesList
          v-for="(movie, idx) in searchMovies" 
          :key="idx"
          :movie="movie"
        />  
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MoviesList from '@/components/MoviesList'

export default {
  name: 'SearchResult',
  components:{
    MoviesList,
  },
  data: function () {
    return {
      searchMovies: [],
    }
  },
  methods: {
    searchRes: function () {
      axios({
        method: 'get',
        url:  `http://127.0.0.1:8000/movies/search/?q=${this.$route.params.searchKeyword}`
      })
      .then(res => {
        console.log(res)
        this.searchMovies = res.data
      })
      .catch(err => {
          console.log(err)
      })
    }
  },
  created: function () {
    this.searchRes()
  },
  // created만 적으면 재검색을 했을 때 렌더링이 안 된다.
  computed: {
    url: function () {
      return `http://127.0.0.1:8000/movies/search/?q=${this.$route.params.searchKeyword}`
    }
  },
  watch: {
    url:  function () {
      this.searchRes()
    }
  }
}
</script>

<style>

</style>