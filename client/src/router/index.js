import Vue from 'vue'
import VueRouter from 'vue-router'
import Movies from '@/views/movies/Movies.vue'
import MovieDetail  from '@/views/movies/MovieDetail.vue'
import ReviewPage from '@/views/movies/ReviewPage.vue'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import MyProfile from '@/views/accounts/MyProfile'
import SelectedProfile from '@/views/accounts/SelectedProfile'
import CreateReview from '@/views/movies/CreateReview.vue'
import ReviewDetail from '@/views/movies/ReviewDetail.vue'
import UpdateReview from '@/views/movies/UpdateReview.vue'
import SearchResult from '@/views/movies/SearchResult.vue'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Movies',
    component: Movies
  },
  {
    path: '/:movieId/',
    name: 'MovieDetail',
    component: MovieDetail
  },
  {
    path: '/:movieId/community/',
    name: 'ReviewPage',
    component: ReviewPage
  },
  {
    path: '/accounts/signup/',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login/:case',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/MyProfile/',
    name: 'MyProfile',
    component: MyProfile,
  },
  {
    path: '/accounts/Profile/:userId/',
    name: 'SelectedProfile',
    component: SelectedProfile,
  },
  {
    path: '/:movieId/reviews/',
    name: 'CreateReview',
    component: CreateReview,
  },
  {
    path: '/community/:reviewId/',
    name: 'ReviewDetail',
    component: ReviewDetail,
  },
  {
    path: '/community/:reviewId/update/',
    name: 'UpdateReview',
    component: UpdateReview,
  },
  {
    path: '/searchresult/:searchKeyword/',
    name: 'SearchResult',
    component: SearchResult,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
