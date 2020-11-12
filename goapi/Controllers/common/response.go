package common

import "github.com/gin-gonic/gin"

/*
	封装接口返回 response 格式
*/
func Response(code string, message string, data string) gin.H {
	resp := gin.H{
		"code":    code,
		"message": message,
		"data":    data,
	}
	return resp
}