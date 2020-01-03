<template>
  <a-card :bordered="false">
    <a-table :columns="columns" :dataSource="learningData" rowKey="id" :pagination="pagination" :bordered="true">
      <template slot="operation" slot-scope="text,record">
        <span>
          <a-popconfirm
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
import learningApi from '@/api/LearningApi'
import { Icon } from 'ant-design-vue'
import { mapActions, mapGetters } from 'vuex'

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1511545_tdkl3xmtms.js'
})
const columns = [
  {
    title: '序号',
    dataIndex: 'no',
    width: '60px'
  }, {
    title: '课程标题',
    dataIndex: 'course_title',
    width: '120px'
  }, {
    title: '课程类别',
    dataIndex: 'category_name'
  }, {
    title: '进度',
    dataIndex: 'progress'
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
  components: {
    IconFont
  },
  data () {
    return {
      columns,
      learningData: [],
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
          this.loadLearningData(this.queryParam)
        },
        onShowSizeChange: (current, pageSize) => {
          this.pagination.pageSize = pageSize
          this.queryParam.pageSize = this.pagination.pageSize
          this.loadLearningData(this.queryParam)
        }
      },
      queryParam: {
        userId: 0,
        pageNo: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    ...mapGetters(['userId'])
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.queryParam.userId = vm.userId
      vm.loadLearningData(vm.queryParam)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadLearningData (queryParam) {
      learningApi.getLearningByUserId(queryParam).then(res => {
        this.pagination.current = res.pageNo
        this.pagination.pageSize = res.pageSize
        this.pagination.total = res.totalCount
        this.learningData = res.data
        console.log(res.data)
        this.learningData.forEach((value, index) => {
          value.no = (res.pageNo - 1) * res.pageSize + index + 1
        })
      })
    },
    handleDel (record) {
      learningApi.deleteLearningById(record.id).then(res => {
        this.loadLearningData(this.queryParam)
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      })
    },
    onSwitchChange () {
      this.loadLearningData(this.queryParam)
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
