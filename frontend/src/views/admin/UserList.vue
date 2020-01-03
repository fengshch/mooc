<template>
  <a-card :bordered="false">
    <a-col :span="24" :style="{ marginBottom: '18px'}">
      <a-button type="primary" icon="plus" @click="handleNew()" :style="{ marginRight: '40px' }">新建</a-button>
      是否显示子机构用户:
      <a-switch defaultChecked checkedChildren="显示" v-model="queryParam.showGrand" unCheckedChildren="不显示" @change="onSwitchChange"/>
    </a-col>
    <a-row :gutter="8" style="display:flex">
      <a-col :span="5" class="custom-tree">
        <a-directory-tree
          ref="userGroup"
          :defaultExpandAll="true"
          :treeData="orgTreeData"
          @select="onSelect"
          :replaceFields="replaceFields"
        />
      </a-col>
      <a-col :span="19">
        <a-table :columns="columns" :dataSource="userData" rowKey="id" :pagination="pagination" :bordered="true">
          <template slot="avatar" slot-scope="value">
            <img :src="value" style="width: 40px; height:40px" />
          </template>
          <template slot="roles" slot-scope="value">
            <a-checkbox-group :options="value" :value="value"/>
          </template>
          <template slot="operation" slot-scope="text,record">
            <span>
              <a @click="handleEdit(record)">
                编辑
              </a>
              <a-divider type="vertical"/>
              <a @click="handleResetPassword(record)">
                重置密码
              </a>
              <a-divider type="vertical"/>
              <a-popconfirm
                title="确定要删除吗？"
                @confirm="handleDel(record)">
                <a>删除</a>
              </a-popconfirm>
            </span>
          </template>
        </a-table>
      </a-col>
    </a-row>
  </a-card>
</template>
<script>
import UserGroupTree from '@/components/Tree/UserGroupTree'
import organizationApi from '@/api/OrganizationApi'
import userApi from '@/api/UserApi'
import { Icon } from 'ant-design-vue'
import { mapActions } from 'vuex'

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1511545_tdkl3xmtms.js'
})
const columns = [
  {
    title: '序号',
    dataIndex: 'no',
    width: '60px'
  }, {
    title: '登录名',
    dataIndex: 'username',
    width: '80px'
  }, {
    title: '用户名',
    dataIndex: 'name',
    width: '120px'
  }, {
    title: '电话',
    dataIndex: 'mobile_phone'
  }, {
    title: '邮箱',
    dataIndex: 'email'
  }, {
    title: '图像',
    dataIndex: 'avatar',
    scopedSlots: { customRender: 'avatar' }
  }, {
    title: '用户组',
    dataIndex: 'roles',
    scopedSlots: { customRender: 'roles' }
  }, {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    width: '400px',
    align: 'center',
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  components: {
    UserGroupTree,
    IconFont
  },
  data () {
    return {
      orgTreeData: [],
      replaceFields: {
        title: 'name',
        key: 'id'
      },
      columns,
      userData: [],
      pagination: {
        pageSizeOptions: ['10', '20', '30', '40', '50'],
        hideOnSinglePage: false,
        defaultCurrent: 1,
        defaltPageSize: 10,
        showSizeChanger: true,
        showQuickJumper: false,
        pageSize: 10,
        total: 0,
        onChange: pageNo => {
          this.queryParam.pageNo = pageNo
          this.loadUserData(this.queryParam)
        },
        onShowSizeChange: (current, pageSize) => {
          console.log(pageSize)
          this.pagination.pageSize = pageSize
          this.queryParam.pageSize = this.pagination.pageSize
          this.loadUserData(this.queryParam)
        }
      },
      queryParam: {
        orgId: 0,
        pageNo: 1,
        pageSize: 10,
        showGrand: true
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadTreeData()
      vm.loadUserData(vm.queryParam)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    onSelect (selectKeys, info) {
      this.queryParam.orgId = selectKeys[0]
      this.queryParam.pageNo = 1
      this.loadUserData(this.queryParam)
    },
    onCheck (checkedKeys, info) {
      console.log('onCheck', checkedKeys, info)
    },
    loadTreeData () {
      organizationApi
        .getOrgTree()
        .then(res => {
          this.orgTreeData = res.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    loadUserData (queryParam) {
      userApi.getUsersByOrgId(queryParam).then(res => {
        this.pagination.current = res.pageNo
        this.pagination.pageSize = res.pageSize
        this.pagination.total = res.totalCount
        this.userData = res.data
        this.userData.forEach((value, index) => {
          value.no = (res.pageNo - 1) * res.pageSize + index + 1
        })
      })
    },
    handleNew () {
      this.$router.push({ name: 'UserEditAdmin', params: { userId: 'new' } })
    },
    handleEdit (record) {
      this.$router.push({ name: 'UserEditAdmin', params: { userId: record.id } })
    },
    handleDel (record) {
      userApi.deleteUser(record.id).then(res => {
        this.loadUserData(this.queryParam)
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      })
    },
    onSwitchChange () {
      this.loadUserData(this.queryParam)
    },
    handleResetPassword (record) {
      userApi.resetPassword(record.id).then(res => {
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      }).catch(error => {
        this.showAlert({
          'type': 'success',
          'messsage': error.messsage
        })
      })
    }
  }
}
</script>

<style lang="less">
.custom-tree {
  border:solid 20px;
  border-color: #fafafa;
  // background-color: #fafafa
}
</style>
