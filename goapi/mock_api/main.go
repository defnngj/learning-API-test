package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/mock/:number/*subpath", func(c *gin.Context) {
		/*
			支持 subpath URL
		*/
		number := c.Param("number")
		subpath := c.Param("subpath")
		c.JSON(http.StatusOK, gin.H{
			"number":  number,
			"subpath": subpath,
		})
	})

	r.GET("/check/status_code", func(c *gin.Context) {
		/*
			支持非200状态码
			http.StatusNotImplemented  指定 501
		*/
		c.JSON(http.StatusNotImplemented, gin.H{
			"message": "状态码 501",
		})
	})

	r.GET("/check/delay", func(c *gin.Context) {
		/*
			支持延迟返回
			3s 后返回结果
		*/
		var sec int = 3
		time.Sleep(time.Duration(sec) * time.Second)
		c.JSON(http.StatusOK, gin.H{
			"message": "delay 3s",
		})
	})

	r.GET("/check/header", func(c *gin.Context) {
		/*
			支持 header请求头
		*/
		var header = make(map[string]string)
		header["token"] = ""
		header["user"] = ""

		// 从header请求头中提取参数值
		for k, _ := range header {
			i := c.Request.Header.Get(k)
			header[k] = i
		}

		fmt.Printf("%+v\n", header)

		c.JSON(http.StatusOK, gin.H{
			"message": "ok",
			"header":  header,
		})
	})

	r.GET("/check/params", func(c *gin.Context) {
		/*
			支持 GET params 参数
		*/
		var param = make(map[string]string)
		param["id"] = ""
		param["name"] = ""
		param["is_delete"] = ""

		// 从请求URL中提取参数值
		for k, _ := range param {
			i := c.Query(k)
			param[k] = i
		}

		fmt.Printf("%+v\n", param)

		c.JSON(http.StatusOK, gin.H{
			"message": "params",
			"param":   param,
		})
	})

	r.POST("/check/data", func(c *gin.Context) {
		/*
			支持 POST from-datas/x-www-form-urlencoded 参数
		*/
		var param = make(map[string]string)
		param["id"] = ""
		param["name"] = ""

		// 从请求URL中提取参数值
		for k, _ := range param {
			value := c.PostForm(k)
			param[k] = value
		}

		fmt.Printf("%+v\n", param)

		c.JSON(http.StatusOK, gin.H{
			"message": "params",
			"data":    param,
		})
	})

	r.POST("/check/json", func(c *gin.Context) {
		/*
			支持 POST json 参数
		*/
		json := make(map[string]interface{}) //注意该结构接受的内容
		c.BindJSON(&json)
		log.Printf("%v\n", &json)

		c.JSON(http.StatusOK, gin.H{
			"message": "params",
			"json":    &json,
		})
	})

	r.POST("check/xml", func(c *gin.Context) {
		/*
			支持 body XML 格式数据
		*/
		body, _ := ioutil.ReadAll(c.Request.Body)
		println("body XML", string(body))

		// 查看完的数据重新放回去
		c.Request.Body = ioutil.NopCloser(bytes.NewReader(body))

		// 返回 XML
		// c.XML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
		// 返回 string
		c.String(http.StatusOK, string(body))
	})

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
