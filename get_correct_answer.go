package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"

	"github.com/anaskhan96/soup"
)

var infile = flag.String("i", "data.json", "题库文件")
var outfile = flag.String("o", "get_correct_answer.txt", "答案文件")
var usage = `
Usage: gml2json [options...]

Options:
  -i    题库文件. (default: "data.json")
  -o    答案文件. (default: "get_correct_answer.txt")

Example:

  get_correct_answer -i data.json -o get_correct_answer.txt
`

func init() {
	flag.Usage = func() {
		fmt.Fprint(os.Stderr, usage)
	}
	flag.Parse()
}

func main() {
	fmt.Printf("输入url地址:")
	var url string
	fmt.Scanf("%s", &url)
	if url != "" {
		url += "&pageSize=50"
		url = strings.Replace(url, "startAnswerQuestion", "getQuestions", -1)

		jsonstr := readfile(infile)

		str := map[string]map[string]string{}
		json.Unmarshal(jsonstr, &str)

		//log.Println(str[1])
		resp, err := soup.Get(url)
		if err != nil {
			log.Fatalf("URL读取失败.%v", err)
		}
		var questions string
		doc := soup.HTMLParse(resp)
		for _, content := range doc.FindAll("div", "class", "txtMg") {
			question_content := content.Find("span").Text()                            //找到题目内容
			question_id := content.Find("input", "type", "radio").Attrs()["class"][9:] //找到题目编号

			question := strings.Repeat("=", 50) + "\r\n"
			question += question_content + "\r\n\r\n"
			question += str[question_id]["answer"] + "\r\n" //匹配题库答案
			questions += question
		}
		savefile(*outfile, questions)
	}
}

//读取题库文件
func readfile(filename *string) []byte {
	ifile, err := ioutil.ReadFile(*filename)
	if err != nil {
		log.Fatalf("读取题库文件: [%s] 出错! %v\n", *filename, err)
	}
	log.Printf("已成功读取题库文件: [%s] ", *filename)

	return []byte(ifile)
}

//保存答案文件
func savefile(file, context string) {
	ofile, err := os.OpenFile(file, os.O_WRONLY|os.O_TRUNC|os.O_CREATE, 0666)
	if err != nil {
		log.Fatalln(err)
	}
	defer ofile.Close()

	ofile.WriteString(context)
	log.Printf("成功保存答案文件: [%s] \n", file)
}
