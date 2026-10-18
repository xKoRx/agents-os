package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) == 4 && os.Args[1] == "mlist" {
		if err := runMinioList(os.Args[2], os.Args[3]); err != nil {
			fmt.Println("MINIO_LIST_ERROR:", err)
			os.Exit(1)
		}
		return
	}
	if len(os.Args) == 5 && os.Args[1] == "mget" {
		if err := runMinioGet2(os.Args[2], os.Args[3], os.Args[4]); err != nil {
			fmt.Println("MINIO_GET_ERROR:", err)
			os.Exit(1)
		}
		return
	}
	fmt.Println("usage: miotool mlist <bucket> <prefix> | mget <bucket> <key> <out>")
	os.Exit(2)
}
