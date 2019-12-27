<template>
  <a-card :bordered="false">
    <div class="table-operator">
      <a-button type="primary" icon="plus">新建</a-button>
    </div>

    <s-table
      ref="table"
      size="small"
      rowKey="id"
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      :showPagination="false"
    >
      <span slot="idx" slot-scope="idx">
        {{ idx }}
      </span>
      <span slot="name" slot-scope="text">
        {{ text }}
      </span>
      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">编辑</a>
          <a-divider type="vertical"/>
          <a @click="handleDel(record)">删除</a>
        </template>
      </span>
    </s-table>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import { getCategories } from '@/api/category'

const columns = [
  {
    title: '序号',
    dataIndex: 'idx',
    scopedSlots: { customRender: 'idx' }
  },
  {
    title: '名称',
    dataIndex: 'title',
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
  components: {
    STable
  },
  data () {
    return {
      mdl: {},
      columns,
      loadData: parameter => {
        return getCategories(Object.assign(parameter, this.queryParam)).then(res => {
          console.log(res)
          return res.result
        })
      },
      selectedRowKeys: [],
      selectedRows: [],
      options: {
        alert: { show: false },
        rowSelection: {
          selectedRowKeys: this.selectedRowKeys,
          onChange: this.onSelectChange
        }
      },
      optionsAlertShow: false
    }
  },
  created () {
    this.tableOption()
  },
  methods: {
    tableOption () {
      this.options = {
        alert: false,
        rowSelection: null
      }
      this.optionsAlertShow = false
    },
    handleEdit (record) {
      console.log(record)
    },
    handleDel (record) {
      console.log(record)
    }
  },
  onSelectChange (selectedRowKeys, selectedRows) {
    this.selectedRowKeys = selectedRowKeys
    this.selectedRows = selectedRows
  }
}
</script>
