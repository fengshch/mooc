<template>
  <a-layout-header :style="{ background: '#fff', padding: '0', minWidth: '600px' }">
    <div class="logo">
      南驰MOOC
    </div>
    <a-menu
      mode="horizontal"
      :style="{ lineHeight: '64px', float: 'left'}"
    >
      <a-menu-item key="home">
        <a href="/" target="_blank">
          首页
        </a>
      </a-menu-item>
      <a-sub-menu>
        <span slot="title">
          课程分类
        </span>
        <a-menu-item
          v-for="item in categories"
          :key="item.id"
          @click="handleMenuItem(item)"
        >
          {{ item.name }}
        </a-menu-item>
      </a-sub-menu>
    </a-menu>
    <div style="display: inline; float:right">
      <router-link :to="{ name: 'MyCourses'}" target="_blank">
        我的课程
      </router-link>
      <user-menu style="float:right; margin: 0 24px"></user-menu>
    </div>
  </a-layout-header>
</template>

<script>
import categoryApi from '@/api/CategoryApi'
import UserMenu from '../tools/UserMenu'
import { mixin } from '@/utils/mixin'
export default {
  components: {
    UserMenu
  },
  mixins: [mixin],
  data () {
    return {
      categories: []
    }
  },
  mounted () {
    this.loadCategories()
  },
  methods: {
    loadCategories () {
      categoryApi.getCategories().then(res => {
        console.log(res)
        this.categories = res.data
      }).catch(err => {
        console.log(err)
      })
    },
    handleMenuItem (item) {
      this.$router.push({ name: 'Category', params: { categoryId: item.id } })
      // const route = this.$router.resolve({ name: 'Category', params: { categoryId: item.id } })
      // let route = this.$router.resolve('/link/to/page'); // This also works.
      // window.open(route.href, '_blank')
    }
  }
}
</script>

<style lang="less" scoped>
  .logo {
    width: 120px;
    height: 48px;
    background:rgba(255, 255, 255, .2);
    margin: 0 24px 32px 24px;
    float: left;
    font-size: 1.3rem;
    font-weight: 100;
  }
  .topright {
    float:right;
    // margin-right: 30px;
  }
</style>
