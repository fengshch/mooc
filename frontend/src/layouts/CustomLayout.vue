<template>
  <a-layout id="components-layout-demo-top">
    <custom-header />
    <a-layout-content style="margin: 16x 0">
      <route-view></route-view>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      <div class="links">
        <a href="#">帮助</a>
        <a-divider type="vertical"/>
        <a href="#">隐私</a>
        <a-divider type="vertical"/>
        <a href="#">条款</a>
      </div>
      <div class="copyright">
        Copyright &copy; 2020 南驰集团出品
      </div>
    </a-layout-footer>
  </a-layout>
</template>

<script>
import RouteView from './RouteView'
// import { mixinDevice } from '@/utils/mixin'
import CustomHeader from '@/components/CustomHeader'

export default {
  name: 'CustomLayout',
  components: { RouteView, CustomHeader },
  // mixins: [mixinDevice],
  data () {
    return {}
  },
  mounted () {
    // document.body.classList.add('userLayout')
  },
  beforeDestroy () {
    // document.body.classList.remove('userLayout')
  }
}
</script>
