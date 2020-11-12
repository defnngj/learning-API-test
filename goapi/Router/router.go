package Router

import (
    "github.com/gin-gonic/gin"
    "goapi/Controllers"
)

func InitRouter() {
    router := gin.Default()
	
	apiV1 := router.Group("api/v1")
    {	

		apiV1.GET("/", Controllers.Hello)
		apiV1.GET("/user/:name", Controllers.HelloName)
		apiV1.GET("/users", Controllers.UserInfo)
		apiV1.POST("/login", Controllers.Login)
    }
    
    router.Run(":8081")
}