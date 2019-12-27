<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="章节标题"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.title"
          name="title"
          placeholder="请输入章节标题"
        />
      </a-form-item>
      <a-form-item :wrapper-col="{span: 12, offset: 5}">
        <a-button type="primary" html-type="submit">
          保存
        </a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script>
import chapterApi from '@/api/ChapterApi'
import { mapActions } from 'vuex'

const defaultForm = {
  title: '',
  videos: []
}
export default {
  data () {
    return {
      // form: this.$form.createForm(this),
      form: Object.assign({}, defaultForm)
    }
  },
  computed: {
    chapterId () {
      return this.$route.params.chapterId
    },
    courseId () {
      return this.$route.params.courseId
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadChapter(to.params.chapterId)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadChapter (chapterId) {
      if (chapterId && chapterId !== 'new') {
        chapterApi.getChapterById(chapterId).then(res => {
          this.form = Object.assign({}, res.data)
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.handleAdd()
      }
    },
    handleSubmit (e) {
      e.preventDefault()
      if (!this.form.id) {
        this.addChapter()
      } else {
        this.updateChapter()
      }
    },
    addChapter () {
      const newChapter = Object.assign({}, this.form)
      newChapter.course_id = parseInt(this.courseId)
      console.log(newChapter)
      chapterApi.addChapter(newChapter).then(res => {
        console.log(res)
        this.form = Object.assign(this.form, res.data)
        this.showAlert({
          'show': true,
          'type': 'success',
          'message': res.message
        }).catch(err => {
          this.showAlert({
            'show': true,
            'type': 'error',
            'message': err.message
          })
        })
      })
    },
    updateChapter () {
      const chapter = Object.assign({}, this.form)
      chapterApi.updateChapter(chapter).then(res => {
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
    handleAdd () {
      this.form = Object.assign({}, defaultForm)
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
