const  Mock = require('mockjs2')
// import { builder, getBody } from '../util'

const username = ['admin', 'super']
// 强硬要求 ant.design 相同密码
// '21232f297a57a5a743894a0e4a801fc3',
const password = ['8914de686ab28dc22f30d3d8e107ff6c'] // admin, ant.design

const login = (req, res) => {
  const body = req.body
  console.log('mock: body', body)
  if (!body || !username.includes(body.username) || !password.includes(body.password)) {
    res.status(401)
    res.jsonp({ isLogin: true, msg: '账户或密码错误'})
    res.send()
    return
  }

  res.jsonp({
    result: {
    'id': Mock.mock('@guid'),
    'name': Mock.mock('@name'),
    'username': 'admin',
    'password': '',
    'avatar': 'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png',
    'status': 1,
    'telephone': '',
    'lastLoginIp': '27.154.74.117',
    'lastLoginTime': 1534837621348,
    'creatorId': 'admin',
    'createTime': 1497160610259,
    'deleted': 0,
    'roleId': 'admin',
    'lang': 'zh-CN',
    'token': '4291d7da9005377ec9aec4a71ea837f'
  }, message: '',code: 200, header: { 'Custom-Header': Mock.mock('@guid') }})
}

const logout = (req, res) => {
  res.jsonp({msg: '[测试接口] 注销成功'})
}

const smsCaptcha = (req, res) => {
  res.jsonp({ captcha: Mock.mock('@integer(10000, 99999)') })
}

const twofactor = (req, res) => {
  res.jsonp({ stepCode: Mock.mock('@integer(0, 1)') })
}

// Mock.mock(/\/auth\/login/, 'post', login)
// Mock.mock(/\/auth\/logout/, 'post', logout)
// Mock.mock(/\/account\/sms/, 'post', smsCaptcha)
// Mock.mock(/\/auth\/2step-code/, 'post', twofactor)
module.exports = {
  login,
  logout,
  smsCaptcha,
  twofactor
}