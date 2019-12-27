<template>
  <div class="page-header">
    <div class="page-header-index-wide">
      <s-breadcrumb />
      <div class="detail">
        <div class="main" v-if="!$route.meta.hiddenHeaderContent">
          <div class="row">
            <img v-if="logo" :src="logo" class="logo"/>
            <h1 v-if="title" class="title">{{ title }}</h1>
            <a-alert
              :class="[alert.show? 'show':'hide']"
              class="flash"
              :message="alert.message"
              :type="alert.type"
              :description="alert.description"
              :showIcon="alert.showIcon"
              closable
            >
              <a-icon type="close" slot="closeText" @click.stop="onClick" style="font-size:16px"/>
            </a-alert>
            <div class="action">
              <slot name="action"></slot>
            </div>
          </div>
          <div class="row">
            <div v-if="avatar" class="avatar">
              <a-avatar :src="avatar" />
            </div>
            <div v-if="this.$slots.content" class="headerContent">
              <slot name="content"></slot>
            </div>
            <div v-if="this.$slots.extra" class="extra">
              <slot name="extra"></slot>
            </div>
          </div>
          <div>
            <slot name="pageMenu"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/tools/Breadcrumb'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'PageHeader',
  components: {
    's-breadcrumb': Breadcrumb
  },
  props: {
    title: {
      type: [String, Boolean],
      default: true,
      required: false
    },
    logo: {
      type: String,
      default: '',
      required: false
    },
    avatar: {
      type: String,
      default: '',
      required: false
    }
  },
  data () {
    return {}
  },
  computed: {
    ...mapState({
      alert: state => state.flash.alert
    })
  },
  methods: {
    ...mapActions(['closeAlert']),
    onClick (e) {
      // console.log('click')
      this.closeAlert()
    }
  }
}
</script>

<style lang="less" scoped>
.show {
  visibility: visible
}
.hide {
  visibility: hidden;
}
.page-header {
  background: #fff;
  padding: 16px 32px 0;
  border-bottom: 1px solid #e8e8e8;

  .breadcrumb {
    margin-bottom: 16px;
  }

  .detail {
    display: flex;
    /*margin-bottom: 16px;*/

    .avatar {
      flex: 0 1 72px;
      margin: 0 24px 8px 0;

      & > span {
        border-radius: 72px;
        display: block;
        width: 72px;
        height: 72px;
      }
    }

    .main {
      width: 100%;
      flex: 0 1 auto;

      .row {
        display: flex;
        width: 100%;

        .avatar {
          margin-bottom: 16px;
        }
      }
     .flash {
        margin-bottom: 16px;
        min-width: 300px;
        max-width: 800px;
        flex-grow: 0;
      }
      .title {
        font-size: 20px;
        font-weight: 500;
        min-width: 200px;
        max-width: 500px;
        font-size: 20px;
        line-height: 28px;
        font-weight: 500;
        color: rgba(0, 0, 0, 0.85);
        margin-bottom: 16px;
        flex-grow: 1;
      }
      .logo {
        width: 28px;
        height: 28px;
        border-radius: 4px;
        margin-right: 16px;
      }
      .content,
      .headerContent {
        flex: auto;
        color: rgba(0, 0, 0, 0.45);
        line-height: 22px;

        .link {
          margin-top: 16px;
          line-height: 24px;

          a {
            font-size: 14px;
            margin-right: 32px;
          }
        }
      }
      .extra {
        flex: 0 1 auto;
        margin-left: 88px;
        min-width: 242px;
        text-align: right;
      }
      .action {
        margin-left: 56px;
        min-width: 266px;
        flex: 0 1 auto;
        text-align: right;
        &:empty {
          display: none;
        }
      }
    }
  }
}

.mobile .page-header {
  .main {
    .row {
      flex-wrap: wrap;

      .avatar {
        flex: 0 1 25%;
        margin: 0 2% 8px 0;
      }

      .content,
      .headerContent {
        flex: 0 1 70%;

        .link {
          margin-top: 16px;
          line-height: 24px;

          a {
            font-size: 14px;
            margin-right: 10px;
          }
        }
      }

      .extra {
        flex: 1 1 auto;
        margin-left: 0;
        min-width: 0;
        text-align: right;
      }

      .action {
        margin-left: unset;
        min-width: 266px;
        flex: 0 1 auto;
        text-align: left;
        margin-bottom: 12px;

        &:empty {
          display: none;
        }
      }
    }
  }
}
</style>
