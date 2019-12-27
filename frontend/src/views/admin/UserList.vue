<template>
  <a-card :bordered="false">
    <a-row :gutter="8">
      <a-col :span="5">
        <a-tree :treeData="orgTreeData" :replaceFields="replaceFields" :showIcon="false" @select="onSelect"></a-tree>
      </a-col>
      <a-col :span="19">
        <a-table :columns="columns" :dataSource="userData" rowKey="id" :pagination="pagination">
          <template slot="avatar" slot-scope="value">
            <img :src="value" />
          </template>
        </a-table>
      </a-col>
    </a-row>
  </a-card>
</template>
<script>
import organizationApi from '@/api/OrginationApi'
import userApi from '@/api/UserApi'
const columns = [
  {
    title: '序号',
    dataIndex: 'no'
  }, {
    title: '登录名',
    dataIndex: 'username'
  }, {
    title: '用户名',
    dataIndex: 'name'
  }, {
    title: '电话',
    dataIndex: 'mobilePhone'
  }, {
    title: '邮箱',
    dataIndex: 'email'
  }, {
    title: '图像',
    dataIndex: 'avatar',
    scopedSlots: { customRender: 'avatar' }
  }, {
    title: '用户组',
    dataIndex: 'groupName'
  }, {
    title: '最近登录时间',
    dataIndex: 'lastLoginTime'
  }, {
    title: '最近登录IP',
    dataIndex: 'lastLoginIp'
  }
]

export default {
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
        pageSize: 10
      }
    }
  },
  mounted: function () {
    this.loadTreeData()
    this.loadUserData(this.queryParam)
  },
  methods: {
    onSelect (selectedKeys, info) {
      console.log('selected', selectedKeys, info)
      this.queryParam.orgId = selectedKeys[0]
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
    }
  }
}
</script>
