<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="课程分类名称"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.name"
          name="name"
          placeholder="请输入课程分类名称"
        />
      </a-form-item>
      <b-row>
        <a-form-item :wrapper-col="{span: 12, offset: 5}">
          <a-button type="primary" html-type="submit">
            保存
          </a-button>
        </a-form-item>
        <a-form-item :wrapper-col="{span: 12, offset: 20}">
          <a-button type="primary" @click="continueAdd">
            继续增加
          </a-button>
        </a-form-item>
      </b-row>
    </a-form>
  </a-card>
</template>

<script>
import categoryApi from '@/api/CategoryApi'
import { mapActions } from 'vuex'

const defaultForm = {
  name: ''
}
export default {
  data () {
    return {
      form: Object.assign({}, defaultForm),
      category: {}
    }
  },
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => vm.loadCategory(to.params.categoryId))
  },
  methods: {
    ...mapActions(['showAlert']),
    loadCategory (categoryId) {
      if (categoryId && categoryId !== 'new') {
        categoryApi.getCategoryById(categoryId).then(res => {
          this.form = Object.assign({}, res.data)
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
        this.addNewCategory()
      } else {
        this.updateCategory()
      }
    },
    addNewCategory () {
      const newCategory = Object.assign({}, this.form)
      categoryApi.addCategory(newCategory).then(res => {
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
    updateCategory () {
      const category = Object.assign({}, this.form)
      categoryApi.updateCategory(category).then(res => {
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
    continueAdd () {
      this.form = Object.assign({}, defaultForm)
    }
  },
  clear () {
    this.$refs.editor.clear()
  }
}
</script>

<style lang="less">
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
