import Vue from 'vue'
import { login, getInfo, logout } from '@/api/login'
import { ACCESS_TOKEN } from '@/store/mutation-types'
import { welcome } from '@/utils/util'

const user = {
  state: {
    access_token: '',
    refresh_token: '',
    userId: null,
    name: '',
    welcome: '',
    avatar: '',
    roles: [],
    info: {}
  },

  mutations: {
    SET_ACCESS_TOKEN: (state, accessToken) => {
      state.access_token = accessToken
    },
    SET_REFRESH_TOKEN: (state, refreshToken) => {
      state.refresh_token = refreshToken
    },
    SET_USER_ID: (state, userId) => {
      state.userId = userId
    },
    SET_NAME: (state, { name, welcome }) => {
      state.name = name
      state.welcome = welcome
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_INFO: (state, info) => {
      state.info = info
    }
  },

  actions: {
    // 登录
    Login ({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          Vue.ls.set(ACCESS_TOKEN, response.access_token, 7 * 24 * 60 * 60 * 1000)
          commit('SET_ACCESS_TOKEN', response.access_token)
          commit('SET_REFRESH_TOKEN', response.refresh_token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo ({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const result = response.data

          if (result.roles && result.roles.length > 0) {
            // const role = result.roles
            // role.permissions = result.role.permissions
            // role.permissions.map(per => {
            //   if (per.actionEntitySet != null && per.actionEntitySet.length > 0) {
            //     const action = per.actionEntitySet.map(action => { return action.action })
            //     per.actionList = action
            //   }
            // })
            // role.permissionList = role.permissions.map(permission => { return permission.permissionId })
            commit('SET_ROLES', result.roles)
            commit('SET_INFO', result)
          } else {
            reject(new Error('getInfo: roles must be a non-null array !'))
          }
          commit('SET_USER_ID', result.id)
          commit('SET_NAME', { name: result.name, welcome: welcome() })
          commit('SET_AVATAR', result.avatar)

          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    Logout ({ commit, state }) {
      console.log(state.token)
      return new Promise((resolve) => {
        logout(state.token).then(() => {
          resolve()
        }).catch(() => {
          resolve()
        }).finally(() => {
          commit('SET_ACCESS_TOKEN', '')
          commit('SET_ROLES', [])
          commit('SET_USER_ID', null)
          Vue.ls.remove(ACCESS_TOKEN)
        })
      })
    }

  }
}

export default user
