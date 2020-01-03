// eslint-disable-next-line
import { UserLayout, BasicLayout, RouteView, PageView, HomeLayout } from '@/layouts'
import { bxAnaalyse } from '@/core/icons'

export const asyncRouterMap = [

  {
    path: '/admin',
    name: 'index',
    component: BasicLayout,
    meta: { title: '系统管理' },
    redirect: '/admin/course-admin',
    children: [
      // Courses Management
      {
        path: '/admin/course-admin',
        name: 'Admin',
        redirect: '/admin/categories',
        component: PageView,
        meta: { title: '课程管理', keepAlive: true, icon: bxAnaalyse, roles: [ 'system', 'manager', 'user' ] },
        children: [
          {
            path: '/admin/categories',
            name: 'CategoryListAdmin',
            component: () => import('@/views/admin/CategoryList'),
            meta: { title: '课程分类', keepAlive: true, roles: [ 'system', 'manager', 'user' ] }
          },
          {
            path: '/admin/categories/:categoryId',
            name: 'CategoryEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/CategoryEdit'),
            meta: { title: '编辑课程分类', keepAlive: true, roles: [ 'system', 'manager' ] }
          },
          {
            path: '/admin/courses',
            name: 'CourseListAdmin',
            component: () => import('@/views/admin/CourseList'),
            meta: { title: '课程列表', keepAlive: true, roles: [ 'system', 'manager', 'user' ] }
          },
          {
            path: '/admin/courses/:courseId',
            name: 'CourseEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/CourseEdit'),
            meta: { title: '编辑课程详情', keepAlive: true, roles: [ 'system', 'manager' ] }
          },
          {
            path: '/admin/chapters/:chapterId',
            name: 'ChapterEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/ChapterEdit'),
            meta: { title: '编辑章节', keepAlive: true, roles: [ 'system', 'manager' ] },
            props: { courseId: null }
          },
          {
            path: '/admin/videos/:videoId',
            name: 'VideoEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/VideoEdit'),
            meta: { title: '编辑视频', keepAlive: true, roles: [ 'system', 'manager' ] },
            props: { chapterId: null }
          },
          {
            path: '/admin/chapters/course/:courseId',
            name: 'ChapterListAdmin',
            hidden: true,
            component: () => import('@/views/admin/ChapterList'),
            meta: { title: '课程章节', roles: [ 'system', 'manager', 'user' ] }
          }
        ]
      },

      // User Management
      {
        path: '/admin/users',
        name: 'UserAdmin',
        component: PageView,
        meta: { title: '用户管理', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] },
        children: [
          {
            path: '/admin/groups',
            name: 'GroupListAdmin',
            component: () => import('@/views/admin/UserGroupList'),
            meta: { title: '用户组', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] }
          },
          {
            path: '/admin/groups/:groupId',
            name: 'UserGroupEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/UserGroupEdit'),
            meta: { title: '编辑用户组', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] },
            props: { parentId: null }
          },
          {
            path: '/admin/users/list',
            name: 'UserListAdmin',
            component: () => import('@/views/admin/UserList'),
            meta: { title: '用户列表', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] }
          },
          {
            path: '/admin/users/edit',
            name: 'UserEditAdmin',
            hidden: true,
            component: () => import('@/views/admin/UserEdit'),
            meta: { title: '编辑用户', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] },
            props: { userId: null }
          }
        ]
      },
      {
        path: '/admin/learning',
        name: 'learning',
        component: PageView,
        meta: { title: '学习管理', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager', 'user'] },
        children: [
          {
            path: '/admin/learnings/list',
            name: 'LearningList',
            component: () => import('@/views/admin/LearningList'),
            meta: { title: '选课列表', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] }
          },
          {
            path: '/admin/learnings/course/:courseId',
            name: 'LearningSelectUsers',
            hidden: true,
            component: () => import('@/views/admin/LearningUsersSelected'),
            meta: { title: '选课列表', keepAlive: true, icon: bxAnaalyse, roles: ['system', 'manager'] }
          }
        ]
      },
      // Exception
      {
        path: '/exception',
        name: 'exception',
        component: RouteView,
        redirect: '/exception/403',
        hidden: true,
        meta: { title: '异常页', icon: 'warning', permission: [ 'exception' ] },
        children: [
          {
            path: '/exception/403',
            name: 'Exception403',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/403'),
            meta: { title: '403', permission: [ 'exception' ] }
          },
          {
            path: '/exception/404',
            name: 'Exception404',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404'),
            meta: { title: '404', permission: [ 'exception' ] }
          },
          {
            path: '/exception/500',
            name: 'Exception500',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/500'),
            meta: { title: '500', permission: [ 'exception' ] }
          }
        ]
      },

      // account
      {
        path: '/account',
        component: PageView,
        redirect: '/account/learning',
        name: 'account',
        meta: { title: '个人中心', icon: 'user', keepAlive: true, roles: [ 'system', 'manager', 'user' ] },
        children: [
          {
            path: '/account/learning',
            name: 'MyCourses',
            component: () => import('@/views/admin/MyLearninglist'),
            meta: { title: '我的课程', keepAlive: true, roles: [ 'system', 'manager', 'user' ] }
          },
          {
            path: '/account/settings',
            name: 'settings',
            component: () => import('@/views/account/settings/Index'),
            meta: { title: '个人设置', hideHeader: true, roles: [ 'system', 'manager', 'user' ] },
            redirect: '/account/settings/base',
            hideChildrenInMenu: true,
            children: [
              {
                path: '/account/settings/base',
                name: 'BaseSettings',
                component: () => import('@/views/account/settings/BaseSetting'),
                meta: { title: '基本设置', roles: [ 'system', 'manager', 'user' ] }
              },
              {
                path: '/account/settings/password',
                name: 'PasswordSettings',
                component: () => import('@/views/account/settings/Password'),
                meta: { title: '修改密码', keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/custom',
                name: 'CustomSettings',
                component: () => import('@/views/account/settings/Custom'),
                meta: { title: '个性化设置', keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/binding',
                name: 'BindingSettings',
                component: () => import('@/views/account/settings/Binding'),
                meta: { title: '账户绑定', keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/notification',
                name: 'NotificationSettings',
                component: () => import('@/views/account/settings/Notification'),
                meta: { title: '新消息通知', keepAlive: true, permission: [ 'user' ] }
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*', redirect: '/404', hidden: true
  }
]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register')
      },
      {
        path: 'register-result',
        name: 'registerResult',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult')
      },
      {
        path: 'recover',
        name: 'recover',
        component: undefined
      }
    ]
  },
  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  },
  {
    path: '/',
    component: HomeLayout,
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/Home')
      },
      {
        path: '/category/:categoryId',
        name: 'Category',
        component: () => import('@/views/Category')
      },
      {
        path: '/courses/:courseId',
        name: 'CourseDetail',
        component: () => import('@/views/CourseDetail')
      },
      {
        path: '/play/learning/:learningId',
        name: 'playLearning',
        component: () => import('@/views/PlayLearning'),
        meta: { title: '安全设置', keepAlive: true, permission: [ 'system', 'manager', 'user' ] }
      }
    ]
  }
]
