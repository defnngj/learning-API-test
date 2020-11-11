package common

/*
	封装接口返回respsonse格式
*/
func response(code string, message string, data string) gin.H {
	resp := gin.H{
		"code":    code,
		"message": message,
		"data":    data,
	}
	return resp
}