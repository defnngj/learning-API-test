package main

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"

	"github.com/gin-gonic/gin"
)

func proxy(c *gin.Context) {
	proxyPath := c.Param("proxyPath")
	fmt.Printf("proxyPath: %+v\n", proxyPath)

	remote, err := url.Parse("https://httpbin.org")
	if err != nil {
		panic(err)
	}

	proxy := httputil.NewSingleHostReverseProxy(remote)

	mockMode := c.Request.Header.Get("mock-mode")
	fmt.Println("headers: mock-mode=", mockMode)
	if mockMode == "1" {
		// 代理到指定的服务
		// 设置 Header 请求头
		c.Request.Header.Set("cookie", "xxxxx")
		proxy.Director = func(req *http.Request) {
			req.Header = c.Request.Header
			req.Host = remote.Host
			req.URL.Scheme = remote.Scheme
			req.URL.Host = remote.Host
			req.URL.Path = c.Param("proxyPath")
		}

		proxy.ServeHTTP(c.Writer, c.Request)

	} else {
		// 服务自己处理
		c.JSON(http.StatusOK, gin.H{
			"message": "mock server",
		})
	}

}

func main() {

	r := gin.Default()

	// 创建路由
	r.Any("/*proxyPath", proxy)

	r.Run(":8085")
}
