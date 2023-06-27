package Controllers

/*
参考：https://geektutu.com/post/quick-go-gin.html
*/

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"goapi/Controllers/common"
	"net/http"
	"reflect"
)

func Hello(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    "hello gin!",
	})

}

func HelloName(c *gin.Context) {
	name := c.Param("name")
	c.JSON(http.StatusOK, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    "hello, " + name,
	})
}

func UserInfo(c *gin.Context) {
	name := c.Query("name")
	role := c.DefaultQuery("role", "tearcher")
	c.JSON(http.StatusOK, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    name + " is a " + role,
	})
}

func Login(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	//判断返回值类型
	fmt.Println(reflect.TypeOf(username))
	fmt.Println(reflect.TypeOf(password))

	if username == "" || password == "" {
		c.JSON(http.StatusOK, common.Response("10101", "username or password null", ""))
	} else if username != "admin" || password != "123" {
		c.JSON(http.StatusOK, common.Response("10102", "username or password error", ""))
	} else {
		c.JSON(http.StatusOK, common.Response("10200", "success", ""))

	}

}
