<template>
  <section class="w-75 my-3 mx-auto" style="text-align:left">
    <b-card no-body class="p-3">
      <b-card-body class="py-0">
        <b-card-img
          :src="course.cover"
          :alt="course.title"
          left=true
          width="240px"
          height="180px"
          style="float:left"
          class="mr-4"/>
          <!-- style="width:240px; height:180px;max-height:180px; float:left"/> -->
        <b-card-title>{{ course.title }}</b-card-title>
        <p>{{ course.intro }} </p>
        <b-button style="position:absolute; bottom:1rem" variant="success">立即参与</b-button>
      </b-card-body>
    </b-card>
    <b-tabs class="mt-3">
      <b-tab title="课程详情" active>
        <article class="m-3 py-3">
          <h1 class="my-3 text-secondary">{{ course.title }}</h1>
          <p style="font-size: 1.1rem">{{ course.intro }}</p>
          <hr class="my-4"/>
          <p style="text-indent: 2rem" v-html="course.content"/>
        </article>
      </b-tab>
      <b-tab title="课程章节">
        <b-list-group class="m-3">
          <b-list-group-item no-body v-for="(chapter, index) in chapters" :key="chapter.id" class="my-1 py-1 border-0">
            <div class="d-flex w-100 border-bottom justify-content-between pb-1 chapter" @click="toggleVisible(index)">
              <h5 class="mb-1 text-secondary border-0">
                <i class="mr-3">{{ index+ 1 }}</i>
                {{ chapter.title }}
              </h5>
              <a-icon :type="arrow[index]" class="mt-2 mr-3"></a-icon>
            </div>
            <div class="mt-2" v-show="show[index]">
              <b-list-group class="m-0">
                <b-list-group-item
                  v-for="(video, vIndex) in chapter.videos"
                  :key="video.id"
                  class="d-flex justify-content-between align-items-center border-0 p-1"
                  style="border-bottom:0"
                  :to="{ name: 'playCourse', params: { courseId: courseId, videoId: video.id }}"
                >
                  <h6 class="text-secondary" >
                    <i class="mr-1">{{ index + 1 }}.{{ vIndex + 1 }}</i>
                    {{ video.title }}
                  </h6>
                  <a-icon type="play-circle"></a-icon>
                </b-list-group-item>
              </b-list-group>
            </div>
          </b-list-group-item>
        </b-list-group>
      </b-tab>
      <b-tab title="讨论">
        <p>I'm a disabled tab!</p>
      </b-tab>
    </b-tabs>
  </section>
</template>
<script>
import courseApi from '@/api/CourseApi'
import chapterApi from '@/api/ChapterApi'

export default {
  data () {
    return {
      course: {},
      chapters: {},
      queryParams: {
        courseId: 0,
        pageNo: 1,
        pageSize: 5
      },
      show: [],
      arrow: [],
      courseId: '',
      imageRoot: process.env.VUE_APP_IMAGE_ROOT
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      const courseId = parseInt(to.params.courseId)
      console.log(courseId)
      vm.loadData(courseId)
    })
  },
  watch: {
    $route (to, from) {
      if (to.name === 'CourseDetail') {
        const courseId = parseInt(to.params.courseId)
        this.loadData(courseId)
      }
    }
  },
  methods: {
    loadData (courseId) {
      this.courseId = this.$route.params.courseId
      courseApi.getCourseById(courseId).then(res => {
        this.course = res.data
        this.queryParams.courseId = res.data.id
        chapterApi.getChaptersByCourseId(this.queryParams).then(res2 => {
          this.chapters = res2.data
          this.chapters.map((element, index) => {
            this.arrow[index] = 'down'
          })
        })
      })
    },
    toggleVisible (index) {
      // this.$refs[chapterId].visible = !this.$refs[chapterId].visible
      // this.chapters[index].show = !this.chapters[index].show
      // console.log(this.$refs[chapterId])
      this.$set(this.show, index, !this.show[index])
      if (this.show[index]) {
        this.$set(this.arrow, index, 'up')
      } else {
        this.$set(this.arrow, index, 'down')
      }
    }
  }
}
</script>

<style scoped>
  .chapter {
    cursor: pointer;
  }
</style>
