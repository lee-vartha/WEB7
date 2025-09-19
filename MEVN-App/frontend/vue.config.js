// vue.config.js
module.exports = {
  transpileDependencies: true,

  devServer: {
    port: 5000, // change if you want
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // backend server
        changeOrigin: true
      }
    }
  }
}
