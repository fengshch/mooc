<template>
  <div>
    <b-navbar toggleable="lg" class="mx-4">
      <b-navbar-brand href="#">南驰MOOC</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="{name: 'Home'}">首页</b-nav-item>
          <b-nav-item-dropdown text="课程">
            <b-dropdown-item
              v-for="item in categories"
              :key="item.id"
              :to="{ name: 'Category', params: {categoryId: item.id}}"
            >
              <span> {{ item.name }} </span>
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
          </b-nav-form>

          <b-nav-item :to="{ name: 'login'}" right v-show="!access_token">请登录</b-nav-item>
          <b-nav-item :to="{ name: 'MyCourses'}" right v-show="access_token">我的课程</b-nav-item>
          <b-nav-item-dropdown right v-show="access_token">
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>{{ nickname }}</em>
            </template>
            <b-dropdown-item :to="{ name: 'settings'}">个人设置</b-dropdown-item>
            <b-dropdown-item @click.stop="handleLogout">
              退出
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div id="banner" v-show="isHome">
      <b-carousel
        id="carousel-fade"
        :interval="4000"
        controls
        img-width="1024"
        img-height="80"
        style="text-shadow: 0px 0px 2px #000"
        fade
        indicators
      >
        <b-carousel-slide caption="First slide" img-src="/images/banners/01.jpg"></b-carousel-slide>
        <b-carousel-slide caption="Second Slide" img-src="/images/banners/02.jpg"></b-carousel-slide>
        <b-carousel-slide caption="Third Slide" img-src="/images/banners/03.jpg"></b-carousel-slide>
        <b-carousel-slide caption="Forth Slide" img-src="/imges/banners/04.jpg"></b-carousel-slide>
      </b-carousel>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import categoryApi from '@/api/CategoryApi'
import NoticeIcon from '@/components/NoticeIcon'
export default {
  components: {
    NoticeIcon
  },
  data () {
    return {
      isHome: this.$route.name === 'Home',
      categories: [],
      queryParams: {
        categoryId: this.$route.params.categoryId,
        pageNo: 1,
        pageSize: 5
      }
    }
  },
  computed: {
    ...mapGetters(['nickname', 'avatar', 'access_token']),
    hostname () {
      return window.location.origin
    }
  },
  mounted () {
    console.log('mounted')
    this.loadCategories()
  },
  methods: {
    ...mapActions(['Logout']),
    handleLogout () {
      this.$confirm({
        title: '提示',
        content: '真的要注销登录吗?',
        onOk: () => {
          return this.Logout({}).then(() => {
            setTimeout(() => {
              window.location.reload()
            }, 16)
          }).catch(err => {
            this.$message.error({
              title: '错误',
              description: err.message
            })
          })
        },
        onCancel () {
        }
      })
    },
    loadCategories () {
      categoryApi.getCategories().then(res => {
        this.categories = res.data
      })
    }
  }
}
</script>
