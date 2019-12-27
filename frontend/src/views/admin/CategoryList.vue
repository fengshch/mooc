<template>
  <a-card :bordered="false">
    <div class="table-operator">
      <a-button type="primary" icon="plus" @click="handleNew()">新建</a-button>
    </div>

    <a-table
      size="small"
      rowKey="id"
      :columns="columns"
      :dataSource="categories"
      :pagination="pagination"
      :bordered="false"
    >
      <span slot="no" slot-scope="no">
        {{ no }}
      </span>
      <span slot="name" slot-scope="text">
        {{ text }}
      </span>
      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">编辑</a>
          <a-divider type="vertical"/>
          <a-popconfirm
            v-if="categories.length"
            title="确定要删除吗？"
            @confirm="handleDel(record)">
            <a>删除</a>
          </a-popconfirm>
        </template>
      </span>
    </a-table>
  </a-card>
</template>

<script>
import categoryApi from '@/api/CategoryApi'
import { mapActions } from 'vuex'

const columns = [
  {
    title: '序号',
    dataIndex: 'no',
    customRender: (value, row, index) => {
      return value
    }
  },
  {
    title: '名称',
    dataIndex: 'name',
    scopedSlots: { customRender: 'name' }
  },
  {
    title: '操作',
    dataIndex: 'action',
    width: '150px',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'CategoryAdmin',
  data () {
    return {
      mdl: {},
      columns,
      categories: [],
      pagination: {
        pageSizeOptions: ['5', '10', '20'],
        hideOnSinglePage: true,
        defaultCurrent: 1,
        defaltPageSize: 5,
        showSizeChanger: true,
        showQuickJumper: false,
        pageSize: 5,
        total: 0,
        onChange: pageNo => {
          this.queryParam.pageNo = pageNo
          this.loadData(this.queryParam)
        },
        onShowSizeChange: (current, pageSize) => {
          console.log(pageSize)
          this.pagination.pageSize = pageSize
          this.queryParam.pageSize = this.pagination.pageSize
          this.loadData(this.queryParam)
        }
      },
      queryParam: {
        pageNo: 1,
        pageSize: 5
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadData()
    })
  },
  created () {
  },
  methods: {
    ...mapActions(['showAlert']),
    tableOption () {
      this.options = {
        alert: false,
        rowSelection: null
      }
      this.optionsAlertShow = false
    },
    handleEdit (record) {
      this.$router.push({ name: 'CategoryEditAdmin', params: { categoryId: record.id } })
    },
    handleDel (record) {
      categoryApi.deleteCategory(record.id).then(res => {
        if (this.categories.length === 1 && this.queryParam.pageNo > 1) {
          this.queryParam.pageNo = this.queryParam.pageNo - 1
        }
        this.loadData()
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      }).catch(err => {
        this.showAlert({
          'type': 'error',
          'message': err.message
        })
      })
    },
    handleNew () {
      this.$router.push({ name: 'CategoryEditAdmin', params: { categoryId: 'new' } })
    },
    loadData () {
      categoryApi.getCategories(this.queryParam).then(res => {
        this.categories = res.data
        this.categories.forEach((value, index) => {
          value.no = (res.pageNo - 1) * res.pageSize + index + 1
        })
        this.pagination.pageSize = res.pageSize
        this.pagination.total = res.totalCount
      })
    }
  },
  onSelectChange (selectedRowKeys, selectedRows) {
    this.selectedRowKeys = selectedRowKeys
    this.selectedRows = selectedRows
  }
}
</script>
