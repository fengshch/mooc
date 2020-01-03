<template>
  <a-card :bordered="false">
    <div class="table-operator">
      <a-tree-select
        showSearch
        style="width: 300px"
        :dropdownStyle="{ maxHeight: '400px', overflow: 'auto' }"
        placeholder="请选择用户组"
        allowClear
        treeDefaultExpandAll
        :treeData="orgTreeData"
        v-model="organizationId"
        v-decorator="[
          'organization_id',
          {
            rules: [{ required: true, message: '用户组不能为空'}]
          }
        ]"
      />
      是否显示子机构用户:
      <a-switch defaultChecked checkedChildren="显示" v-model="queryParam.showGrand" unCheckedChildren="不显示" @change="onSwitchChange"/>
    </div>
    <a-transfer
      showSearch
      :dataSource="userData"
      :targetKeys="targetKeys"
      :selectedKey="selectedKeys"
      :render="item=>item.title"
      @change="handleChange"
      :listStyle="{
        width: '250px',
        height: '300px',
      }"
      :operations="['选中', '取消']"
    >
    </a-transfer>
  </a-card>
</template>

<script>
import organizationApi from '@/api/OrganizationApi'
import { mapActions } from 'vuex'
import userApi from '../../api/UserApi'
import learningApi from '@/api/LearningApi'

export default {
  data () {
    return {
      orgTreeData: [],
      courseId: null,
      userData: [],
      targetKeys: [],
      selectedKeys: [],
      organizationId: null,
      queryParam: {
        orgId: 0,
        pageNo: 1,
        pageSize: 10,
        showGrand: true
      }
    }
  },
  watch: {
    organizationId: function (val) {
      this.queryParam.orgId = val
      this.loadUserData()
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.loadOrgData()
      if (to.params.courseId) {
        vm.courseId = to.params.courseId
      }
      vm.loadUserData()
    })
  },
  methods: {
    ...mapActions(['showAlert']),
    loadOrgData () {
      organizationApi
        .getOrgTree()
        .then(res => {
          this.orgTreeData = []
          res.data.map(org => this.orgTreeData.push(this.transferOrgToNode(org)))
        })
        .catch(error => {
          console.log(error)
        })
    },
    loadUserData () {
      userApi.getUsersByOrgId(this.queryParam).then(res => {
        this.userData = []
        res.data.map(item => this.userData.push({
          key: item.id.toString(),
          title: item.name,
          description: item.name
        }))
        this.loadSelectedUser()
      })
    },
    transferOrgToNode (org) {
      const node = { 'key': org.id, 'value': '' + org.id, 'label': org.name, children: [] }
      org.children.map(item => node.children.push(this.transferOrgToNode(item)))
      return node
    },
    handleChange (nextTargetKeys, direction, moveKeys) {
      console.log(direction)
      if (direction === 'right') {
        learningApi.addLearningByCourseId({
          courseId: this.courseId,
          userIds: moveKeys
        }).then(res => {
          this.targetKeys = nextTargetKeys
          this.showAlert({
            'show': true,
            'type': 'success',
            'message': res.message
          })
        })
      } else {
        learningApi.deleteLearningByCourseId({
          courseId: this.courseId,
          userIds: moveKeys
        }).then(res => {
          this.targetKeys = nextTargetKeys
          this.showAlert({
            'show': true,
            'type': 'success',
            'message': res.message
          })
        })
      }
    },
    onSwitchChange () {
      this.loadUserData()
    },
    loadSelectedUser () {
      console.log(this.courseId)
      learningApi.getLearningByCourseId({
        courseId: this.courseId,
        orgId: this.queryParam.orgId,
        showGrand: this.queryParam.showGrand
      }).then(res => {
        this.targetKeys = []
        res.data.map(item => {
          console.log(item.user_id)
          this.targetKeys.push(item.user_id.toString())
        })
      })
    }
  }
}
</script>
