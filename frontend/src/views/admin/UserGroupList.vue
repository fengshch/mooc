<template>
  <a-card :bordered="false">
    <a-table
      :columns="columns"
      :dataSource="data"
      rowKey="id"
      bordered
      :pagination="false">
      <template slot="operation" slot-scope="text,record">
        <span>
          <a @click="handleAddSibling(record)">
            添加同级组
          </a>
          <a-divider type="vertical"/>
          <a @click="handleAddChild(record)">
            添加下级组
          </a>
          <a-divider type="vertical"/>
          <a @click="handleEdit(record)">
            编辑
          </a>
          <a-divider type="vertical" v-show="record.children.length===0"/>
          <a-popconfirm
            v-if="record.children.length===0"
            title="确定要删除吗？"
            @confirm="handleDel(record)">
            <a>删除</a>
          </a-popconfirm>
        </span>
      </template>
    </a-table>
  </a-card>
</template>

<script>
import organizationApi from '@/api/OrganizationApi'
import { mapActions } from 'vuex'
const columns = [
  {
    title: '名称',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '全称',
    dataIndex: 'fullname',
    key: 'fullname'
  },
  {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    width: '400px',
    align: 'center',
    scopedSlots: { customRender: 'operation' }
  }
]
export default {
  data () {
    return {
      columns,
      data: []
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.fetchdata()
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    fetchdata () {
      organizationApi.getOrgTree().then(res => {
        this.data = res.data
      })
    },
    handleAddSibling (record) {
      console.log(record)
      this.$router.push({ name: 'UserGroupEditAdmin', params: { groupId: 'new', parentId: record.parent_id } })
    },
    handleAddChild (record) {
      this.$router.push({ name: 'UserGroupEditAdmin', params: { groupId: 'new', parentId: record.id } })
    },
    handleEdit (record) {
      this.$router.push({ name: 'UserGroupEditAdmin', params: { groupId: record.id } })
    },
    handleDel (record) {
      organizationApi.deleteOrganization(record.id).then(res => {
        this.fetchdata()
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      })
    }
  }
}
</script>
