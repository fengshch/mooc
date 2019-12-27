// const fs = require('fs')
const path = require('path')
const db = require('./db.js')
const routes = require('./routes.js')
const jsonServer = require('json-server')
const {info, userNav} = require('./data/user')
const {login, logout, smsCaptcha, twofactor } = require('./data/auth')

const server = jsonServer.create()
const middlewares = jsonServer.defaults()
const port = process.env.PORT || 3000

server.use(jsonServer.bodyParser)
server.use(middlewares)

// const routes = JSON.parse(fs.readFileSync(path.join(__dirname, 'routes.js')))

server.use((req, res, next) => {
  next()
})

server.post('/api/auth/login', (req, res) => {
  login(req, res)
})
server.use('/api/user/info', (req, res, next) => {
  info(req, res, next)
})
server.post('/api/auth/2step-code', (req, res) => {
  twofactor(req, res)
}) 
server.post('/api/auth/logout', (req, res) => {
  logout(req, res)
})
server.post('/api/auth/sms', (req, res) => {
  smsCaptcha(req, res)
})

const router = jsonServer.router(db())
// server.use("/api", router)
// server.use(jsonServer.rewriter(routes))
server.use(router)
server.listen(port, () => {
  console.log('JSON Server is runing')
})
