let {categories, courses} = require('./data/courses.js')
// let {info, userNav} = require('./data/user.js')

module.exports = function() {
  var data = { 
      categories: categories(),
      courses: courses(100)
      // user:  {
      //   info: info()
      // },
      // userNav: userNav()
  };
  
  return data
}