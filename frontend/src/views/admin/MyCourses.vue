<template>
  <a-card :bordered="false">
    <a-list :grid="{ gutter: 16, column: 4}" :dataSource="data">
      <a-list-item slot="renderItem" slot-scope="item">
        <a-card hoverable style="margin: 20px; padding: 20px">
          <img
            :src="item.avatar"
            slot="cover"
          />
          <a-card-meta :title="item.title">
          </a-card-meta>
          <template class="ant-card-actions" slot="actions">
            <a-icon type="delete"/>
          </template>
        </a-card>
      </a-list-item>
    </a-list>
  </a-card>
</template>

<script>
import courseApi from '@/api/CourseApi'

export default {
  name: 'MyCourses',
  data () {
    return {
      data: [],
      userId: 0
    }
  },
  mounted () {
    this.loadData(this.userId)
  },
  methods: {
    loadData (userId) {
      courseApi.getCoursesByUserId(userId).then(res => {
        this.data = res.data
      })
    }
  }
}
</script>
