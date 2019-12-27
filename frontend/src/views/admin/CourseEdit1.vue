<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="课程标题"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.title"
          name="title"
          placeholder="请输入课程标题"
        />
      </a-form-item>
      <a-form-item
        label="封面"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-upload
          name="course_cover"
          listType="picture-card"
          class="avatar-uploader"
          action="/upload/course_cover"
          :showUploadList="false"
          :beforUpload="beforeUpload"
          @change="handleUpload"
        >
          <img v-if="form.cover" :src="form.cover" alt="avatar" style="width:300px; height:200px"/>
          <div v-else>
            <a-icon :type="loading ? 'loading': 'plus'"/>
            <div class="ant-upload-text">上传</div>
          </div>
        </a-upload>
      </a-form-item>
      <a-form-item
        label="分类"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}">
        <a-select v-model="form.category_id">
          <a-select-option v-for="c in categories" :key="c.id" :value="c.id">
            {{ c.name }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        label="课程简介"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-textarea
          v-model="form.intro"
          name="intro"
          placeholder="请输入课程简介"
          :rows="4"
        />
      </a-form-item>
      <a-form-item
        label="课程详情"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 20}, sm: {span: 20}}"
      >
        <quill-editor
          id="myQuillEditor"
          v-model="content">
        </quill-editor>
      </a-form-item>
      <a-form-item
        label="是否发布"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}">
        <a-switch
          v-model="form.published"
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
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor'
import courseApi from '@/api/CourseApi'
import categoryApi from '@/api/CategoryApi'
import { mapActions } from 'vuex'

const defaultForm = {
  title: '',
  categoryId: '',
  intro: '',
  content: '',
  published: false,
  publishedTime: null
}
export default {
  components: {
    quillEditor
  },
  data () {
    return {
      loading: false,
      msg: 'Welcome to Use Tinymce Editor',
      disabled: false,
      // form: this.$form.createForm(this),
      form: Object.assign({}, defaultForm),
      categories: [],
      content: ''
    }
  },
  computed: {
    courseId () {
      return this.$route.params.courseId
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadCategories()
      vm.loadCourse(to.params.courseId)
    })
  },
  mounted () {
  },
  methods: {
    ...mapActions(['showAlert']),
    loadCategories () {
      categoryApi.getCategories().then(res => {
        this.categories = res.data
      })
    },
    loadCourse (courseId) {
      if (courseId && courseId !== 'new') {
        courseApi.getCourseById(courseId).then(res => {
          this.form = Object.assign({}, res.data)
          this.content = res.data.content
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.continueAdd()
      }
    },
    handleSubmit (e) {
      e.preventDefault()
      if (!this.form.id) {
        this.addNewCourse()
      } else {
        this.updateCourse()
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
        console.log(info)
        this.form.cover = info.file.response.file.url
        this.loading = false
        // getBase64(info.file.originFileObj, imageUrl => {
        // this.form.cover =
        // this.loading = false
        // })
      }
    },
    addNewCourse () {
      const newCourse = Object.assign({}, this.form)
      courseApi.addCourse(newCourse).then(res => {
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
    updateCourse () {
      const course = Object.assign({}, this.form)
      delete course.category_name
      console.log(this.content)
      course.content = this.content
      courseApi.updateCourse(course).then(res => {
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
    continueAdd () {
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
