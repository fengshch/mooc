<template>
  <div class="text-center">
    <b-list-group class="w-75 mx-auto my-3" >
      <h4 class="my-3" style="text-align:left" > {{ category.name }}</h4>
      <b-list-group-item class="flex-column" style="text-align:left" v-for="item in courseData" :key="item.id">
        <b-media>
          <template v-slot:aside>
            <router-link :to="{ name: 'CourseDetail', params: {courseId: item.id} }">
              <b-img :src="item.cover" fluid @click="showCourseDetail" style="width:200px; height:150px;"/>
            </router-link>
          </template>
          <h5 class="mt-0 mb-2">{{ item.title }}</h5>
          <p class="mb-0 mt-3 intro">
            {{ item.intro }}
          </p>
        </b-media>
      </b-list-group-item>
      <b-button v-show="showMore" variant="info" @click="more">更多</b-button>
    </b-list-group>
  </div>
</template>

<script>
import courseApi from '@/api/CourseApi'
import categoryApi from '../api/CategoryApi'
export default {
  data () {
    return {
      courseData: [],
      category: {},
      queryParams: {
        categoryId: null,
        pageNo: 1,
        pageSize: 5
      },
      totalCount: 0,
      imageRoot: process.env.VUE_APP_IMAGE_ROOT
    }
  },
  computed: {
    categoryId () {
      return parseInt(this.$$router.params.categoryId)
    },
    showMore () {
      return this.totalCount > this.queryParams.pageSize
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      const categoryId = parseInt(to.params.categoryId)
      vm.loadData(categoryId)
    })
  },
  watch: {
    $route (to, from) {
      if (to.name === 'Category') {
        const categoryId = parseInt(to.params.categoryId)
        this.loadData(categoryId)
      }
    }
  },
  methods: {
    loadData (categoryId) {
      categoryApi.getCategoryById(categoryId).then(res => {
        this.category = res.data
        this.queryParams.categoryId = categoryId
        console.log(this.queryParams.categoryId)
        courseApi.getCoursesByCategoryId(this.queryParams).then(res => {
          this.courseData = res.data
          this.totalCount = res.totalCount
        })
      }).catch(err => {
        console.log(err)
      })
    },
    more () {
      this.queryParams.pageSize += 5
      this.loadData(this.queryParams)
    },
    showCourseDetail () {
      this.$router.push({
        name: 'CourseDetail'
      })
    }
  }
}
</script>

<style scoped>
.intro {
  font-size: 0.8rem;
}
</style>
