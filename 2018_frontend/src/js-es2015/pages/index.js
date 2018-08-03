//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
import { STEP } from "../component.js";

//import answer from 'the-answer';
//import {test} from 'youtubeiframe-jojo'
//import * as PIXI from 'pixi.js';
//import TweenMax from "TweenMax";
//import CSSPlugin from "gsap/CSSPlugin";
import { Particle } from "../particleSystem2.js"
import { FullPagejs } from "../fullpage.js"
export {
    INDEX as INDEX,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
var cm, council, lu;
class INDEX extends Main {
    constructor(NAME = 'index', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.bind = this.bind.bind(this);
        lu = new LocateUpdator();
        
        this.watchScroll();
        this.map = new MAP();

        new Particle();
        cm = new CountyMayo();
        council = new Councilor();
       
        new FullPagejs();
        this.init();

    }
    init() {
        let context = this;
        super.init();
        
        $(window).resize(onresize)
        function onresize(){
            let vh = Number(getBrowserHeight());
            let vw = Number(getBrowserWidth())
            let s = vh/1080;
            TweenMax.set($('svg') , {scaleX :s , scaleY:s , transformOrigin:"40% 0%"})
            if(vw < 768){
                $(".step1").mCustomScrollbar('destroy')
                $(".step1").mCustomScrollbar({
                    theme: "my-theme1",
                    axis: "y"
                });

            }else{
                $(".step1").mCustomScrollbar('destroy')
            }
            
        }
        onresize();

        

        $(".step2").mCustomScrollbar({
            theme: "my-theme1",
            axis: "y"
        });


        new STEP("#kv", "#MayorAndCouncilor", anim);
        new STEP("#MayorAndCouncilor", "#seemore", anim);
        new STEP("#seemore", "#bills", anim);
        new STEP("#bills", "#votes", anim);
        new STEP("#votes", "#wishingwell", anim);
        new STEP("#wishingwell", ".end", anim);
        let timer = 0;
        function anim(typ, sec = ".kv1") {
            let dom = $(sec);
            



            if (typ) {
                if(sec == '#kv'){
                    let d = (timer>0)? 1 : 2
                    TweenMax.fromTo($('#kv .title '), .7, { opacity: 0 }, { delay: d, opacity: 1 })
                    let count = 0;
                    $('#kv .sub > * ').each(function() {
                        TweenMax.fromTo($(this), 1, { opacity: 0, y: 20 }, { delay: d + .1 * count, y: 0, opacity: 1 })
                        count++
                    })
                }else if(sec == '#MayorAndCouncilor'){
                    let d =0;
                    let count =0;
                   
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.fromTo($(this) , .5 , {x:30 , opacity:0} , {delay: d + .1 * count, x:0, opacity:1 ,ease:Back.easeOut})    
                        count++
                    })

                    /**
                     * ICON ANIMATION
                     */
                    let icos = dom.find('.ico');
                    count =0;
                    d = 1;
                    icos.each(function(){
                        let fromy = (count ==0)?500 : -500
                        TweenMax.fromTo($(this) , .7 , {y:fromy } , {delay: d , y:0, opacity:1 ,ease:Cubic.easeOut})    
                        count++
                    })
                    
                }else if(sec == '#seemore'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.fromTo($(this) , .5, {x:30 , opacity:0} , {delay: d + .1 * count, x:0, opacity:1 ,ease:Back.easeOut})    
                        count++
                    })
                    d=1;
                    let icos = dom.find('.ico');
                    //TweenMax.killTweensOf( icos.find('.eyeball')) ;
                    TweenMax.fromTo(icos, 1.5 , {x:-50} , {delay: 0 ,x:0 ,ease:Back.easeInOut})
                    TweenMax.fromTo(icos.find('.eyeball') , .7 , {x:-50} , {delay: 0 , x:50 , yoyo:true, repeat:1 , repeatDelay:.7,ease:Sine.easeInOut,onComplete:function(){
                        TweenMax.to(icos.find('.eyeball') , .7 , {delay:.7, x:0})
                    }})
                    
                }else if(sec == '#bills'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.fromTo($(this) , .5 , {x:30 , opacity:0} , {delay: d + .1 * count, x:0, opacity:1 ,ease:Back.easeOut})    
                        count++
                    })
                    d=1;
                    let icos = dom.find('.ico');
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.fromTo(icos ,1.2 , {x:800} , {delay: 0 , y:0,  x:0 ,ease:Sine.easeInOut})
                    
                }else if(sec == '#votes'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.fromTo($(this) , .5 , {x:30 , opacity:0} , {delay: d + .1 * count, x:0, opacity:1 ,ease:Back.easeOut})    
                        count++
                    })
                    d=1;
                    let hammer = dom.find('.hammer') ,dong = dom.find('.dong')  ;
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.fromTo(hammer ,1.2 , {x:100 , y:-100 , rotation:30, transformOrigin:"100% 100%"} , {delay: 0, transformOrigin:"100% 100%" , y:0,  x:0, rotation:0 ,ease:Back.easeInOut})
                    TweenMax.fromTo(dong , .1 , {opacity:0} , {delay: .9 ,opacity:1 ,ease:Sine.easeInOut})
                    
                }else if(sec == '#wishingwell'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.fromTo($(this) , .5 , {x:30 , opacity:0} , {delay: d + .1 * count, x:0, opacity:1 ,ease:Back.easeOut})    
                        count++
                    })
                    d=1;
                    let ico = dom.find('.ico');
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.fromTo(ico , 1.5 , {x:-500 , y:500 } , {delay: 0,  y:0,  x:0, rotation:0 ,ease:Sine.easeInOut})
                    
                }


                timer ++ ;

            }else{

                if(sec == '#kv'){
                    TweenMax.to($('#kv .title '), .7, { opacity: 0 })
                    $('#kv .sub > * ').each(function() {
                        TweenMax.to($(this), .7, { opacity: 0, y: 20 })
                       
                    })
                }else if(sec == '#MayorAndCouncilor'){
                    let d =.5;
                    let count =0;
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.to($(this) , .7 , {x:30 , opacity:0} )    
                        count++
                    })
                     let icos = dom.find('.ico');
                     icos.each(function(){
                        let fromy = (count ==0)?500 : -500
                        TweenMax.to($(this) , .7 , {y:fromy} )    
                    })
                    
                    
                }else if(sec == '#seemore'){
                    let d =.5;
                    let count =0;
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.to($(this) , .7 , {x:30 , opacity:0} )    
                        count++
                    })
                    let icos = dom.find('.ico');
                    TweenMax.to(icos, 1 , {x:-50})
                    //  let icos = dom.find('.ico');
                    //  icos.each(function(){
                    //     let fromy = (count ==0)?500 : -500
                        
                    // })
                    
                    
                }else if(sec == '#bills'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.to($(this) , .7 , {x:30 , opacity:0} )    
                        count++
                    })
                    d=1;
                    let icos = dom.find('.ico');
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.to(icos , 1.2 , {x:800} )
                    
                } else if(sec == '#votes'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.to($(this) , .5 , {x:30 , opacity:0})    
                        count++
                    })
                    d=1;
                    let hammer = dom.find('.hammer') ,dong = dom.find('.dong')  ;
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.to(hammer ,1, {x:100 , y:-100 , rotation:30, transformOrigin:"100% 100%"})
                    TweenMax.to(dong , .5 , {opacity:0} , {delay: 1.2 ,opacity:1 ,ease:Sine.easeInOut})
                    
                } else if(sec == '#wishingwell'){
                    let d =0;
                    let count = 0;
                    console.log('sec .... ' + sec)
                    
                    dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function(){
                        TweenMax.to($(this) , .5 , {x:30 , opacity:0} )    
                        count++
                    })
                    d=1;
                    let ico = dom.find('.ico');
                    //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                    TweenMax.to(ico , 1, {x:-500 , y:500 })
                    
                }
            }
        }


        context.anim();



    }
    anim() {
        // TweenMax.fromTo($('#kv .title '), .7, { opacity: 0 }, { delay: 2, opacity: 1 })
        // let count = 0;
        // $('#kv .sub > * ').each(function() {
        //     TweenMax.fromTo($(this), 1, { opacity: 0, y: 20 }, { delay: 2 + .1 * count, y: 0, opacity: 1 })
        //     count++
        // })
        if( typeof global_location.county == 'undefined'){
            TweenMax.fromTo($('#kv .locator > .ico '), .8, { opacity: 0, scaleX: 1.1, scaleY: 1.1 }, { delay: 3, y: 0, opacity: 1, scaleX: 1, scaleY: 1 })
            TweenMax.fromTo($('#kv .locator  span '), .8, { opacity: 0 }, { delay: 3.2, y: 0, opacity: 1 })

        }else{
            $('#kv .locator ').hide();
            lu.updateLocation();
            $('#kv .locator-ed ').delay(3000).fadeIn();

        }
        

    }
    watchScroll() {

    }
    bind() {
        super.bind();
        let context = this;
        $('.btn-findCouncilmen,.btn-findMayor').hover(function (){
            TweenMax.to($(this).find('.ico') , .5 , {y:-5 , repeat:-1 , yoyo:true})
        } , function (){
            TweenMax.killTweensOf($(this).find('.ico'))    ;
            TweenMax.to($(this).find('.ico') , .2 , {y:0})
        })
        $('.btn-findCouncilmen').click(function() {
            let href = $(this).attr('href');
            if (href == "#")
                route('findcouncilor')
            else {
                location.href = href;
            }
        })
        $('.btn-findMayor').click(function() {
            let href = $(this).attr('href');
            if (href == "#")
                route('findmayor')
            else {
                location.href = href;
            }
        })


        /*
         *update locator by 
         */

        $('.locator').click(function() {
            $('.locator').fadeOut(500);


            ///////update View.....
            function error(err) {
                
                lu.updateLocation();

            };
            navigator.geolocation.getCurrentPosition(function(position) {
                $.ajax({
                    url: global_geolookupApi,
                    type: 'GET',
                    data: {
                        zoom: 19,
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    },
                    success: function(data) {
                        global_location = { county: data[0].values[1], area: data[0].values[2] };
                        
                        lu.updateLocation();
                        //update highlight
                        //



                        
                    },
                    error: function() {
                        alert('抱歉，定位失敗，請手動選擇～');
                        lu.updateLocation();
                        
                    },
                });
            }, error, { enableHighAccuracy: true });
        })
        if (global_location.county != undefined) {
            $('.locator-ed').click(function() {
                context.map.addMap()
            })
        } else {
            $('.btn-chooseLocation').click(function() {
                context.map.addMap()
            })
        }
        $('.pop-map .btn-close').click(function() {
            context.map.removeMap()
        })
    }

}

function LocateUpdator() {


    this.updateLocation = function() {
        __updateLocation()
    }
    function __updateLocation(){
        if (global_location.county != undefined) {
            $('.locator').hide();
            $('.locator-ed .desc p:first').html('您已標定的區域');
            $('.county_val').html(global_location.county)
            if (global_location.area != undefined) {
                $('.area_val').html(', ' + global_location.area)
            } else {
                $('.area_val').html('')
            }
        } else {
            $('.locator-ed .desc p:first').html('您尚未定位');
        }
        $('.locator-ed').delay(500).fadeIn(500);
        // 改變縣市長/議員HIGHLIGHT
        updateHighlights();
        // 取得選區號 存入COOKIE 改變URL
        getConstituency();
        //
    }
    function getConstituency() {
        $.ajax({
            url: global_constituencylookupApi,
            type: 'POST',
            data: {
                type: 'councilor',
                county: global_location.county,
                district: global_location.area,
            },
            success: function(data) {
                //                {"county":"臺北市","constituency":1,"type":"councilor","district":"萬華區"}
                setCookies(data);
                updateMayorCouncilorURL(data);

            },
            error: function() {
                console.log('error : cant get constituencies...');
                if (location.href.indexOf('localhost') >= 0) {
                    setCookies({ county: '臺北市', district: '萬華區', constituency: '1' });
                    updateMayorCouncilorURL({ county: '臺北市', district: '萬華區', constituency: '1' });
                }
            },
        });
    }

    function updateMayorCouncilorURL(d) {
        console.log('chg mayor councilor url....');
        $('#kv .btn-findMayor').attr('href', `${prefixUrlMayor_global}${d.county}/`)
        $('#kv .btn-findCouncilmen').attr('href', `${prefixUrlCouncilor_global}${d.county}/${d.constituency}/`)
        $('#bills a:first').attr('href' , `${prefixUrlMayorForBills_global}${d.county}/`)
        $('#bills a:nth-child(2)').attr('href' , `${prefixUrlCouncilorForBills_global}${d.county}/`)
    }

    function updateHighlights() {
        cm.findAreaBycounty(global_location.county);
        council.findAreaBycounty(global_location.county);
    }

    function setCookies(d) {
        console.log('saving coockies...');
        setCookie('county', d.county, 30)
        setCookie('district', d.district, 30)
        setCookie('constituency', d.constituency, 30)
    }

    function init() {

        console.log('locateUpdator init ....')
        //檢查cookie
        global_location.county = ( getCookie('county') != null)? getCookie('county') : undefined;
        global_location.area = (getCookie('district') != null)? getCookie('district') : undefined;

        //global_location = getCookie('constituency');
        //__updateLocation();
       
    }
    init();

}


function Councilor() {
    let dom = $('.sec2 .findcouncilor');
    let area;



    function bind() {

        dom.find('.select-area a').click(function(e) {
            e.preventDefault();
            let vw =Number(getBrowserWidth()) ;
            let area = $(this).data('id');

            if(vw < 768){
                location.href= `${prefixUrlCouncilor_global}#${area}`
                return;
            }
            
            if (area == "") { area = "六都" }
            let cityies = GLOBAL.geo[area].cities;

            updateViewUi(area);
            updateView(cityies, 'city', area);
            let ct = updateViewUiCounty(0);

        })
    }

    function bindcounty() {
        const context = this;
        dom.find('.select-county > a').off('click').click(function() {
            let id = $(this).data('id');
            let ct = updateViewUiCounty(id)
        })


    }

    this.findAreaBycounty = function(county) {
        let area;
        for (let i in GLOBAL.geo) {
            let cities = GLOBAL.geo[i].cities;
            console.log('iterate ...area:' + i)
            for (let j in cities) {
                let ct = GLOBAL.geo[i].cities[j].cne;
                if (county == ct) {
                    console.log('city match ...area:' + county);
                    area = i;
                    break;
                }
            }

            if (typeof area != 'undefined')
                break;
        }
        console.log('find ...area:' + area)
        if (area != undefined) {

            let cityies = GLOBAL.geo[area].cities;

            updateViewUi(area)
            updateView(cityies, area);
            updateViewUiCounty(county);
        } else {
            console.log('area undefined!...')
        }






    }

    // function findAreaBycounty(county) {
    //     let area;

    //     return area;

    // }

    function updateView(cityies, typ, area) {
        dom.find('.select-county').html('')
        for (let i in cityies) {
            dom.find('.select-county').append(`
             <a href="${prefixUrlCouncilor_global}${cityies[i].cne}#${area}" data-id="${cityies[i].cne}">${cityies[i].cne}</a>
              `)
        }
        bindcounty();


    }

    function updateViewUiCounty(county = 0) {
        if (county == 0) {
            county = dom.find('.select-county a:first').data('id');
        }

        dom.find('.select-county a').each(function() {

            let id = $(this).data('id');

            if (id == county) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }

        })

        return county;

    }

    function updateViewUi(area) {

        dom.find('.select-area > a').each(function() {
            let id = $(this).data('id');
            if (id == area) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }
        })



    }

    function datafetch(area, year) {
        const context = this;
        getD(area, year);

        function getD(area = '六都', year = 2018) {
            if (year_global) year = year_global;
            $.get(jsonUrl_global, (pResponse) => {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');

                    if (area == "") { area = "六都" }
                    let cityies = GLOBAL.geo[area].cities;
                    updateViewUi(area);
                    updateView(cityies, 'city', area);

                    let ct = updateViewUiCounty('');
                    //updateViewCounty(ct);



                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');
        }

        function updateData(category) {

            GLOBAL.geo[category] = { cities: [] };
            //找出有山地原住民
            let items = GLOBAL.constituencies;



            let cts = $.grep(items, function(item) {
                if (category == '高山原住民')
                    return item.district.indexOf('山地原住民') >= 0;
                else
                    return item.district.indexOf(category) >= 0;
            });

            //console.log(cts)
            let norepeatcts = _.groupBy(cts, function(ct) { return ct.county; });

            for (let ct in norepeatcts) {
                console.log('norepeatcts ...' + ct);
                let eng = findEngCounty(ct)
                GLOBAL.geo[category].cities.push({ cne: ct, eng: eng })
            }
        }

        function findEngCounty(countyval) {
            let all = GLOBAL.allcities
            let cts = $.grep(all, function(item) {

                return item.cne.indexOf(countyval) >= 0;
            });
            return cts[0].eng
        }
    }

    function init() {
        datafetch('六都', 2018)
        bind();
    }
    init();
}

function CountyMayo() {
    let dom = $('.sec2 .findmayor');
    let area;

    function bind() {
        dom.find('.select-area > a').click(function(e) {
            e.preventDefault();
            let vw = getBrowserWidth();
            let area = $(this).data('id');

            if(vw < 768){
                location.href= `${prefixUrlMayor_global}#${area}`;
                return;
            }
            // context.datafetch(id);
            if (area == "") { area = "六都" }
            let cityies = GLOBAL.geo[area].cities;

            updateViewUi(area)
            updateView(cityies, area)
            updateViewUiCounty(0)
        })
    }
    this.findAreaBycounty = function(county) {
        let area;
        for (let i in GLOBAL.geo) {
            let cities = GLOBAL.geo[i].cities;
            console.log('iterate ...area:' + i)
            for (let j in cities) {
                let ct = GLOBAL.geo[i].cities[j].cne;
                if (county == ct) {
                    console.log('city match ...area:' + county);
                    area = i;
                    break;
                }
            }

            if (typeof area != 'undefined')
                break;
        }
        console.log('find ...area:' + area)
        if (area != undefined) {

            let cityies = GLOBAL.geo[area].cities;

            updateViewUi(area)
            updateView(cityies, area);
            updateViewUiCounty(county);
        } else {
            console.log('area undefined!...')
        }






    }

    function updateViewUiCounty(val) {
        if (val == 0) {
            val = dom.find('.select-county a:first').data('id');
        }
        $('.select-county  a').each(function() {
            let id = $(this).data('id');
            if (id == val) {
                dom.find(this).addClass('act');
            } else {
                dom.find(this).removeClass('act');
            }
        })
    }

    function updateViewUi(area) {
        dom.find('.select-area > a').each(function() {
            let id = $(this).data('id');
            if (id == area) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }
        })
    }

    function updateView(cityies, area) {
        const context = this;
        dom.find('.select-county').html('')
        for (let i in cityies) {
            dom.find('.select-county').append(`
             <a href="${prefixUrlMayor_global}${cityies[i].cne}/#${area}" data-id="${cityies[i].cne}">${cityies[i].cne}</a>
              `)
        }
    }

    function datafetch(area) {
        const context = this;
        console.log('data fetching....');
        if (area == "") { area = "六都" }
        let cityies = GLOBAL.geo[area].cities;

        updateViewUi(area)
        updateView(cityies, area)
        updateViewUiCounty(0)

    }

    function init() {
        datafetch("六都");
        bind();
    }
    init();
}

function MAP() {
    let step = 0;
    let countys = ["臺南市", "高雄市", "南投縣", "臺中市", "苗栗縣", "彰化縣", "雲林縣",
        "宜蘭縣", "花蓮縣", "澎湖縣", "新北市", "嘉義縣", "嘉義市", "連江縣", "金門縣",
        "臺東縣", "屏東縣", "臺北市", "桃園市", "新竹縣", "基隆市", "新竹市",
    ]

    let zip = [];
    zip[0] = ['臺北市', '基隆市', '新北市', '宜蘭縣', '新竹市', '新竹縣', '桃園市', '苗栗縣', '臺中市', '彰化縣', '南投縣', '嘉義市', '嘉義縣', '雲林縣', '臺南市', '高雄市', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣', '金門縣', '連江縣'];

    //區
    zip["臺北市"] = { '中正區': 100, '大同區': 103, '中山區': 104, '松山區': 105, '大安區': 106, '萬華區': 108, '信義區': 110, '士林區': 111, '北投區': 112, '內湖區': 114, '南港區': 115, '文山區': 116 };
    zip["基隆市"] = { '仁愛區': 200, '信義區': 201, '中正區': 202, '中山區': 203, '安樂區': 204, '暖暖區': 205, '七堵區': 206 };
    zip["新北市"] = { '萬里區': 207, '金山區': 208, '板橋區': 220, '汐止區': 221, '深坑區': 222, '石碇區': 223, '瑞芳區': 224, '平溪區': 226, '雙溪區': 227, '貢寮區': 228, '新店區': 231, '坪林區': 232, '烏來區': 233, '永和區': 234, '中和區': 235, '土城區': 236, '三峽區': 237, '樹林區': 238, '鶯歌區': 239, '三重區': 241, '新莊區': 242, '泰山區': 243, '林口區': 244, '蘆洲區': 247, '五股區': 248, '八里區': 249, '淡水區': 251, '三芝區': 252, '石門區': 253 };
    zip["宜蘭縣"] = { '宜蘭巿': 260, '頭城鎮': 261, '礁溪鄉': 262, '壯圍鄉': 263, '員山鄉': 264, '羅東鎮': 265, '三星鄉': 266, '大同鄉': 267, '五結鄉': 268, '冬山鄉': 269, '蘇澳鎮': 270, '南澳鄉': 272 };
    zip["新竹市"] = { '東區': 300, '北區': 300, '香山區': 300 };
    zip["新竹縣"] = { '竹北市': 302, '湖口鄉': 303, '新豐鄉': 304, '新埔鎮': 305, '關西鎮': 306, '芎林鄉': 307, '寶山鄉': 308, '竹東鎮': 310, '五峰鄉': 311, '橫山鄉': 312, '尖石鄉': 313, '北埔鄉': 314, '峨眉鄉': 315 };
    zip["桃園市"] = { '中壢區': 320, '平鎮區': 324, '龍潭區': 325, '楊梅區': 326, '新屋區': 327, '觀音區': 328, '桃園區': 330, '龜山區': 333, '八德區': 334, '大溪區': 335, '復興區': 336, '大園區': 337, '蘆竹區': 338 };
    zip["苗栗縣"] = { '竹南鎮': 350, '頭份鎮': 351, '三灣鄉': 352, '南庄鄉': 353, '獅潭鄉': 354, '後龍鎮': 356, '通霄鎮': 357, '苑裡鎮': 358, '苗栗市': 360, '造橋鄉': 361, '頭屋鄉': 362, '公館鄉': 363, '大湖鄉': 364, '泰安鄉': 365, '銅鑼鄉': 366, '三義鄉': 367, '西湖鄉': 368, '卓蘭鎮': 369 };
    zip["臺中市"] = { '中區': 400, '東區': 401, '南區': 402, '西區': 403, '北區': 404, '北屯區': 406, '西屯區': 407, '南屯區': 408, '太平區': 411, '大里區': 412, '霧峰區': 413, '烏日區': 414, '豐原區': 420, '后里區': 421, '石岡區': 422, '東勢區': 423, '和平區': 424, '新社區': 426, '潭子區': 427, '大雅區': 428, '神岡區': 429, '大肚區': 432, '沙鹿區': 433, '龍井區': 434, '梧棲區': 435, '清水區': 436, '大甲區': 437, '外埔區': 438, '大安區': 439 };
    zip["彰化縣"] = { '彰化市': 500, '芬園鄉': 502, '花壇鄉': 503, '秀水鄉': 504, '鹿港鎮': 505, '福興鄉': 506, '線西鄉': 507, '和美鎮': 508, '伸港鄉': 509, '員林鎮': 510, '社頭鄉': 511, '永靖鄉': 512, '埔心鄉': 513, '溪湖鎮': 514, '大村鄉': 515, '埔鹽鄉': 516, '田中鎮': 520, '北斗鎮': 521, '田尾鄉': 522, '埤頭鄉': 523, '溪州鄉': 524, '竹塘鄉': 525, '二林鎮': 526, '大城鄉': 527, '芳苑鄉': 528, '二水鄉': 530 };
    zip["南投縣"] = { '南投市': 540, '中寮鄉': 541, '草屯鎮': 542, '國姓鄉': 544, '埔里鎮': 545, '仁愛鄉': 546, '名間鄉': 551, '集集鎮': 552, '水里鄉': 553, '魚池鄉': 555, '信義鄉': 556, '竹山鎮': 557, '鹿谷鄉': 558 };
    zip["嘉義市"] = { '嘉義市': 600 };
    zip["嘉義縣"] = { '番路鄉': 602, '梅山鄉': 603, '竹崎鄉': 604, '阿里山': 605, '中埔鄉': 606, '大埔鄉': 607, '水上鄉': 608, '鹿草鄉': 611, '太保鄉': 612, '朴子市': 613, '東石鄉': 614, '六腳鄉': 615, '新港鄉': 616, '民雄鄉': 621, '大林鎮': 622, '溪口鄉': 623, '義竹鄉': 624, '布袋鎮': 625 };
    zip["雲林縣"] = { '斗南鎮': 630, '大埤鄉': 631, '虎尾鎮': 632, '土庫鎮': 633, '褒忠鄉': 634, '東勢鄉': 635, '臺西鄉': 636, '崙背鄉': 637, '麥寮鄉': 638, '斗六市': 640, '林內鄉': 643, '古坑鄉': 646, '莿桐鄉': 647, '西螺鎮': 648, '二崙鄉': 649, '北港鎮': 651, '水林鄉': 652, '口湖鄉': 653, '四湖鄉': 654, '元長鄉': 655 };
    zip["臺南市"] = { '中西區': 700, '東區': 701, '南區': 702, '北區': 704, '安平區': 708, '安南區': 709, '永康區': 710, '歸仁區': 711, '新化區': 712, '左鎮區': 713, '玉井區': 714, '楠西區': 715, '南化區': 716, '仁德區': 717, '關廟區': 718, '龍崎區': 719, '官田區': 720, '麻豆區': 721, '佳里區': 722, '西港區': 723, '七股區': 724, '將軍區': 725, '學甲區': 726, '北門區': 727, '新營區': 730, '後壁區': 731, '白河區': 732, '東山區': 733, '六甲區': 734, '下營區': 735, '柳營區': 736, '鹽水區': 737, '善化區': 741, '大內區': 742, '山上區': 743, '新市區': 744, '安定區': 745 };
    zip["高雄市"] = { '新興區': 800, '前金區': 801, '苓雅區': 802, '鹽埕區': 803, '鼓山區': 804, '旗津區': 805, '前鎮區': 806, '三民區': 807, '楠梓區': 811, '小港區': 812, '左營區': 813, '仁武區': 814, '大社區': 815, '岡山區': 820, '路竹區': 821, '阿蓮區': 822, '田寮區': 823, '燕巢區': 824, '橋頭區': 825, '梓官區': 826, '彌陀區': 827, '永安區': 828, '湖內區': 829, '鳳山區': 830, '大寮區': 831, '林園區': 832, '鳥松區': 833, '大樹區': 840, '旗山區': 842, '美濃區': 843, '六龜區': 844, '內門區': 845, '杉林區': 846, '甲仙區': 847, '桃源區': 848, '那瑪夏區': 849, '茂林區': 851, '茄萣區': 852 };
    zip["屏東縣"] = { '屏東市': 900, '三地鄉': 901, '霧臺鄉': 902, '瑪家鄉': 903, '九如鄉': 904, '里港鄉': 905, '高樹鄉': 906, '鹽埔鄉': 907, '長治鄉': 908, '麟洛鄉': 909, '竹田鄉': 911, '內埔鄉': 912, '萬丹鄉': 913, '潮州鎮': 920, '泰武鄉': 921, '來義鄉': 922, '萬巒鄉': 923, '崁頂鄉': 924, '新埤鄉': 925, '南州鄉': 926, '林邊鄉': 927, '東港鄉': 928, '琉球鄉': 929, '佳冬鄉': 931, '新園鄉': 932, '枋寮鄉': 940, '枋山鄉': 941, '春日鄉': 942, '獅子鄉': 943, '車城鄉': 944, '牡丹鄉': 945, '恆春鎮': 946, '滿州鄉': 947 };
    zip["臺東縣"] = { '臺東市': 950, '綠島鄉': 951, '蘭嶼鄉': 952, '延平鄉': 953, '卑南鄉': 954, '鹿野鄉': 955, '關山鎮': 956, '海端鄉': 957, '池上鄉': 958, '東河鄉': 959, '成功鎮': 961, '長濱鄉': 962, '太麻里': 963, '金峰鄉': 964, '大武鄉': 965, '達仁鄉': 966 };
    zip["花蓮縣"] = { '花蓮市': 970, '新城鄉': 971, '秀林鄉': 972, '吉安鄉': 973, '壽豐鄉': 974, '鳳林鎮': 975, '光復鄉': 976, '豐濱鄉': 977, '瑞穗鄉': 978, '萬榮鄉': 979, '玉里鎮': 981, '卓溪鄉': 982, '富里鄉': 983 };
    zip["澎湖縣"] = { '馬公市': 880, '西嶼鄉': 881, '望安鄉': 882, '七美鄉': 883, '白沙鄉': 884, '湖西鄉': 885 };
    zip["金門縣"] = { '金沙鎮': 890, '金湖鎮': 891, '金寧鄉': 892, '金城鎮': 893, '烈嶼鄉': 894, '烏坵': 896 };
    zip["連江縣"] = { '南竿': 209, '北竿': 210, '莒光': 211, '東引': 212 };

    function updateStep2(county) {
        console.log('縣市....' + county);
        step = 2;



        updateAreaView(county);
        rebindArea(county);
        $('.pop-map .step1').fadeOut(200)
        $('.pop-map .step2').delay(200).show()
        let count =0 
        $('.pop-map .step2 .tit,.pop-map .step2  .sub ,.pop-map .step2  .select , .pop-map .step2  .select-county-blk > div').each(function(){
            TweenMax.fromTo($(this) , .5 , {opacity:0 , y:20 } , {delay:.5 + .05 * count , opacity:1 , y:0 , ease:Back.easeOut})
            count++;
        })
    }

    function updateStep1() {
        step = 1
        $('.pop-map .step2').hide()
        $('.pop-map .step1').show();
        let count =0 
        $('.pop-map .step1 .tit,.pop-map .step1  .sub ,.pop-map .step1  .select , .pop-map .step1  .select-county-blk > div').each(function(){
            TweenMax.fromTo($(this) , .5 , {opacity:0 , y:20 } , {delay:.5 + .05 * count , opacity:1 , y:0 , ease:Back.easeOut})
            count++;
        })
    }
    this.removeMap = function() {
        rmMap()
    }

    function rmMap() {
        $('.pop-map').fadeOut(300);
        step = 1;
    }
    this.addMap = function() {
        $('.pop-map').fadeIn(300);
        
        
        if (step == 1) {
            updateStep1()
        }
    }



    function rebindArea(county) {
        $('.pop-map .step2 .select-area-blk a').each(function() {
            $(this).off('click').click(function() {
                let area = $(this).data('area')
                global_location.county = county
                global_location.area = area;
                lu.updateLocation();
                rmMap();
                //route('MayorAndCouncilor')

            })
        })
    }

    function bind() {
        $('svg').find('.btn-county').each(function() {
            $(this).click(function() {
                let d = $(this).data('county');
                updateStep2(d);
            })
        })

        $('.pop-map .step1 select').change(function() {
            updateStep2($(this).val())
        })

        $('.pop-map .step1 .select-county-blk > div >a').each(function() {
            $(this).click(function(e) {
                e.preventDefault();
                let d = $(this).data('county');
                updateStep2(d)
            })
        })
    }

    function updateColors(dom) {
        let count = 0
        let rnd = Math.random() * 30
        let rndint = Math.ceil(rnd);
        let colorclass = 'bg-light-group-color'
        dom.each(function() {
            let n = (count + rndint) % 30 + 1
            $(this).addClass(colorclass + n)
            count++
        })

    }

    function updateAreaView(county) {

        $('.pop-map .step2 .select-area-blk').html('')
        for (let i in zip[county]) {
           
            $('.pop-map .step2 .select-area-blk').append(`<div class="col-xs-6 col-sm-3"><a class="info" href="#" data-area="${i}">
                <p>${i}</p>
                <p class="eng">${zip[county][i]}</p></a></div>`)
        }
        updateColors($('.pop-map .step2 .select-area-blk > div > a'));


    }

    function updatetwmapAttr() {
        let count = 0;
        $('svg g#ch > g ').each(function() {
            if (count < countys.length) {

                $(this).attr('data-county', countys[count]);
                $(this).addClass('btn-county');
            }

            $(this).hover(function() {
                $('svg g#ch > g ').css("opacity", .4)
                $(this).css("opacity", 1)
            }, function() {
                $('svg g#ch > g ').css("opacity", 1)

            })
            count++;
        })

        //update  mobile county selector
        $('.pop-map .step1 .select-county-blk > div >a').each(function() {
            let c = $(this).data('county');



            for (let i in GLOBAL.geo) {
                for (let j in GLOBAL.geo[i].cities) {
                    if (GLOBAL.geo[i].cities[j].cne == c) {
                        $(this).find('.eng').html(GLOBAL.geo[i].cities[j].eng)
                    }
                }
            }

        })

        updateColors($('.pop-map .step1 .select-county-blk > div >a'));


    }

    function init() {

        updatetwmapAttr();
        bind();
        step = 1;
    }

    init();
}



function route(hash) {
    var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
    const speed = 100;
    let top;
    let navh = $('nav').height();
    top = $("#" + hash).offset().top;
    let t = 700
    //TweenMax.set(window, {scrollTo:{y:top}});
    $body.stop().animate({
        scrollTop: top - navh
    }, t);
}
