<template>
  <div :class="prefixCls">
    <quill-editor
      v-model="content"
      ref="myQuillEditor"
      :options="editorOption"
      @blur="onEditorBlur($event)"
      @focus="onEditorFocus($event)"
      @ready="onEditorReady($event)"
      @change="onEditorChange($event)">
    </quill-editor>

  </div>
</template>

<script>
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor'

export default {
  name: 'QuillEditor',
  components: {
    quillEditor
  },
  props: {
    prefixCls: {
      type: String,
      default: 'ant-editor-quill'
    },
    // 表单校验用字段
    // eslint-disable-next-line
    value: {
      type: String
    },
    editorOption: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      content: null
    }
  },
  methods: {
    onEditorBlur (quill) {
      this.emit('editorBlur', quill)
    },
    onEditorFocus (quill) {
      this.emit('editorForcus', quill)
    },
    onEditorReady (quill) {
      this.emit('editorReady', quill)
    },
    onEditorChange ({ quill, html, text }) {
      console.print(text)
      this.$emit('change', html)
    }
  },
  watch: {
    value (val) {
      console.log(val)
      this.content = val
    }
  }
}
</script>

<style lang="less" scoped>
@import url('../index.less');

/* 覆盖 quill 默认边框圆角为 ant 默认圆角，用于统一 ant 组件风格 */
.ant-editor-quill {
  /deep/ .ql-toolbar.ql-snow {
    border-radius: @border-radius-base @border-radius-base 0 0;
  }
  /deep/ .ql-container.ql-snow {
    border-radius: 0 0 @border-radius-base @border-radius-base;
  }
}
</style>
