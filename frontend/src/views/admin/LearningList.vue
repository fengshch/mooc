<template>
  <a-card :bordered="false">
    <a-col :span="24" :style="{ marginBottom: '18px'}">
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
      </a-col>
    </a-row>
  </a-card>
</template>
<script>
import UserGroupTree from '@/components/Tree/UserGroupTree'
import organizationApi from '@/api/OrganizationApi'
import learningApi from '@/api/LearningApi'
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
    title: '用户名',
    dataIndex: 'user_name',
    width: '80px'
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
      vm.loadLearningData(vm.queryParam)
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    onSelect (selectKeys, info) {
      this.queryParam.orgId = selectKeys[0]
      this.queryParam.pageNo = 1
      this.loadLearningData(this.queryParam)
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
    loadLearningData (queryParam) {
      learningApi.getLearningByOrgId(queryParam).then(res => {
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
