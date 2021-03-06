<template>
  <a-card :bordered="false">
    <div slot="extra">
      <a-radio-group v-model="status">
        <a-radio-button value="all">全部</a-radio-button>
        <a-radio-button value="all">已发布</a-radio-button>
        <a-radio-button value="all">未发布</a-radio-button>
      </a-radio-group>
      <a-input-search style="margin-left:16px; width: 272px;"/>
    </div>

    <div class="table-operator">
      <a-button type="dashed" style="width: 100%" icon="plus" @click="handleAdd" >添加</a-button>
    </div>

    <a-list size="large" :pagination="pagination">
      <a-list-item :key="index" v-for="(item,index) in data">
        <a-list-item-meta>
          <div slot="description">
            <div v-html="item.intro"/>
          </div>
          <a-avatar slot="avatar" size="large" shape="square" :src="item.cover"/>
          <a slot="title">{{ item.title }}</a>
        </a-list-item-meta>
        <div slot="actions">
          <router-link :to="{ name: 'CourseEditAdmin', params: { courseId: item.id}}">编辑</router-link>
        </div>
        <div slot="actions">
          <router-link :to="{ name: 'ChapterListAdmin', params: { courseId: item.id}}">章节</router-link>
        </div>
        <div slot="actions">
          <router-link :to="{ name: 'LearningSelectUsers', params: { courseId: item.id}}">分配学员</router-link>
        </div>
        <div slot="actions">
          <a-popconfirm
            title="确定要删除吗？"
            @confirm="handleDel(item)">
            <a>删除</a>
          </a-popconfirm>
        </div>
        <div slot="actions">
          <a-dropdown>
            <a-menu slot="overlay">
              <a-menu-item>
                <router-link :to="{ name: 'CourseEditAdmin', params: { courseId: item.id}}">编辑</router-link>
              </a-menu-item>
              <a-menu-item>
                <router-link :to="{ name: 'ChapterListAdmin', params: { courseId: item.id}}">章节</router-link>
              </a-menu-item>
              <a-menu-item>
                <a @click="handleDel(item)">删除</a>
              </a-menu-item>
            </a-menu>
            <a><a-icon type="down"/></a>
          </a-dropdown>
        </div>
        <div class="list-content">
          <div class="list-content-it">
            <span class="mr-5">{{ item.category_name }}</span>
            <span class="ml-5">
              <a-switch
                :checked="item.published"
                @change="onPublishedChange(index, item.id, item.published)"
              />
            </span>
          </div>
        </div>
      </a-list-item>
    </a-list>
  </a-card>
</template>

<script>
import courseApi from '@/api/CourseApi'
import { mapActions } from 'vuex'

export default {
  name: 'CourseList',
  data () {
    return {
      data: [],
      status: 'all',
      pagination: {
        showSizeChanger: true,
        showQuickJumper: true,
        pageSize: 5,
        total: 0,
        onChange: pageNo => {
          this.queryParam.pageNo = pageNo
          this.loadData(this.queryParam)
        },
        onShowSizeChange: (current, pageSize) => {
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
  methods: {
    ...mapActions(['showAlert']),
    handleAdd () {
      this.$router.push({ name: 'CourseEditAdmin', params: { courseId: 'new' } })
    },
    handleDel (record) {
      courseApi.deleteCourseById(record.id).then(res => {
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
    loadData () {
      courseApi.getCourses(this.queryParam).then(res => {
        this.data = res.data
        this.pagination.pageSize = res.pageSize
        this.pagination.total = res.totalCount
      })
    },
    onPublishedChange (index, courseId, checked) {
      courseApi.updatePublished(courseId, !checked).then(res => {
        this.data[index].published = res.data
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>
    .ant-avatar-lg {
        width: 150px;
        height: 100px;
        line-height: 60px;
    }

    .list-content-item {
        color: rgba(0, 0, 0, .45);
        display: inline-block;
        vertical-align: middle;
        font-size: 14px;
        margin-left: 20px;
        span {
            line-height: 20px;
        }
        p {
            margin-top: 4px;
            margin-bottom: 0;
            line-height: 22px;
        }
    }
</style>
