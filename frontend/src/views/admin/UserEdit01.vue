<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="用户组"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-tree-select
          showSearch
          style="width: 300px"
          v-model="form.organization_id"
          :dropdownStyle="{ maxHeight: '400px', overflow: 'auto' }"
          placeholder="请选择用户组"
          allowClear
          treeDefaultExpandAll
          :treeData="orgTreeData"
        />
      </a-form-item>
      <a-form-item
        label="登录名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.username"
          name="username"
          placeholder="请请输登录名"
        />
      </a-form-item>
      <a-form-item
        label="用户名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.fullname"
          name="fullname"
          placeholder="请请输入用户名"
        />
      </a-form-item>
      <a-form-item
        label="邮箱"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.email"
          name="email"
          placeholder="请请输入用户邮箱"
          v-decorator="[
            'email',
            {
              rules: [
                {
                  type: 'email',
                  message: '请输入有效的邮箱地址'
                }
              ]
            }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="电话"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.mobil_phone"
          name=""
          placeholder="请请输入用户电话"
        />
      </a-form-item>
      <a-form-item
        label="图像"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-upload
          name="avatar"
          listType="picture-card"
          class="avatar-uploader"
          action="/api/upload/avatar"
          :showUploadList="false"
          @change="handleUpload"
        >
          <img v-if="form.avatar" :src="form.avatar" alt="avatar" style="width:300px; height:200px"/>
          <div v-else>
            <a-icon :type="loading ? 'loading': 'plus'"/>
            <div class="ant-upload-text">上传</div>
          </div>
        </a-upload>
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
import organizationApi from '@/api/OrganizationApi'
import userApi from '@/api/UserApi'

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
  data () {
    return {
      orgTreeData: [],
      form: this.$form.createForm(this),
      // form: Object.assign({}, defaultForm),
      value: undefined,
      loading: false,
      replaceFields: {
        title: 'name',
        key: 'id'
      }
    }
  },
  computed: {
    courseId () {
      return this.$route.params.courseId
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadOrgData()
      vm.loadUser(to.params.userId)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadOrgData () {
      organizationApi
        .getOrgTree()
        .then(res => {
          res.data.map(org => this.orgTreeData.push(this.transferOrgToNode(org)))
        })
        .catch(error => {
          console.log(error)
        })
    },
    transferOrgToNode (org) {
      const node = { 'key': org.id, 'value': '' + org.id, 'label': org.name, children: [] }
      org.children.map(item => node.children.push(this.transferOrgToNode(item)))
      return node
    },
    loadUser (userId) {
      if (userId && userId !== 'new') {
        userApi.getUserById(userId).then(res => {
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
        this.addNewCourse()
      } else {
        this.updateCourse()
      }
    },
    handleUpload (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
      // Get this url from response in real world.
        console.log(info)
        this.form.avatar = info.file.response.file.url
        this.loading = false
        // getBase64(info.file.originFileObj, imageUrl => {
        // this.form.cover =
        // this.loading = false
        // })
      }
    },
    addNewUser () {
      const newUser = Object.assign({}, this.form)
      userApi.addUser(newUser).then(res => {
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
    updateUser () {
      const user = Object.assign({}, this.form)
      userApi.updateUser(user).then(res => {
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
