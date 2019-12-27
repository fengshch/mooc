<template>
  <section style="text-align:left">
    <b-tabs content-class="mt-3 mx-1">
      <b-tab title="最新课程" active>
        <b-card-group deck class="mt-3">
          <router-link
            v-for="item in coursesData"
            :key="item.id"
            :to="{ name: 'CourseDetail', params: {courseId: item.id}}"
            class="course"
          >
            <b-card
              :title="item.title"
              img-alt="Image"
              img-top
              tag="article"
              class="m-4 card"
              title-tag="h6"
            >
              <b-card-img :src="item.cover" alt="item.title" top style="width:200px; height:150px;"/>
              <i class="intro">{{ item.intro }}</i>
            </b-card>
          </router-link>
        </b-card-group>
      </b-tab>
    </b-tabs>
  </section>
</template>

<script>
import coursesApi from '@/api/CourseApi'

export default {
  data () {
    return {
      coursesData: [],
      queryParams: {
        pageNo: 1,
        pageSize: 10
      },
      imageRoot: process.env.VUE_APP_IMAGE_ROOT
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => vm.loadData())
  },
  methods: {
    loadData () {
      coursesApi.getCourses(this.queryParams).then(res => {
        this.coursesData = res.data
      })
    }
  }
}
</script>

<style lang="less" scoped>
.intro {
  font-size: 0.8rem;
  font-style: normal
}
.card-deck .card {
  width: 240px;
  height:300px;
}
.course {
  &:hover {
    text-decoration: none
  }
}
</style>
