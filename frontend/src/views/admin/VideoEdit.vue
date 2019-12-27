<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="视频标题"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.title"
          name="title"
          placeholder="请输入视频标题"
        />
      </a-form-item>
      <a-form-item
        label="视频"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-upload
          name="video"
          listType="picture-card"
          class="avatar-uploader"
          action="/api/upload/video"
          :showUploadList="false"
          :beforUpload="beforeUpload"
          @change="handleUpload"
        >
          <div style="position: relative">
            <img v-if="form.thumbnail" :src="form.thumbnail" alt="thumbnail" style="width:300px; height:200px"/>
            <div v-else>
              <a-icon v-show="!loading" type="plus"/>
              <div class="ant-upload-text">上传</div>
            </div>
            <a-icon
              v-show="loading"
              type="loading"
              style="position: absolute; margin:0 auto; left:0; right:0; text-align:center; top: 40%"/>
          </div>
        </a-upload>
      </a-form-item>
      <a-row>
        <a-col :span="24" :style="{ textAlign: 'left'}">
          <a-button type="primary" html-type="submit">
            保存
          </a-button>
          <a-button type="primary" @click="handleNew" :style="{ marginLeft: '20px'}">
            增加
          </a-button>
        </a-col>
      </a-row>
    </a-form>
  </a-card>
</template>

<script>
import videoApi from '@/api/VideoApi'
import { mapActions } from 'vuex'

const defaultForm = {
  title: '',
  chapter_id: '',
  thumbnail: '',
  url: ''
}
export default {
  data () {
    return {
      loading: false,
      // form: this.$form.createForm(this),
      form: Object.assign({}, defaultForm)
    }
  },
  computed: {
    chapterId () {
      return this.$route.params.chapterId
    },
    videoId () {
      return this.$route.params.videoId
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadVideo(to.params.videoId)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadVideo (videoId) {
      if (videoId && videoId !== 'new') {
        videoApi.getVideoById(videoId).then(res => {
          this.form = Object.assign({}, res.data)
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.handleNew()
      }
    },
    handleSubmit (e) {
      e.preventDefault()
      if (!this.form.id) {
        this.addNewVideo()
      } else {
        this.updateVideo()
      }
    },
    beforeUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      if (!isJPG) {
        this.$message.error('You can only upload JPG file!')
      }
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('Image must smaller than 2MB!')
      }
      return isJPG && isLt2M
    },
    handleUpload (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
      // Get this url from response in real world.
        this.form.thumbnail = info.file.response.data.thumbnail
        this.form.url = info.file.response.data.url
        this.loading = false
        this.showAlert({
          'show': true,
          'type': 'success',
          'message': '上传视频成功'
        })
        // getBase64(info.file.originFileObj, imageUrl => {
        // this.form.cover =
        // })
      }
    },
    addNewVideo () {
      const newVideo = Object.assign({}, this.form)
      newVideo.chapter_id = parseInt(this.chapterId)
      videoApi.addVideo(newVideo).then(res => {
        this.form = Object.assign(this.form, res.data)
        this.showAlert({
          'show': true,
          'type': 'success',
          'message': res.message
        })
      }).catch(err => {
        this.showAlert({
          'show': true,
          'type': 'error',
          'message': err.message
        })
      })
    },
    updateVideo () {
      const video = Object.assign({}, this.form)
      videoApi.updateVideo(video).then(res => {
        this.form = Object.assign(this.form, res.data)
        this.showAlert({
          'type': 'success',
          'message': res.message
        }).catch(err => {
          this.showAlert({
            'type': 'error',
            'message': err.message
          })
        })
      })
    },
    handleNew () {
      this.form = Object.assign({}, defaultForm)
      this.form.chapter_id = this.chapterId
    }
  },
  clear () {
    this.$refs.editor.clear()
  }
}
</script>

<style>
  .avatar-uploader > .ant-upload {
    width: 128px;
    height: 128px;
  }
  .ant-upload-select-picture-card i {
    font-size: 32px;
    color: #999;
  }

  .ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
  }
</style>
