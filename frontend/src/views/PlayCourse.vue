<template>
  <div>
    <b-row>
      <b-col class="border-1 col-4">
        <b-list-group class="m-3 border-1">
          <b-list-group-item
            no-body
            v-for="(chapter, index) in chapters"
            :key="chapter.id"
            class="my-0 py-0 px-0">
            <div
              class="d-flex w-100 justify-content-between py-2 mx-0 px-3 chapter text-secondary"
              @click="toggleVisible(index)"
            >
              <h5 class="my-1 border-0 text-secondary">
                <i class="mr-3">{{ index+ 1 }}</i>
                {{ chapter.title }}
              </h5>
              <a-icon :type="arrow[index]" class="mt-2 mr-3"></a-icon>
            </div>
            <div class="mt-2 px-3" v-show="show[index]">
              <b-list-group class="m-0">
                <b-list-group-item
                  v-for="(video, vIndex) in chapter.videos"
                  :key="video.id"
                  class="d-flex justify-content-between align-items-center border-0 p-1 video"
                  style="border-bottom:0"
                  @click="selectVideo(video.id)"
                >
                  <h6 class="text-success">
                    <i class="mr-1">{{ index + 1 }}.{{ vIndex + 1 }}</i>
                    {{ video.title }}
                  </h6>
                  <a-icon type="play-circle" class="text-success"></a-icon>
                </b-list-group-item>
              </b-list-group>
            </div>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col class="col-8">
        <video-player
          class="video-player-box my-3 border-1"
          ref="videoPlayer"
          :options="playerOptions"
        >
        </video-player>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import chapterApi from '@/api/ChapterApi'
import 'video.js/dist/video-js.css'
import { videoPlayer } from 'vue-video-player'

export default {
  components: {
    videoPlayer
  },
  data () {
    return {
      video_url: null,
      chapters: [],
      videos: [],
      show: [],
      arrow: [],
      thumbnail: null,
      queryParams: {
        courseId: this.$route.params.courseId
      },
      videoId: this.$route.params.videoId
    }
  },
  computed: {
    playerOptions: function () {
      return {
        muted: true,
        language: 'zh-CN',
        autoplay: false,
        playbackRates: [0.7, 1.0, 1.5, 2.0],
        width: '600px',
        height: '400px',
        sources: [{
          type: 'video/mp4',
          src: this.video_url
        }],
        poster: this.thumbnail
      }
    },
    player () {
      return this.$refs.videoPlayer.player
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.fetchChapters(to.params.courseId, to.params.videoId)
    })
  },
  methods: {
    selectVideo (videoId) {
      const video = this.videos.find(item => {
        return item.id === videoId
      })
      this.video_url = video.url
      this.thumbnail = video.thumbnail
    },
    fetchChapters (courseId, videoId) {
      chapterApi.getChaptersByCourseId({ 'courseId': courseId }).then(res => {
        this.chapters = res.data
        this.chapters.map((element, index) => {
          this.arrow[index] = 'down'
        })
        this.chapters.forEach(chapter => {
          this.videos.push(...chapter.videos)
        })
        if (videoId) {
          this.selectVideo(videoId)
        } else {
          this.video_url = this.videos[0].url
          this.thumbnail = this.videos[0].thumbnail
        }
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
  .video {
    cursor: pointer;
  }
</style>
