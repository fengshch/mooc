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
          :dropdownStyle="{ maxHeight: '400px', overflow: 'auto' }"
          placeholder="请选择用户组"
          allowClear
          treeDefaultExpandAll
          :treeData="orgTreeData"
          v-decorator="[
            'organization_id',
            {
              rules: [{ required: true, message: '用户组不能为空'}]
            }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="登录名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="username"
          placeholder="请请输登录名"
          v-decorator="[
            'username',
            {
              rules: [{ required: true, message: '登录名不能为空'}]
            }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="用户名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="name"
          placeholder="请输入用户名"
          v-decorator="[
            'name',
            {
              rules: [{ required: true, message: '用户名不能为空'}]
            }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="邮箱"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
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
          name=""
          placeholder="请请输入用户电话"
          v-decorator="[
            'mobile_phone',
            {
              rules: [{ required: false }]
            }
          ]"/>
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
          <img
            v-if="user.avatar"
            :src="user.avatar"
            alt="avatar"
            style="width:80px; height:80px"
          />
          <div v-else>
            <a-icon :type="loading ? 'loading': 'plus'"/>
            <div class="ant-upload-text">上传</div>
          </div>
        </a-upload>
      </a-form-item>
      <a-form-item
        label="角色"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-checkbox-group
          name="roles"
          :options="rolesOptions"
          v-decorator="[
            'roles',
            {
              rules: [{ required: true, message: '请至少选择一个角色' }]
            }
          ]"
        />
      </a-form-item>
      <a-col :span="24" :style="{ textAlign: 'left' }">
        <a-button type="primary" html-type="submit">
          保存
        </a-button>
        <a-button type="primary" :style="{ marginLeft: '24px'}" @click="handleNew">
          新增
        </a-button>
      </a-col>
    </a-form>
  </a-card>
</template>

<script>
import organizationApi from '@/api/OrganizationApi'
import userApi from '@/api/UserApi'

import { mapActions } from 'vuex'

export default {
  data () {
    return {
      orgTreeData: [],
      form: this.$form.createForm(this),
      loading: false,
      incidents: null,
      user: {},
      rolesOptions: [
        { label: '系统管理员', value: 'system' },
        { label: '课程管理员', value: 'manager' },
        { label: '普通用户', value: 'user' }
      ],
      userId: null
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadOrgData()
      if (to.params.userId) {
        vm.userId = to.params.userId
      }
      vm.loadUser()
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadOrgData () {
      organizationApi
        .getOrgTree()
        .then(res => {
          this.orgTreeData = []
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
    loadUser () {
      this.user = {}
      if (this.userId && this.userId !== 'new') {
        userApi.getUserById(this.userId).then(res => {
          this.user = Object.assign({}, res.data)
          this.form.setFieldsValue({
            organization_id: '' + this.user.organization_id,
            username: this.user.username,
            name: this.user.name,
            email: this.user.email,
            mobile_phone: this.user.mobile_phone,
            roles: this.user.roles
          })
          // this.form = this.$form.createFormField(this, {
          //   'username': this.user.username
          // })
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.form = this.$form.createForm(this)
      }
    },
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.organization_id = parseInt(values.organization_id)
          this.user = Object.assign(this.user, values)
          if (!this.user.id) {
            this.addNewUser(this.user)
          } else {
            this.updateUser(this.user)
          }
        }
      })
    },
    handleUpload (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
      // Get this url from response in real world.
        this.user.avatar = info.file.response.file.url
        this.loading = false
        // getBase64(info.file.originFileObj, imageUrl => {
        // this.form.cover =
        // this.loading = false
        // })
      }
    },
    addNewUser (user) {
      userApi.addUser(user).then(res => {
        this.form = Object.assign(this.form, res.data)
        this.userId = res.data.id
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
    updateUser (user) {
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
    handleNew () {
      this.userId = null
      this.loadUser()
    }
  },
  clear () {
    this.$refs.editor.clear()
  }
}
</script>

<style>
  .avatar-uploader > .ant-upload {
    width: 80px;
    height: 80px;
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
