import re
import requests
import os
import datetime
import time
import sys

def writejianjie(contents,filePath):
    with open(sys.path[0]+'\\'+filePath,'a',encoding='utf-8') as ff:#创建jianjie
        ff.write(contents)
    return

def selectBook(bookNames,tezheng,introduce,auther):
    while True:
        ipt=input().strip().lower()#获取指令
        num=re.findall('.([0-9]+)',ipt,re.S)#正则抓取数字
        if 'ls' in ipt:#输出结果                            #参数识别
            for i in range(len(bookNames)):
               print(str(i)+' '+bookNames[i])
        elif 'bk' in ipt:#返回搜索
            return
        elif 'help' in ipt:#输出可用指令
            print('ls\n')
            print('List the title of the book\n')
            print('bk\n')
            print('Return to search\n')
            print('dt <num>\n')
            print('Show the details of the book\n')
            print('pa <num>\n')
            print('Crawling book\n')
        elif 'dt' in ipt:#输出书本细节
            if int(num[0])>len(tezheng):
                print('Index out of range')
                if '-d' in ipt:#进入书本主页爬取并输出细节
                    (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng[int(num[0])])
                    print('Title: 《'+zhuyebookname[0]+'》')
                    print('Auther: '+zhuyebookauther[0])
                    print(zhuyebookintroduction[0])
                else:#直接输出细节
                    print('Title: 《'+bookNames[num]+'》')
                    print('Auther: '+auther[num])
                    print(introduce[num])
        elif 'pa' in ipt:#爬书
            (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng[int(num[0])])
            paxsbqgTraversalChapter(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[int(num[0])])
            return

def paxsbqgSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.xsbiquge.com/search.php?keyword='+keyword).content.decode('utf-8')#请求搜索数据
    searchHtmlResult=searchHtmlResult.replace('\t\t\t\t','')#除去不明所以的四个'\t'
    searchBookNames=re.findall('title="(.*?)" class="result-game-item-title-link" target="_blank">\r\n',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<a cpos="title" href="https://www.xsbiquge.com/(.*?)/"',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<p class="result-game-item-desc">(.*?)</p>\r\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<span>\r\n                            (.*?)\r\n                        </span>',searchHtmlResult,re.S)#正则抓取作者
    for i in range(len(searchtezheng)):#遍历输出结果
        print(str(i)+' '+searchBookNames[i])
    print("Note: due to unknown reasons, we can't get all the results of xsbiquge.com's search interface")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def paxsbqgzhuye(xiaoshuohao):#xsbiquge.com
    url="https://www.xsbiquge.com/"+xiaoshuohao+"/"
    html=requests.get(url).content.decode('utf-8')#请求数据
    emptychapter=re.findall('<dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>',html,re.S)#正则筛选   <dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>
    for i in range(len(emptychapter)):#遍历去除
        html=html.replace(emptychapter[i],emptychapter[i].replace(' class="empty"',''))
    html_str=re.findall('<dd><a href="/'+xiaoshuohao+'/.*?.html">.*?</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookname=re.findall('/>\\r\\n<meta property="og:title" content="(.*?)"',html,re.S)#正则抓取书名
    bookauther=re.findall('/>\\r\\n<meta property="og:novel:author" content="(.*?)"',html,re.S)#正则抓取作者
    bookintroduction=re.findall('/>\r\n<meta property="og:description" content="(.*?)"',html,re.S)#正则抓取简介
    return(url,html_str,bookname,bookauther,bookintroduction)

def paxsbqgTraversalChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,singleChapterOutPut):
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入书名
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入作者
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入简介
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入获取的章节数
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入获取的章节数至总文件
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    for i in range(len(html_str)):#遍历章节
        ii=i
        SingleChapterOutPut=singleChapterOutPut
        success=paxsbqgChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,ii,SingleChapterOutPut)
        if success==True:
            print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        else:
            chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
            print('Error: '+chapterName[0])
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(html_str))+' seconds per chapter\n')

def paxsbqgChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,i,singleChapterOutPut):
    writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
    chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
    chapterFeature=re.findall('<dd><a href="/'+xiaoshuohao+'/(.*?).html',html_str[i],re.S)#获取章节URL特征
    chapterUrl='https://www.xsbiquge.com/'+xiaoshuohao+'/'+chapterFeature[0]+'.html'#拼接章节URL
    try:
        chapterName[0]=chapterName[0].replace('\\','[反斜杠]')#去除反斜杠
    except:#出错处理
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    chapterName[0]=chapterName[0].replace('/','[斜杠]')#去除斜杠
    chapterName[0]=chapterName[0].replace(':','[半角冒号]')#去除半角冒号
    chapterName[0]=chapterName[0].replace('*','[星号]')#去除星号
    chapterName[0]=chapterName[0].replace('?','[半角问号]')#去除半角问号
    chapterName[0]=chapterName[0].replace('"','[半角双引号]')#去除半角双引号
    chapterName[0]=chapterName[0].replace('<','[小于号]')#去除小于号
    chapterName[0]=chapterName[0].replace('>','[大于号]')#去除大于号
    chapterName[0]=chapterName[0].replace('|','[竖线]')#去除竖线
    try:
        chapter=requests.get(chapterUrl).content.decode('utf-8')#请求数据
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
    try:
        text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    else :
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','\n')#处理换行
        if singleChapterOutPut==True:#是否输出单章
            with open(os.getcwd()+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                f.write(str(i)+' '+text[0])#写入正文与节号至分文件
        writejianjie(str(i)+' '+chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名与节号至总文件
        writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
        print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        return True

def padingdianSearchPage(keyword):#未完成
    keyword=keyword.encode('gbk')
    keyword=str(keyword).replace('\\x','%').replace("b'",'').replace("'",'')
    searchHtmlResult=requests.get('https://so.biqusoso.com/s1.php?siteid=booktxt.net&q='+str(keyword)).content.decode('utf-8')#请求搜索数据
    searchBookNames=re.findall('<span class="s2"><a href="http://www.booktxt.net/book/goto/id/.[0-9]+" target="_blank">(.*?)</a></span>',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<span class="s2"><a href="http://www.booktxt.net/book/goto/id/(.[0-9]+)" target="_blank">.*?</a></span>',searchHtmlResult,re.S)#正则抓取网址
    for i in range (len(searchtezheng)):#为不存在的简介填充
        searchtezheng[i]=searchtezheng[i][0]+'_'+searchtezheng[i]
    searchIntroduce=[0 for i in range(len(searchBookNames))]
    for i in range(len(searchBookNames)):#处理特征以使之能被直接与URL组合
        searchIntroduce[i]=''
    searchAuther=re.findall('<span class="s4">(.[^<>]+)</span>',searchHtmlResult,re.S)#正则抓取作者
    for i in range(len(searchtezheng)):#遍历输出结果
        print(str(i)+' '+searchBookNames[i])
    print("Note: booktxt.net will not display a introduction to each book on the search page")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def padingdianzhuye(xiaoshuohao):#booktxt.net
    url='https://www.booktxt.net/'+xiaoshuohao+'/'
    html=requests.get(url).content.decode('gbk')#请求数据
    bookname=re.findall('<h1>(.*?)</h1>',html,re.S)#正则抓取书名
    bookauther=re.findall('<meta property="og:novel:author" content="(.*?)"/>',html,re.S)#正则抓取作者
    bookintroduction=re.findall('<meta property="og:description" content="(.*?)"/>',html,re.S)#正则抓取简介
    bookintroduction[0]=bookintroduction[0].replace(r'\r\n', "")
    garbage=re.findall('<!doctype html>.*<dt>《'+bookname[0]+'》正文',html,re.S)#顶点在正文前面有几个最新章节的链接，去除正文前面所有的内容
    html=html.replace(garbage[0],'')
    html_str=re.findall('<dd><a href ="[0-9]+.html">.*?</a></dd>\r\n\t\t',html,re.S)#正则抓取章节名与URL特征
    return(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao)

def padingdianTraversalChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,singleChapterOutPut):#未完成
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')  #写入书籍相关信息至报告文件
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:  #创建总文件
        f.write('')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')  #写入书籍相关信息至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    for i in range(len(html_str)):#遍历章节
        ii=i
        SingleChapterOutPut=singleChapterOutPut
        success=paxsbqgChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,ii,SingleChapterOutPut)
        if success==True:
            print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        else:
            chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
            print('Error: '+chapterName[0])
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(html_str))+' seconds per chapter\n')

def padingdianChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,i,singleChapterOutPut):
    writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
    chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
    chapterFeature=re.findall('<a href ="([0-9]+).html">',html_str[i],re.S)#获取章节URL特征
    chapterUrl='https://www.booktxt.net/'+xiaoshuohao+'/'+chapterFeature[0]+'.html'#拼接章节URL
    try:                                                                                                #不记得为什么要这么做了
        chapterName[0]=chapterName[0].replace('\\','[反斜杠]')#去除反斜杠
    except:#出错处理
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        print('Error: Section'+i)
        return False
    else:
        chapterName[0]=chapterName[0].replace('/','[斜杠]')#去除斜杠
        chapterName[0]=chapterName[0].replace(':','[半角冒号]')#去除半角冒号
        chapterName[0]=chapterName[0].replace('*','[星号]')#去除星号
        chapterName[0]=chapterName[0].replace('?','[半角问号]')#去除半角问号
        chapterName[0]=chapterName[0].replace('"','[半角双引号]')#去除半角双引号
        chapterName[0]=chapterName[0].replace('<','[小于号]')#去除小于号
        chapterName[0]=chapterName[0].replace('>','[大于号]')#去除大于号
        chapterName[0]=chapterName[0].replace('|','[竖线]')#去除竖线
        while True:
            try:
                chapter=requests.get(chapterUrl).content.decode('gbk','ignore')#请求数据，dingdian偶尔会在正常的章节出现莫名其妙的非法字符，只能忽略，但是dingdian似乎只使用gbk所以看起来不会有什么问题
            except:
                chapter=''
            if chapter!='':
                break
    try: #如果出错意味着该章节没有内容
        text=re.findall('<div id="content">(.*?).[0-9!-<>]?<br /><br /><script>chaptererror()',chapter,re.S)#正则抓取正文，未能解决为什么会变为tuple而不是list
        text[0]=text[0][0]#将元组内容提出并重新为列表赋值
    except:#输出报告
        writejianjie('There is no content in section '+str(i)+'('+chapterName[0]+')'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
        writejianjie('There is no content in section '+str(i)+'('+chapterName[0]+')''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
        print('Error: '+chapterName[0])
        return False
    else:
        text[0]=text[0].replace('\u3000\u3000\u3000\u3000','\u3000\u3000')#替换四重空格
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','').replace('\r\r','\r')#处理换行
        if singleChapterOutPut==True:#是否输出单章
            with open(os.getcwd()+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                f.write(str(i)+' '+text[0])#写入正文与节号至分文件
        writejianjie(chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名至总文件
        writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
        return True

def paxswSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.xiashuwu.com/search.html?searchkey='+keyword+'&searchtype=all').content.decode('utf-8')#请求搜索数据
    searchBookNames=re.findall('《<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank">(.*?)</a>》</h3></div>\n<div class="pic">\n<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank"><img ',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('《<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank">.*?</a>》</h3></div>\n<div class="pic">\n<a href="/api/search/index/id/([0-9]+?)/type/www/" target="_blank"><img ',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<div class="intro">&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<div class="nickname">(.*?) / 著</div>\n',searchHtmlResult,re.S)#正则抓取作者
    for i in range(len(searchtezheng)):#遍历输出结果
        print(str(i)+' '+searchBookNames[i])
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def paxswzhuye(xiaoshuohao):#xiashuwu.com#未完成
    #下书网
    #https://www.xiashuwu.com/
    #傻逼华附
    #需要使用的库文件在外面
    #又是一个只能在家里做的东西
    #而且似乎在学校不一定能用
    #(searchBookNames,searchtezheng,searchIntroduce,searchAuther)=paxswSearchPage('霸道')
    #paxswzhuye(searchtezheng)
    url="https://www.xsbiquge.com/"+xiaoshuohao+"/"
    html=requests.get(url).content.decode('utf-8')#请求数据
    emptychapter=re.findall('<dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>',html,re.S)#正则筛选   <dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>
    for i in range(len(emptychapter)):#遍历去除
        html=html.replace(emptychapter[i],emptychapter[i].replace(' class="empty"',''))
    html_str=re.findall('<dd><a href="/'+xiaoshuohao+'/.*?.html">.*?</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookname=re.findall('/>\\r\\n<meta property="og:title" content="(.*?)"',html,re.S)#正则抓取书名
    bookauther=re.findall('/>\\r\\n<meta property="og:novel:author" content="(.*?)"',html,re.S)#正则抓取作者
    bookintroduction=re.findall('/>\r\n<meta property="og:description" content="(.*?)"',html,re.S)#正则抓取简介
    return(url,html_str,bookname,bookauther,bookintroduction)

def paxswChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao):#未完成
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入书名
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入作者
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入简介
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入获取的章节数
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入获取的章节数至总文件
    for i in range(len(html_str)):#遍历章节
        writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
        chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
        chapterFeature=re.findall('<dd><a href="/'+xiaoshuohao+'/(.*?).html',html_str[i],re.S)#获取章节URL特征
        chapterUrl='https://www.xsbiquge.com/'+xiaoshuohao+'/'+chapterFeature[0]+'.html'#拼接章节URL
        try:
            chapterName[0]=chapterName[0].replace('\\','[反斜杠]')#去除反斜杠
        except:#出错处理
            writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
            writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
            writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
            writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
            print('Error: Section'+i)
        else:
            chapterName[0]=chapterName[0].replace('/','[斜杠]')#去除斜杠
            chapterName[0]=chapterName[0].replace(':','[半角冒号]')#去除半角冒号
            chapterName[0]=chapterName[0].replace('*','[星号]')#去除星号
            chapterName[0]=chapterName[0].replace('?','[半角问号]')#去除半角问号
            chapterName[0]=chapterName[0].replace('"','[半角双引号]')#去除半角双引号
            chapterName[0]=chapterName[0].replace('<','[小于号]')#去除小于号
            chapterName[0]=chapterName[0].replace('>','[大于号]')#去除大于号
            chapterName[0]=chapterName[0].replace('|','[竖线]')#去除竖线
            try:
                chapter=requests.get(chapterUrl).content.decode('utf-8')#请求数据
            except:#出错处理
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
                print('Error: '+chapterName[0])
            text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
            try:
                text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
            except:#出错处理
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
                print('Error: '+chapterName[0])
            else :
                    text[0]=text[0].replace('&nbsp;','')#去除无用html标签
                    text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
                    text[0]=text[0].replace('<br />','\n')#处理换行
                    with open(sys.path[0]+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                        f.write(str(i)+' '+text[0])#写入正文与节号至分文件
                    writejianjie(str(i)+' '+chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名与节号至总文件
                    writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
                    print('Completed: '+str(i)+' '+chapterName[0])

def getKeyWord():
    ipt=input('Please enter KeyWords: ')
    return ipt

def getbooks(keyWord):
    keyWord=keyWord

while True:
    keyWord=getKeyWord()
    (searchBookNames,searchtezheng,searchIntroduce,searchAuther)=paxsbqgSearchPage(keyWord)
    selectBook(searchBookNames,searchtezheng,searchIntroduce,searchAuther)

#www.iqishu.la
#http://www.iqishu.la/search.html?searchkey=q
#记录工作进度的文件以支持断点续连
#url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao
#已完成的章节名
#书籍连载情况