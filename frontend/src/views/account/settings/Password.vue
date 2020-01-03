<template>
  <div class="account-settings-info-view">
    <a-form :form="form" layout="vertical" @submit="handleSubmit">
      <a-form-item
        label="新密码"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="password"
          placeholder="请输入新密码"
          type="password"
          v-decorator="[
            'password',
            {
              rules: [{ required: true, message: '密码不能为空'}]
            }
          ]"
        />
      </a-form-item>
      <a-form-item
        label="再输一次"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          name="passwordAgain"
          placeholder="请再输一次新密码"
          type="password"
          v-decorator="[
            'passwordAgain',
            { rules: [{ required: true, message: '密码不能为空'}] }
          ]"
        />
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
      form: this.$form.createForm(this)
    }
  },
  computed: {
    ...mapGetters(['userId'])
  },
  methods: {
    ...mapActions(['showAlert']),
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (values.password !== values.passwordAgain) {
          this.showAlert({
            'type': 'error',
            'message': '两次输入的密码不一致'
          })
          return
        }
        if (!err) {
          this.updatePassword(this.userId, values.password)
        }
      })
    },
    updatePassword (userId, password) {
      userApi.updatePassword(userId, password).then(res => {
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
