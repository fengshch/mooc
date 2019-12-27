<template>
  <a-card :bordered="false">
    <a-row :gutter="8">
      <a-col :span="5">
        <s-tree
          :dataSource="orgTreeData"
          :openKeys.sync="openKeys"
          :search="true"
        ></s-tree>
      </a-col>
    </a-row>
  </a-card>
</template>
<script>
import STree from './components/OrgTree'
import organizationApi from '@/api/OrginationApi'
export default {
  components: {
    STree
  },
  data () {
    return {
      orgTreeData: [],
      replaceFields: {
        title: 'name',
        key: 'id'
      }
    }
  },
  mounted: function () {
    this.loadTreeData()
  },
  methods: {
    onSelect (selectedKeys, info) {
      console.log('selected', selectedKeys, info)
    },
    onCheck (checkedKeys, info) {
      console.log('onCheck', checkedKeys, info)
    },
    loadTreeData () {
      organizationApi.getOrgTree().then(res => {
        this.orgTreeData = res.data
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
