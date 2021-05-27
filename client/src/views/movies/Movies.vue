<template >
<div class="bg-dark.bg-gradient">
  <br>
  <div class="container">
    <div v-if="posterMode" class="row row-cols-1 row-cols-md-6 g-4">
      <MoviesList
         v-for="(movie, idx) in movies" 
        :key="idx+'a'"
        :movie="movie"
      />  
    </div>
    <div v-else>
      <MoviesArticle
         v-for="(movie, idx) in processedMovies" 
        :key="idx+'b'"
        :movie="movie"
      />  
    </div>
  </div>
</div>
</template>

<script>
import MoviesList from '@/components/MoviesList'
import MoviesArticle from '@/components/MoviesArticle'


export default {
  name: 'Movies',
  components: {
    MoviesList,
    MoviesArticle
  },
  data: function () {
    return {
      processedMovies : null,
      i: 0,
      j: 10,
    }
  },
  methods: {
    checkScroll: function () {
      const {scrollTop, clientHeight, scrollHeight} = document.documentElement
      
      if (scrollHeight-scrollTop < clientHeight+400) {
        this.j = this.j + 10
        this.processedMovies = this.movies.slice(this.i, this.j)
      }
    }
  },
  computed: {
    movies: function () {
      return this.$store.state.movies
    },
    posterMode: function () {
      return this.$store.state.posterMode
    },
  },
  watch: {
    // 처음 영화 10개 나오도록
    movies: function () {
      this.processedMovies = this.movies.slice(this.i, this.j)
    },
  },

  mounted() {
    this.$store.dispatch('createMovies')
    this.$store.dispatch('mainGuide')
  },
  created () {
    window.addEventListener('scroll', this.checkScroll);
  },
  destroyed () {
    window.removeEventListener('scroll', this.checkScroll);
  }

}
</script>
