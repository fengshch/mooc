<template>
  <div class="account-settings-info-view">
    <a-form :form="form" layout="vertical" @submit="handleSubmit">
      <a-form-item
        label="登录名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="username"
          placeholder="请输入系统登录名"
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
            { rules: [{ required: true, message: '用户名不能为空'}] }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="电子邮箱"
        :required="false"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="email"
          placeholder="请请输入用户邮箱"
          v-decorator="[
            'email',
            { rules: [{ type: 'email', message: '请输入有效的邮箱地址' }] }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="联系电话"
        :required="false"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name=""
          placeholder="请请输入用户电话"
          v-decorator="[
            'mobile_phone',
            { rules: [{ required: false }] }
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
          <img v-if="user.avatar" :src="user.avatar" alt="avatar" style="width:80px; height:80px" />
          <div v-else>
            <a-icon :type="loading ? 'loading': 'plus'" />
            <div class="ant-upload-text">上传</div>
          </div>
        </a-upload>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">保存</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import userApi from '@/api/UserApi'

export default {
  data () {
    return {
      form: this.$form.createForm(this),
      loading: false,
      user: {}
    }
  },
  computed: {
    ...mapGetters(['userInfo'])
  },
  beforeRouteEnter (to, from, next) {
    next(vm => vm.loadUser())
  },
  methods: {
    ...mapActions(['GetInfo', 'showAlert']),
    loadUser () {
      this.user = this.userInfo
      this.form.setFieldsValue({
        username: this.userInfo.username,
        name: this.userInfo.name,
        email: this.userInfo.email,
        mobile_phone: this.userInfo.mobile_phone
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
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          var user = Object.assign(this.user, values)
          this.updateUser(user)
        }
      })
    },
    updateUser (user) {
      userApi.updateUser(user).then(res => {
        this.form = Object.assign(this.form, res.data)
        this.GetInfo()
        this.user = this.userInfo
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
    }
  }
}
</script>

<style lang="less" scoped>
.avatar-upload-wrapper {
  height: 200px;
  width: 100%;
}

.ant-upload-preview {
  position: relative;
  margin: 0 auto;
  width: 100%;
  max-width: 180px;
  border-radius: 50%;
  box-shadow: 0 0 4px #ccc;

  .upload-icon {
    position: absolute;
    top: 0;
    right: 10px;
    font-size: 1.4rem;
    padding: 0.5rem;
    background: rgba(222, 221, 221, 0.7);
    border-radius: 50%;
    border: 1px solid rgba(0, 0, 0, 0.2);
  }
  .mask {
    opacity: 0;
    position: absolute;
    background: rgba(0, 0, 0, 0.4);
    cursor: pointer;
    transition: opacity 0.4s;

    &:hover {
      opacity: 1;
    }

    i {
      font-size: 2rem;
      position: absolute;
      top: 50%;
      left: 50%;
      margin-left: -1rem;
      margin-top: -1rem;
      color: #d6d6d6;
    }
  }

  img,
  .mask {
    width: 100%;
    max-width: 180px;
    height: 100%;
    border-radius: 50%;
    overflow: hidden;
  }
}
</style>
