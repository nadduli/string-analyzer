require("dotenv").config()
const express = require("express")
const cors = require("cors")
// const crypto = require("crypto")
const stringRouter = require("./routes/strings")
const app = express()
const port = process.env.PORT || 3000

app.use(cors())
app.use(express.json())
app.use("/strings", stringRouter)



app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
})