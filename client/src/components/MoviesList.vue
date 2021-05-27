<template>
  <div class="col">
    <div class="card h-50 border border-dark" @click="showMovieDetail">
      <img :src="moviePosterPath" class="card-img-top rounded" alt="movie">
    </div>
  </div>
</template>


<script>
export default {
  name: 'MoviesList',
  props: {
    movie: {
      type: Object
    }
  },
  methods: {
    showMovieDetail: function () {
      // console.log(this.movie)
      this.$router.push({name: 'MovieDetail', params: { movieId: this.movie.id}})
    },
  },
  computed: {
    moviePosterPath: function () {
      return `https://image.tmdb.org/t/p/w500${this.movie.poster_path}`
    },
  },
}
</script>

<style scoped>
img:hover {
  border: 2px solid #00e054;
}
</style>