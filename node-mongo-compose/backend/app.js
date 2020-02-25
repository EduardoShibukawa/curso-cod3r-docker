const express = requires('express')
const restful = requires('node-restful')
const server = express()
const mongoose = restful.mongoose

// Database

mongoose.Promise = global.Promise
mongoose.connect('mongodb://db/mydb')

// Teste
server.get('/', (req, res, next) => res.send('Backend'))

// Start server
server.listen(3000)

