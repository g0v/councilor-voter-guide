
### 檔案結構
	dist/		  <---發布產生檔案
	src/   		  <---開發用原始檔
		css/
		img/
		js/
		js-es2015/
		less/     <----樣式
		lib/
		pug/
			head.pug  header區塊
			nav.pug   選單區塊
			template.pug  公板
		*.pug


### 頁面架構: 
	首頁
		index.html

	縣市長:
		-區域
		county-mayor-area.html
		-歷任縣市長
		county-mayor.html
	履歷:
		resume-profile.html 
		resume-fund.html 
		resume-video.html 
		resume-fund.html 
		resume-contribution.html
		resume-politics.html



### 資源:
	bootstrap, jQuery, Slick, Font Awsome, GSAP

====================================================

### 開發環境  
	需安裝node & npm (latest stable version)

### 安裝 
	在./ (有package.json的目錄) 執行npm i
    
### 編譯 
	執行npm run dev
	
### 編譯 for production 
	執行npm run bu
