import { Menu, Icon, Input } from 'ant-design-vue'

const { Item, SubMenu } = Menu
const { Search } = Input

export default {
  name: 'Tree',
  props: {
    dataSource: {
      type: Array,
      required: true
    },
    openKeys: {
      type: Array,
      default: () => []
    },
    search: {
      type: Boolean,
      default: false
    }
  },
  created () {
    this.localOpenKeys = this.openKeys.slice(0)
  },
  data () {
    return {
      localOpenKeys: []
    }
  },
  methods: {
    handlePlus (e, item) {
      e.preventDefault()
      this.$emit('add', item)
    },
    handleTitleClick (...args) {
      this.$emit('titleClick', { args })
    },

    renderSearch () {
      return (
        <Search
          placeholder="input search text"
          style="width: 100%; margin-bottom: 1rem"
        />
      )
    },
    renderIcon (icon) {
      return icon && (<Icon type="group" />) || null
    },
    renderIconFont (icon) {
      const IconFont = Icon.createFromIconfontCN({
        scriptUrl: '//at.alicdn.com/t/font_1511545_tdkl3xmtms.js'
      })
      return icon && (<IconFont type={icon}/>) || null
    },
    renderMenuItem (item) {
      return (
        <Item key={item.id}>
          { item.name }
          <a-dropdown>
            <a class="btn"><a-icon type="ellipsis" /></a>
            <a-menu slot="overlay">
              <a-menu-item key="1">新增用户</a-menu-item>
            </a-menu>
          </a-dropdown>
        </Item>
      )
    },
    renderItem (item) {
      return item.children && item.children.length > 0 ? this.renderSubItem(item, item.id) : this.renderMenuItem(item, item.id)
    },
    renderSubItem (item, key) {
      const childrenItems = item.children && item.children.map(o => {
        return this.renderItem(o, o.id)
      })

      const name = (
        <span slot="title">
          { this.renderIconFont('iconfont-usergroup') }
          <span>{ item.name }</span>
          <a-dropdown>
            <a class="btn" {...{ on: { mouseClick: e => e.preventDefault() } }}><a-icon type="ellipsis" /></a>
            <a-menu slot="overlay">
              <a-menu-item key="1" {...{ on: { click: e => this.handlePlus(e, item) } } }>新增用户</a-menu-item>
              <a-checkbox style="margin-left:10px">显示子组用户</a-checkbox>
            </a-menu>
          </a-dropdown>
        </span>
      )

      // titleClick={this.handleTitleClick(item)}
      return (
        <SubMenu key={ key }>
          { name }
          { childrenItems }
        </SubMenu>
      )
    }
  },
  render () {
    const { dataSource, search } = this.$props

    // this.localOpenKeys = openKeys.slice(0)
    const list = dataSource.map(item => {
      return this.renderItem(item)
    })

    return (
      <div class="tree-wrapper">
        { search ? this.renderSearch() : null }
        <Menu mode="inline" class="custom-tree" {...{ on: { click: item => this.$emit('click', item), 'update:openKeys': val => { this.localOpenKeys = val } } }} openKeys={this.localOpenKeys}>
          { list }
        </Menu>
      </div>
    )
  }
}
