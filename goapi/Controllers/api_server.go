package Controllers

/*
参考：https://geektutu.com/post/quick-go-gin.html
*/

import (
	//"gopai/Controllers/common/reponse"
	"github.com/gin-gonic/gin"
)


func Hello(c *gin.Context) {
	c.JSON(200, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    "hello gin!",
	})

}

func HelloName(c *gin.Context) {
	name := c.Param("name")
	c.JSON(200, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    "hello, " + name,
	})
}

func UserInfo(c *gin.Context) {
	name := c.Query("name")
	role := c.DefaultQuery("role", "tearcher")
	c.JSON(200, gin.H{
		"code":    "10200",
		"message": "success",
		"data":    name + " is a " + role,
	})
}

// func Login(c *gin.Context) {
// 	username := c.PostForm("username")
// 	password := c.PostForm("password")

// 	//判断返回值类型
// 	fmt.Println(reflect.TypeOf(username))
// 	fmt.Println(reflect.TypeOf(password))

// 	if username == "" || password == "" {
// 		c.JSON(200, response("10101", "username or password null", ""))
// 	} else if username != "admin" || password != "123" {
// 		c.JSON(200, response("10102", "username or password error", ""))
// 	} else {
// 		c.JSON(200, response("10200", "success", ""))
// 	}

// }


// func main() {
// 	r := gin.Default()

// 	/*
// 		简单额的接口
// 		http://127.0.0.1:8080/
// 	*/
// 	r.GET("/", func(c *gin.Context) {
// 		c.JSON(200, gin.H{
// 			"code":    "10200",
// 			"message": "success",
// 			"data":    "hello gin!",
// 		})
// 	})

// 	/*
// 		REST风格 GET请求
// 		http://127.0.0.1:8080/user/tom
// 	*/
// 	r.GET("/user/:name", func(c *gin.Context) {
// 		name := c.Param("name")
// 		c.JSON(200, gin.H{
// 			"code":    "10200",
// 			"message": "success",
// 			"data":    "hello, " + name,
// 		})
// 	})

// 	/*
// 		GET 请求
// 		http://127.0.0.1:8080/users?name=tom
// 	*/
// 	r.GET("/users", func(c *gin.Context) {
// 		name := c.Query("name")
// 		role := c.DefaultQuery("role", "tearcher")
// 		c.JSON(200, gin.H{
// 			"code":    "10200",
// 			"message": "success",
// 			"data":    name + " is a " + role,
// 		})
// 	})

// 	/*
// 		POST 请求
// 		http://127.0.0.1:8080/login
// 	*/
// 	r.POST("/login", func(c *gin.Context) {
// 		username := c.PostForm("username")
// 		password := c.PostForm("password")

// 		//判断返回值类型
// 		fmt.Println(reflect.TypeOf(username))
// 		fmt.Println(reflect.TypeOf(password))

// 		if username == "" || password == "" {
// 			c.JSON(200, response("10101", "username or password null", ""))
// 		} else if username != "admin" || password != "123" {
// 			c.JSON(200, response("10102", "username or password error", ""))
// 		} else {
// 			c.JSON(200, response("10200", "success", ""))
// 		}

// 	})

// 	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
// }
