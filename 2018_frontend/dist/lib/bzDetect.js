// JavaScript Document
    isIE = navigator.userAgent.search("MSIE") > -1; 
    isIE7 = navigator.userAgent.search("MSIE 7") > -1; 
    isIE8 = navigator.userAgent.search("MSIE 8") > -1; 
    isIE9 = navigator.userAgent.search("MSIE 9") > -1; 
    isIE10 = navigator.userAgent.search("MSIE 10") > -1;
    isIE11 = !!navigator.userAgent.match(/Trident.*rv[ :]*11\./);
    if(isIE11 == true){
        isIE = true;
    } 
    isFirefox = navigator.userAgent.search("Firefox") > -1; 
    isOpera = navigator.userAgent.search("Opera") > -1; 
    isSafari = navigator.userAgent.search("Safari") > -1;

    webMode = "PC";
    if( navigator.platform.indexOf("Win") == 0 )     { webMode = "PC";   }//WIN
    if( navigator.platform.indexOf("Mac") == 0 )     { webMode = "PC";   }//MAC
    if( navigator.platform.indexOf("iPad") == 0 )    { webMode = "PAD";   }//IPAD
    if( navigator.platform.indexOf("iPhone") == 0 )  { webMode = "PHONE"; }//IPHONE
    if( navigator.platform.indexOf("iPod") == 0 )    { webMode = "PHONE"; }//IPOD
    if((navigator.userAgent.indexOf('iPhone') != -1) || (navigator.userAgent.indexOf('iPod') != -1) || (navigator.userAgent.indexOf('iPad') != -1)) { 
        //webMode = "IOS";
    }
    if( navigator.userAgent.indexOf('Android') != -1){  webMode = "ANDROID"; }//ANDROID
    //if( navigator.userAgent.match(/Android/i) )     { webMode = "ANDROID"; }//ANDROID
    //if (navigator.userAgent.indexOf('iPod')!=-1) alert('iPod!');
    //if( navigator.userAgent.search("Mobile") != -1) {webMode = "ANDROID_MOBILE"} else {webMode = "ANDROID_TABLET" }
    function detectBrowser(){
        var sAgent = navigator.userAgent.toLowerCase();
        this.isIE = (sAgent.indexOf("msie")!=-1); //IE6.0-7
        this.isFF = (sAgent.indexOf("firefox")!=-1);//firefox
        this.isSa = (sAgent.indexOf("safari")!=-1);//safari
        this.isOp = (sAgent.indexOf("opera")!=-1);//opera
        this.isNN = (sAgent.indexOf("netscape")!=-1);//netscape
        this.isCh = (sAgent.indexOf("chrome")!=-1);//chrome
        this.isMa = this.isIE;//marthon
        this.isOther = (!this.isIE && !this.isFF && !this.isSa && !this.isOp && !this.isNN && !this.isSa);//unknown Browser
    }
    //var oBrowser = new detectBrowser();
/*
    if (oBrowser.isIE) { 
        alert("IE6.0/7.0(or above version).");
    } 
    if (oBrowser.isSa && !oBrowser.isCh) { 
        alert("Safari."); 
    } 
    if (oBrowser.isOp) { 
        alert("Opera."); 
    } 
    if (oBrowser.isCh && oBrowser.isSa) { 
        alert("Chrom."); 
    } 
    if(oBrowser.isFF) { 
        alert("FireFox."); 
    }
*/