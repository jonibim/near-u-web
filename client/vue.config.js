const fs = require('fs')

module.exports = {
    devServer: {
      open: process.platform === 'darwin',
      host: '0.0.0.0',
      port: 8080, // CHANGE YOUR PORT HERE!
      disableHostCheck: true,  
      https: {
        key: fs.readFileSync('./certs/raspberrypi.local.key'),
        cert: fs.readFileSync('./certs/raspberrypi.local.crt'),
      },
    },
  }