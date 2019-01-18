# NewsSpider
抓取新闻正文内容<br>
<br>
* 一、新浪滚动新闻定时抓取，数据存入mysql，通过找到共同的标签，利用正则提取<br>

* 二、百度新闻正文内容抓取（暂未添加定时功能），数据存入mysql，通过第三方库readability-lxml识别找到新闻的正文部分提取，有些许网站因网站结构不同故而提取存在问题<br>

<br>

## 网页正文提取

<https://www.cnblogs.com/zhengyou/p/3605458.html>

## Python

简介、简单理解、安装、使用、总结

<https://www.oschina.net/code/snippet_197184_14869>

### python-readability

#### 简介

Given a html document, it pulls out the main body text and cleans it up.

readability本是一个JS库（readability的js版本地址：<https://github.com/mozilla/readability>

），通过自动化提取算法对网页的Dom树进行改写，并在浏览器上展现页面抽取后的网页。这里是Python实现的readability，现已更新至readability
0.7

GitHub地址：<https://github.com/buriy/python-readability>

#### 简单理解

给readability的Document类传入一个html
text，Document会重新建立一个etree树，而summary()方法会遍历Dom对象，通过标签和常用文字的加减权，提取文本的正文（通过summary()提取的正文会带有标签，所以要得到纯净的正文需要自己clean）。

#### 安装

> pip install readability-lxml

#### 使用
```

**import** requests

**from** readability **import** Document

response **=** requests**.**get**(**'*http://example.com*'**)**

doc **=** Document**(**response**.**text**)**

doc**.**summary**()**
```

以<http://stock.10jqka.com.cn/20180817/c606560171.shtml>为例（此网站需要添加请求头）

得到：

![](media/f4384e7b33ba77ba3a145296a14346ef.png)

#### 总结

操作简单，容易得到正文，但是需要自己清洗标签；而且经过测试，抓取速度比较快

### newspaper

#### 简介

Inspired by [requests](https://github.com/kennethreitz/requests) for its
simplicity and powered by [lxml](http://lxml.de/) for its speed

作者从requests库的简洁与强大得到灵感，使用python开发的可用于提取文章内容的程序

Newspaper可以用来提取新闻、文章和内容分析。使用多线程，支持10多种语言等

GitHub地址： <https://github.com/codelucas/newspaper>

#### 简单理解

给Article传入两个参数，一个为url，一个为支持的语言（**这里对于中文语言应都添加为‘zh’，否则大部分网站都抓取不了**），生成一个article对象后，调用对象的download()方法，download在内部调用network的get_html_2XX_only方法，调用requests从而得到网页源码；parse()中包含文档清理以及输出格式化，对标签进行清理，可以得到正文的内容

#### 安装

> pip install newspaper3k （Python3以上的版本）

> pip install newspaper （Python2版本）

#### 使用

注意加上 language='zh' 否则大部分中文网站几乎提取不了，且支持多国语言
```

**from** newspaper **import** Article

article **=** Article**(**url**,** language**=**'zh'**)**

article**.**download**()**

article**.**parse**()**

**print(**article**.**text**)**
```

得到：

![](media/e0bd107f873814922800b7b542be2d70.png)

#### 总结

经过简单的初步测试，抓取同样的100条百度新闻，newspaper用了73秒，且提取的正文清晰，不用自己写清洗的工具；

readability用时43秒（在加了清洗的步骤之后）

两者提取到的正文内容相差不多，但是newspaper包含较多的功能，如提取关键字、提取日期、作者，封面图片等，功能更为全面丰富

### goose

#### 简介

Goose was originally an article extractor written in Java that has most recently
(Aug2011) been converted to a scala project.

This is a complete rewrite in Python. The aim of the software is to take any
news article or article-type web page and not only extract what is the main body
of the article but also all meta data and most probable image candidate.

Goose最初是一个用Java编写的文章提取器，最近（2011年8月）被转换为scala项目。

这是Python中的完全重写，该软件的目的是获取任何新闻文章或文章类型的网页，不仅提取文章的主体，而且提取所有元数据和最可能的图像候选

GitHub地址：<https://github.com/goose3/goose3> --可以使用pip安装

GitHub地址：<https://github.com/grangier/python-goose> --要从源安装

为了简便，使用goose3进行测试

#### 简单理解

在提取中文网站时，通过给Goose传递一个dict，包含指定的StopWord分析器（StopWordsChinese），传递给配置对象，这样就做好了中文配置，生成一个Goose对象；

调用extract()方法，此时配置生效，StopWordsChinses通过jieba分词处理（构建一个树会消耗一些时间，所以如果不是中文网站的话，尽量避免使用jieba）最后返回article

随后调用cleaned_text()方法得到一个没有标签的纯净文本，调用title()可以得到文章的标题

#### 安装

> pip install goose3

#### 使用
```

**from** goose3 **import** Goose

**from** goose3**.**text **import** StopWordsChinese

中文需要一个专门的StopWord分析器，需要传递给配置对象

g **=** Goose**({**'stopwords_class'**:** StopWordsChinese**})**

article **=**
g**.**extract**(**url**=**'*http://news.k618.cn/society/201808/t20180817_16594036.html*'**)**

**print(**article**.**cleaned_text**)**

**print(**article**.**title**)**
```

![](media/e4748fa8de9e57f08cf1ce5e8f1e8fa8.png)

#### 总结

提取同样100条新闻正文所需时间为50秒，提取内容清晰；

同样也可提取标题，网页编码格式，但对中文网站的发布时间及作者还是不能够准确提取
； 支持多种语言；

goose有几个不同的源，包括goose3、python-goose，所以在使用不同的goose需注意

### boilerpipe

#### 简介

A python wrapper for Boilerpipe, an excellent Java library for boilerplate
removal and fulltext extraction from HTML pages.

一个引用于Boilerpipe的python包装器，一个用于从HTML页面中删除样板文件和提取全文内容的优秀Java库

GitHub地址：<https://github.com/misja/python-boilerpipe>

#### 简单理解

底层用的是jpype 暂略。

#### 安装

解压从GitHub下载的压缩包，通过命令行进入解压好的文件夹，通常会看见一个 setup.py
的文件。打开命令行，进入该文件夹。运行 python setup.py install

而要使用boilerpipe 还需要jpype、jdk

Python3下载安装jpype：<https://www.lfd.uci.edu/~gohlke/pythonlibs/>

> pip install wheel

待wheel安装好以后，在安装已经下载的JPype1-0.6.2-cp36-cp36m-win_amd64.whl 文件

> pip install JPype1-0.6.2-cp36-cp36m-win_amd64.whl

安装完后如果运行程序，报ImportError: numpy.core.multiarray failed to
import这个错误，是numby库没有安装，再安装numby库

> Pip install numpy

之后在运行若有No such file or directory: 'C:\\\\Program
Files\\\\Java\\\\jre7\\\\bin\\\\client\\\\jvm.dll'

这个错误，则建议重装jdk，之后找到对应的bin目录下，若发现只有server文件夹而没有client文件夹，那么建议复制一个server命名为client（server文件夹中有jvm.dll）

#### 使用
```

**from** boilerpipe**.**extract **import** Extractor

extractor **=** Extractor**(**extractor**=**'ArticleExtractor'**,**
url**=**your_url**)**
```

提取正文

`extracted_text **=** extractor**.**getText**()**`

提取html

`extracted_html **=** extractor**.**getHTML**()**`

#### 总结

安装过程较为复杂；

可以自己选择抽取出的正文内容格式：可以是纯文本的，也可以是携带HTML的；

且测试时对于传入url的情况，由于网页编码不同所以常会报错，对于这种情况，可以传入一个html：
```

extractor **=** Extractor**(**extractor**=**'ArticleExtractor'**,**
html**=**your_html**)**
```

然后通过正则根据不同网页的编码来提取，这样也能做到抓取100同样的新闻耗时为43秒，但是检查后发现抓取的内容虽是正文但是往往只有一部分内容!
；

boilerpipe也有不同的提取方式，这些还未带测试（ArticleExtractor用于提取正文，KeepEverythingWithMinKWordsExtractor用于提取分类的名称）

可能还有更好的用法……

### decruft

#### 简介

“decruft is a fork of python-readability to make it faster. It also has some
logic corrections and improvements along the way.”
（引自：http://www.minvolai.com/blog/decruft-arc90s-readability-in-python/）

decruft是Python
readability的fork版本，其主要提高了readability的速度。decruft的源码是放在Goolge上的，发现他只有0.1版本，而且是10年9月的，但是Python-readability一直在更新的，其核心的readability.py是7个月前更新的，所以不能保证decruft的性能要比现在的readability好

GitHub地址：<https://github.com/dcramer/decruft>

未测试，应该与readability相近

## Java

### Cx-extractor

#### 简介

google地址：<http://cx-extractor.googlecode.com>

GitHub地址：<https://github.com/jiangzhuo/cx-extractor>

基于行块的分布来提取网页中的正文

提取的方法是首先使用Jsoup来获取网页的内容，之后将内容传给cx-extractor，交由其来解析

#### 使用

核心代码如下所示：
```

// 通过Jsoup来获取html，在此设置了范文数据包的头部，因为有些网站会屏蔽爬虫。

String content **=** Jsoup**.**connect**(**url**).**userAgent**(**"Mozilla/5.0
(jsoup)"**).**get**().**html**();**

// html_article即为解析出的正文。

String html_article **=** CXTextExtract**.**parse**(**content**);**
```

#### 总结

这个库有时候会有错误，会将不属于正文的内容提取出来，例如一些无关的底部内容，或者一些链接。但性能比较高，约几十毫秒

### Boilerpipe

#### 简介

google地址：<http://code.google.com/p/boilerpipe/>

GitHub地址：<https://github.com/kohlschutter/boilerpipe>

基于网页dom树来解析，内部有多种解析器，比较准确，但是时间在100毫秒左右。

#### 使用

核心代码如下所示：
```

String content = Jsoup.connect(url).userAgent("Mozilla/5.0
(jsoup)").get().html();

// 使用Bolierpipe来获取网页正文内容

String parse_article = ArticleExtractor.INSTANCE.getText(content);
```

#### 总结

结果比较准确，性能比稍慢，大约在100毫米左右。

### ContentExtractor

new address <https://github.com/CrawlScript/WebCollector>

#### 简介

ContentExtractor是一个开源的网页正文抽取工具，用JAVA实现，具有非常高的抽取精度。

GitHub地址：<https://github.com/hfut-dmic/ContentExtractor>

#### 算法

ContentExtractor的网页正文抽取算法使用的是CEPR，适用于几乎所有的包含正文的网页。

算法简介：<http://dl.acm.org/citation.cfm?id=2505558>

#### 使用

ContentExtractor的接口非常简单，用户可以根据网页的url，或者网页的html，来进行网页正文抽取：

根据url，抽取网页的正文：
```

public static void main**(**String**[]** args**) throws** Exception **{**

String content**=**ContentExtractor**.**getContentByURL**(url**);

System**.**out**.**println**(**content**);**

**}**
```

根据html，抽取网页的正文：

```
**public static void** main**(**String**[]** args**) throws** Exception **{**

String html**=**"获取到的html源码"**;**

String content**=**ContentExtractor**.**getContentByHtml**(**html**);**

System**.**out**.**println**(**content**);**

**}**
```

#### 导入

从ContentExtractor的github主页https://github.com/hfut-dmic/ContentExtractor上下载ContentExtractor-{版本号}-bin.zip；

将解压后得到的jar包全部放到工程的build path即可

### Jreadability

#### 简介

JReadability是一个Java库，它将HTML解析并返回干净、易于阅读的文本

JReadability是arc90最初Javascript项目可读性的一个Java端口。(原来的可读性。js项目现在被迁移成一个服务器端平台，这个平台已经不再是开源的了)

GitHub地址：<https://github.com/wuman/JReadability>

#### 使用

Readability通过任何一个提供的构造函数实例化该类，具体取决于感兴趣的HTML页面的来源（html文档或url）：
```

Readability readability **= new** Readability**(**html**);** // String

Readability readability **= new** Readability**(**url**,** timeoutMillis**);**
// URL

通过运行启动内容提取：

readability**.**init**();**

输出是HTML格式的干净，可读的内容。您可以使用以下命令获取输出：

String cleanHtml **=** readability**.**outerHtml**();**

默认情况下，使用打印调试日志System.out.println()。您也可以通过覆盖dbg()
方法来使用自己的日志记录机制。例如，在Android上，您可以选择这样做：

Readability readability **= new** Readability**(**html**) {**

\@Override

protected void dbg**(**String msg**) {**

Log**.**d**(**LOG_TAG**,** msg**);**

**}**

\@Override

protected void dbg**(**String msg**,** Throwable t**) {**

Log**.**e**(**LOG_TAG**,** msg**,** t**);**

**}**

**};**
```

#### 导入

1、可以下载已发布的jar文件

2、如果使用Maven构建项目，则只需向此库添加依赖项即可
```

\<dependency\>

\<groupId\>com.wu-man\</groupId\>

\<artifactId\>jreadability\</artifactId\>

\<version\>1.3\</version\>

\</dependency\>
```

## Php

爬虫框架：<https://github.com/owner888/phpspider>

其他源的readability

GitHub地址：<https://github.com/andreskrey/readability.php>

### php-readability

#### 简介

解析html文本（通常是新闻和其他文章）并返回标题，作者，主图像和文本内容，过滤导航栏，广告，页脚或任何不是文本主体的内容。分析每个节点，给他们一个分数，并确定什么是相关的，什么可以丢弃。

GitHub地址：<https://github.com/feelinglucky/php-readability>

#### 安装、使用

`\$ sudo apt-get install php7.1-xml php7.1-mbstring`

要求：PHP 5.6+, ext-dom, ext-xml, and ext-mbstring（依赖）
```

**use andreskrey\\Readability\\Readability;**

**use andreskrey\\Readability\\Configuration;**

**\$readability = new Readability(new Configuration());**

**\$html = file_get_contents('http://your.favorite.newspaper/article.html');**

**try {**

**\$readability-\>parse(\$html);**

**echo \$readability;**

**} catch (ParseException \$e) {**

**echo sprintf('Error processing text: %s', \$e-\>getMessage());**

**}**
```

## Node.js

### arex

#### 简介

node.js实现自动提取文章正文， 标题， 发布日期。自动生成文章摘要

GitHub地址：<https://github.com/ahkimkoo/arex>

#### 安装

> npm install arex

#### 使用

`**var** arex **=** require**(**'arex'**);**`

//example 1, 给定网址自动抓取，提取正文，生成摘要
```

arex**.**get_article**(**'http://finance.sina.com.cn/consume/puguangtai/2016-03-15/doc-ifxqhmve9227502.shtml'**,**120**,(**err**,**result**)=\>{**

//120: 摘要长度为120，如果不需要生成摘要此参数传入false.

//result: {"title":"...","content":"....", "summary":"...", "pubdate":"..."}

console**.**log**(**result**['content']);**

**});**
```

//example 2, 给html内容，提取正文，生成摘要

```
result **=**
arex**.**get_article_sync**(**'\<html.........\</html\>'**,**120**);**

//result: {"title":"...","content":"....", "summary":"...", "pubdate":"..."}

//example 3, 给html内容，生成摘要

//summarize(content, exptd_len=120, shingle=false, min=150, max=350, filter=[],
title)

//shingle的意义:
以摘要长度的句子组合为单位计算权重，shingle为false则以自然句为单位计算权重,
filter是过滤规则，符合规则的段落都会被过滤不作为摘要

**var** summary **=** arex**.**summarize**(**'\<html\>.......\</html\>'**,**
120**, true);**

**var** summary **=** arex**.**summarize**(**'\<html\>.......\</html\>'**,**
0.04**, true,** 100**,** 300**);**

//摘要长度比例 4%, 最短 100, 最长 300
```

#### 算法说明

正文抽取: 基于行块密度分布来抽取正文， 每个行块由若干自然段落组成

标题抽取: 分别从正文附近抽取h1标签，从title标签取值，取最可能是标题的那一个

发布日期抽取: 用正则表达式抽取正文附近的日期（有误差）

自动文摘: sentense rank算法，参照pagerank算法的实现，可以指定期望的文摘长度

优化点：加入了神经网络模型判断一句话是否适合作为摘要

### readability

GitHub地址：

<https://github.com/arrix/node-readability/>

<https://github.com/luin/readability>

建议使用<https://github.com/luin/readability>由于<https://github.com/arrix/node-readability/是8>年前的版本，下文也是对luin/readability的简单介绍

#### 简介

将任何web页面转换为干净的视图，这个模块基于arc90的readability

GitHub地址：<https://github.com/luin/readability>

#### 安装

> \$ npm install node-readability

注意，从v2.0.0开始，这个模块只支持node.js \> = 2.0的版本

若要在node.js 1.x版本中使用 则是：

> \$ npm install node-readability\@1

#### 使用

read(html [, options], callback)

1、html 可以是url 或 html code.

2、options 一个可选的选择对象：

-   cleanRulers 允许设置自己的验证规则

-   preprocess
    应该是一个函数，用于检查或修改下载的源代码，然后将其传递给readability

3、callbac运行回调 run - callback(error, article, meta)

例子
```

var read **=** require**(**'node-readability'**);**

read**(url,** function**(**err**,** article**,** meta**) {**

// Main Article

console**.**log**(**article**.**content**);**

// Title

console**.**log**(**article**.**title**);**

// HTML Source Code

console**.**log**(**article**.**html**);**

// DOM

console**.**log**(**article**.**document**);**

// Response Object from Request Lib

console**.**log**(**meta**);**

// Close article to clean up jsdom and prevent leaks

article**.**close**();**

**});**
```

## .Net

### Html2Article

#### 简介

.NET平台下，一个高效的从Html中提取正文的工具。

正文提取采用了基于文本密度的提取算法，支持从压缩的Html文档中提取正文，每个页面平均提取时间为30ms，正确率在95%以上。

GitHub地址：<https://github.com/stanzhai/Html2Article>

标签无关，提取正文不依赖标签；

支持从压缩的html文档中提取正文内容；

支持带标签输出原始正文；

核心算法简洁高效，平均提取时间在30ms左右

#### 使用

> PM\> Install-Package Html2Article

引入命名空间using StanSoft;

添加如下代码：
```

// html为你要提取的html文本

string html = "\<html\>....\</html\>";

//
article对象包含Title(标题)，PublishDate(发布日期)，Content(正文)和ContentWithTags(带标签正文)四个属性

Article article = Html2Article.GetArticle(html);
```

#### 总结

Html2Article类是提取正文的核心类

Html2Article配置说明：

AppendMode：是否使用正文追加模式，默认为false，设置为true会将更多符合条件的文本添加到正文。

Depth：分析的深度，默认为5，对于行空隙较大的页面可增加此值。

LimitCount：字符限定数，当分析的文本数量达到限定数则认为进入正文内容，默认为180个字符。

GetArticle(string html)：从Html文本中获取Article。
