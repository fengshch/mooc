<template>
  <a-card :bordered="false">
    <a-form :form="form" @submit="handleSubmit">
      <a-form-item
        label="用户组名称"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.name"
          name="name"
          placeholder="请输入用户组名称"
        />
      </a-form-item>
      <a-form-item
        label="全名"
        :labelCol="{lg: {span: 2}, sm: {span: 2}}"
        :wrapperCol="{lg: {span: 10}, sm: {span: 10}}"
      >
        <a-input
          v-model="form.fullname"
          name="name"
          placeholder="请输入命名"
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
            增加
          </a-button>
        </a-form-item>
      </b-row>
    </a-form>
  </a-card>
</template>

<script>
import organizationApi from '@/api/OrganizationApi'
import { mapActions } from 'vuex'

const defaultForm = {
  name: '',
  fullname: ''
}
export default {
  data () {
    return {
      form: Object.assign({}, defaultForm),
      parentId: null,
      userGroup: {}
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => vm.loadUserGroup(to.params.groupId, to.params.parentId))
  },
  methods: {
    ...mapActions(['showAlert']),
    loadUserGroup (groupId, parentId) {
      if (groupId && groupId !== 'new') {
        organizationApi.getOrganization(groupId).then(res => {
          this.form = Object.assign({}, res.data)
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.parentId = parentId
        console.log(parentId)
        this.continueAdd()
      }
    },
    handleSubmit (e) {
      e.preventDefault()
      if (!this.form.id) {
        this.addNewUserGroup()
      } else {
        this.updateUserGroup()
      }
    },
    addNewUserGroup () {
      const newUserGroup = Object.assign({}, this.form)
      newUserGroup.parent_id = this.parentId
      organizationApi.addOrganization(newUserGroup).then(res => {
        this.form = Object.assign(this.form, res.data)
        // this.$router.replace({
        //   params: {
        //     groupId: res.data.id,
        //     parent_id: res.data.parent_id
        //   }
        // })
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
    updateUserGroup () {
      const userGroup = Object.assign({}, this.form)
      organizationApi.updateOrganization(userGroup).then(res => {
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
