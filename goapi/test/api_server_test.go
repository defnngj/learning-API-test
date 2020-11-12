package test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"goapi/router"
)

func TestHelloRoute(t *testing.T) {

	router := router.InitRouter()
	w := httptest.NewRecorder()

	req, _ := http.NewRequest("GET", "/api/v1/", nil)
	router.ServeHTTP(w, req)

	assert.Equal(t, 200, w.Code)
	assert.Equal(t, "{\"code\":\"10200\",\"data\":\"hello gin!\",\"message\":\"success\"}", w.Body.String())
}
