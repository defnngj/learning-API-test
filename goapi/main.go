package main

import (
	"goapi/router"
)

func main() {
	r := router.InitRouter()
	r.Run(":8081")
}
