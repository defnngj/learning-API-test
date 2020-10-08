# API base golang gin web framework

## go 环境安装

1. 下载golang
https://golang.org/doc/install

查看go版本

```shell
> go version
go version go1.15.2 darwin/amd64
```

2. 配置环境：GOROOT、GOPATH等

```shell
> go env

GO111MODULE="on"
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/fnngj/Library/Caches/go-build"
GOENV="/Users/fnngj/Library/Application Support/go/env"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOINSECURE=""
GOMODCACHE="/Users/fnngj/go/pkg/mod"
GONOPROXY=""
GONOSUMDB=""
GOOS="darwin"
GOPATH="/Users/fnngj/go"
GOPRIVATE=""
GOPROXY="https://mirrors.aliyun.com/goproxy/"
GOROOT="/usr/local/go"
GOSUMDB="sum.golang.org"
GOTMPDIR=""
GOTOOLDIR="/usr/local/go/pkg/tool/darwin_amd64"
GCCGO="gccgo"
AR="ar"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD="/Users/fnngj/go/src/godemo/go.mod"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/gj/tg9pvv8n5vd15sjtf5ndh7zh0000gn/T/go-build364476694=/tmp/go-build -gno-record-gcc-switches -fno-common"
```

3. 设置国内源

参考：https://goproxy.cn/

```shell
> go env -w GO111MODULE=on

> go env -w GOPROXY=https://goproxy.cn,direct
```

默认管理非官方库在 `$GOPATH\src\`，开启了 GO111MODULE 之后，此时将会到`$GOPATH\src\pkg\` 目录下。
通过 GOPROXY 修改代理为国内源。

4. 设置 go mod

使用`go mod` 管理项目，就不需要非得把项目放到`$GOPATH` 指定目录下，你可以在你磁盘的任何位置新建一个项目。

```shell
> cd goapi   # 进入web项目目录
> go mod init gin
> go mod edit -require github.com/gin-gonic/gin@latest
```

5. 安装gin

github地址：https://github.com/gin-gonic/gin

```shell
> go get -u github.com/gin-gonic/gin
```

## 创建 gin 项目

1. 根据官方例子创建 `api_server.go`

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/hello", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "code":    "10200",
            "message": "success",
            "data":    "hello gin!",
        })
    })
    r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
```

2. 运行`api_server.go`文件.

```shell
> go run example.go
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:	export GIN_MODE=release
 - using code:	gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /hello                    --> main.main.func1 (3 handlers)
[GIN-debug] Environment variable PORT is undefined. Using port :8080 by default
[GIN-debug] Listening and serving HTTP on :8080
```

3. 通过浏览器访问：`http://127.0.0.1:8080`

```json
{
    code: "10200",
    data: "hello gin!",
    message: "success"
}
```
