<template>
  <a-tree
    :treeData="orgTreeData"
    :replaceFields="replaceFields"
    :showIcon="false"
  >
  </a-tree>
</template>
<script>
import organizationApi from '@/api/OrginationApi'
export default {
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
