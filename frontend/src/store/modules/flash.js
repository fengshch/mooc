const flash = {
  state: {
    alert: {
      show: false,
      type: 'info',
      message: '',
      description: '',
      showIcon: true
    }
  },
  mutations: {
    SHOW_ALERT: (state, alert) => {
      state.alert = {
        show: true,
        type: alert.type,
        message: alert.message,
        description: alert.description,
        showIcon: true
      }
    },
    CLOSE_ALERT: (state) => {
      state.alert.show = false
    }
  },
  actions: {
    showAlert ({ commit }, alert) {
      commit('SHOW_ALERT', alert)
    },
    closeAlert ({ commit }) {
      commit('CLOSE_ALERT')
    }
  }
}

export default flash
