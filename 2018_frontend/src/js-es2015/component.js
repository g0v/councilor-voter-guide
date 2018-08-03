
import {getBrowserHeight,updateImg,getBrowserWidth } from './common.js';
import {GLOBAL} from './config.js';

export{STEP as STEP , 
	CONTENT_CAROUSAL as CONTENT_CAROUSAL,
	CONTENT_CAROUSAL_STATIC as CONTENT_CAROUSAL_STATIC,CONTENT_CAROUSAL_STATIC2	,
};

function PARALEX_SCROLL_DECOS(NUM, Ky,ease,DOM){
		var old_pos = [] , oldprop =[];
		function loop(){
			for(var i=1;i<=NUM ; i++){
				let top = Number( $(window).scrollTop()) - 900;
				let Y = old_pos[i-1].y + top / 10 * Ky[i-1] ;
				let _y=  oldprop[i-1].y;
				_y += (Y - _y)*ease;
				$(DOM+i).css('top',_y);
				oldprop[i-1]={y:_y};
			}		
			setTimeout(	loop, 1000/20);
		}
		function reset(){	

		}
		this.init=function(){
			reset();
			for(var i=1;i<=NUM ; i++) {
				old_pos.push( { x:parseInt ( $(DOM+i).css('left'))  ,y:parseInt ( $(DOM+i).css('top')) });
				oldprop.push({ y:parseInt ( $(DOM+i).css('top') )})
			}
			loop();
		}
		this.init();
}
function stars(){
	function addstar (id){
	  $(".stars").append(`<div class="star" id="star_${id}" data-id="${id}">
				<img src="img/dest/star.png">
				</div>`);
	  
	  var rnd = Math.random()*.7 + .1;
	  const WIDTH = getBrowserWidth();
	  const HEIGHT = getBrowserHeight();
	  TweenMax.set( $("#star_" + id), {x:Math.random()*WIDTH  , y:Math.random()* HEIGHT , scaleX:rnd , scaleY:rnd});
	  loopArr($("#star_" + id) ,Math.random()*3 + 1.2 )
	}
	this.anim=function(){

	}
	this.render= function(){
	  for(var i =1 ;i <=40;i++){
		addstar(i)
	  }
	}
	this.render();
}
function FLOWERS(COUNT , RANGE ,DROP_ZONE,PARENT , CLASSNAME, DIRECTION , OPACITY){
	var count = COUNT;
	var particles = [];
	var FRICTION = 1;
	
	function loop(){
		for (var i = 0; i < count; i++) {
			let flake = particles[i],
				x = 500,
				y = 400,
				minDist = 150,
				x2 = flake.x,
				y2 = flake.y;

			let dist = Math.sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y)),
				dx = x2 - x,
				dy = y2 - y;

			if (/*dist < minDist*/false) {
				var force = minDist / (dist * dist),
					xcomp = (x - x2) / dist,
					ycomp = (y - y2) / dist,
					deltaV = force / 2;

				flake.velX -= deltaV * xcomp;
				flake.velY -= deltaV * ycomp;

			} else {
				flake.velX *= FRICTION;
				if (flake.velY <= flake.speed) {
					flake.velY = flake.speed
				}
				flake.velX += Math.cos(flake.step += .05) * flake.stepSize;
			}

			////change property
			flake.y += flake.velY;
			flake.x += flake.velX;
			flake.rot += flake.speedAng;		    
			if(flake.y >= RANGE.h - 50 && flake.y < RANGE.h){
				flake.opacity -= 0.02;
			}

			////update view
			TweenMax.set($(flake.dom) , {x:flake.x , y:flake.y , rotation:flake.rot,opacity:flake.opacity})

			//detect if boundary
			if (flake.y >= RANGE.h || flake.y <= 0) {

				reset(flake ,flake.i );

			}
			if (flake.x >= RANGE.w || flake.x <= -460) {
				reset(flake , flake.i);
			}
		}

		requestAnimationFrame(loop);
	}
	function reset(flake, i){
		 flake.x = DROP_ZONE[i%4].x + Math.floor(Math.random() * 600) - 300,
		 flake.y = DROP_ZONE[i%4].y + Math.floor(Math.random() * 50),
		 flake.size = (Math.random() * 3) + 2;
		 flake.speed = (Math.random() * .8) + 0.4;
		 flake.velY = flake.speed/4;
		 flake.opacity = OPACITY;
	}
	function insertDom( i ){
		var id = Math.ceil(Math.random() * 5) ;     	 
		$(PARENT).append('<div class="flower'+i+'"><img src="img/dest/index/leaf'+id+'.png"></div>');
	}
	this.init = function(){
		 for (var i = 0; i < count; i++) {
			 var x = DROP_ZONE[i%4].x + Math.floor(Math.random() * 600)- 300,
				 y = DROP_ZONE[i%4].y + Math.floor(Math.random() * 50),
				 scale = Math.random() * .5 + .5,
				 size = (Math.random() * 3) + 2,
				 speed = (Math.random() * .8) + 0.4,
				 opacity = OPACITY,//(Math.random() * 0.5) + 0.3;		         
				 speedAng = Math.random() * 1,
				 dom = PARENT + " " + CLASSNAME + i;

				 insertDom(i);
				 TweenMax.set( $(CLASSNAME + i) , {scaleX:scale , scaleY:scale , opacity:opacity})

			 particles.push({
				 i:i,
				 speed: speed,
				 velY: speed/4,
				 velX: (DIRECTION == 'left')?speed * -1.5 : speed * 1.5,
				 x: x,
				 y: y,
				 inix:x,
				 iniy:y,
				 size: size,
				 stepSize: (Math.random()) / 30,
				 step: 0,
				 rot:Math.random() * 180,
				 speedAng : speedAng,
				 opacity: opacity,
				 dom:dom
			 });
		 }
		loop();
	}
	this.init();
	
}


function STEP(SECTION, NEXT , ANIM = null){
	var _delay = 1000 / 5;
	var state = -1;
	var old_state = -1;
	

	function render_loop() {

		var sh = parseInt(getBrowserHeight());
		if (GLOBAL.top < $(SECTION).offset().top - sh * .9) {
			state = 0
			if (state != old_state) {
				animat('dis');
			}
		} else if (GLOBAL.top >= $(SECTION).offset().top - sh * .5 && GLOBAL.top < $(NEXT).offset().top - sh * .5) {
			state = 1
			if (state != old_state) {
				animat('act');
			}
		} else {
			state = 2
			if (state != old_state) {
				animat('dis');
			}
		}
		old_state = state;
		setTimeout(render_loop, _delay)
	}
  this.getanimat=animat;
	function animat(typ) {
		//console.log(SECTION + ' animat typ' + typ)
		

		if (typ == "act") {			
			 ANIM(true , SECTION)
		} else {
		  ANIM(false, SECTION)
	   
	   }
	}
	function reset() {   
		 ANIM(false, SECTION)	
		
	}
	this.init=function() {
		reset();
		render_loop();
	}
	this.init();
	
}


/*
繼承者們
 */

/*HAMMER PAN JS LIB*/
  function PAN(SELECTOR, CONTEXT) {
      var myElement
      var mc
      var _this = this;
      var time = 1000;
      var OFFSET = 100
      var old_pan = ''

      this.init = function() {
          myElement = document.getElementById(SELECTOR);
          mc = new Hammer(myElement);
          mc.get('pan').set({ direction: Hammer.DIRECTION_ALL });
          _this.bind_pan()
      }

      function pan_handle(ev) {
          //console.log("PAN!.............."+ev.type + ev.deltaY)
          if (ev.type == "panright" && ev.deltaX > OFFSET) {
              CONTEXT.act("r");
              mc.off("panleft panright");

              setTimeout(_this.bind_pan, time)
          }
          if (ev.type == "panleft" && ev.deltaX < -OFFSET) {
              CONTEXT.act("l");
              mc.off("panleft panright");
              setTimeout(_this.bind_pan, time)
          }
          if (ev.type == "panup") {
              console.log('up...')
              if (old_pan != "panup")
                  TweenMax.to(window, .5, { scrollTo: 400 });
          } else if (ev.type == "pandown") {
              if (old_pan != "pandown")
                  TweenMax.to(window, .5, { scrollTo: 0 });
          }

          old_pan = ev.type

      }

      this.bind_pan = function() {
          mc.on("panleft panright panup pandown", function(ev) {
              pan_handle(ev);
          });
      }

      this.init();
  }



function GIF(SELECT, NAME) {
    var interval;
    var count = 1;
    var tloop = 400 //msec
    function loop() {
        //console.log("GIF loop")
        if (count < 3)
            count++;
        else
            count = 1;
        updateImg(SELECT.find('.char'), "http://819c375429527e275f54-b1b6e7de992e67a5fcec75da074835f8.r32.cf6.rackcdn.com/img/dest/" + NAME + count + ".png")

        interval = setTimeout(loop, tloop)
    }

    function reset() {

        count = 1;
        updateImg(SELECT.find('.char'), "http://819c375429527e275f54-b1b6e7de992e67a5fcec75da074835f8.r32.cf6.rackcdn.com/img/dest/" + NAME + count + ".png");
    }

    this.play = function() {
        clearTimeout(interval);
        loop();
    }
    this.killgif = function() {
        reset();
        clearTimeout(interval);
    }
    this.init = function() {
        reset();

    }
    this.init();
}


/*SLIDE*/
function CONTENT_CAROUSAL(_btnleft, _btnright, _dots, _content, _itemW, _total, _curr = 1, _pageAmount = 1, _titles) {
    const btns = {};
    btns.left = _btnleft;
    btns.right = _btnright;
    const dots = _dots;
    const content = _content;
    const item_w = _itemW;
    const page_w = _itemW * _pageAmount;
    const total = _total;
    let curr = _curr
    const titles = _titles;
    const pageAmount = _pageAmount
    const autoplay = true;
    const context_parent = this;
    var DIRECT = "R";
    let last;


    this.getDIRECT = function() {
        return DIRECT;
    }
    this.getLast = function() {
        return last;
    }

    function WHEEL_CONTROLLER(_PARENT, _CURR, _TOTAL, PAGEAMOUNT = 1) {
        var CURR = _CURR
        var TOTAL = _TOTAL;
        var PARENT = _PARENT;
        var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT);

        this.init = function() {
            reset();
            this.bind();

        }.bind(this);

        this.unbind = function() {
            content.off('mousewheel');
        }
        this.bind = function() {
            content.off('mousewheel').on('mousewheel', function(event) {
                var act = event.deltaY;
                if (act > 0) {
                    //PARENT.act_triggered('L');
                }
                if (act < 0) {
                    console.log('wheel');
                    PARENT.killloop();
                    PARENT.act_triggered('R');

                }

            });
        }

        function reset() {

        }
        this.init();
    }

    function BTN_ARROW(_PARENT, _CURR, _TOTAL, PAGEAMOUNT = 1) {
        var CURR = _CURR
        var TOTAL = _TOTAL;
        var PARENT = _PARENT;
        var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT);
        this.init = function() {
            reset();
            this.bind();
            this.update_view(CURR)
        }.bind(this)
        this.unbind = function() {
            btns.left.off('click')
            btns.right.off('click')
        }
        this.bind = function() {
            btns.left.off('click').on('click', function() {

                //PARENT.act_triggered('L')
            })
            btns.right.off('click').on('click', function() {
                //PARENT.act_triggered('R');

            })
        }

        this.update_view = function(curr) {
            CURR = curr

            if (PAGEMAX <= 1) {
                btns.left.hide();
                btns.right.hide();
                //alert("both hide");
            } else if (curr == 1) {
                btns.left.hide();
                btns.right.show();
            } else if (curr == PAGEMAX) {
                btns.left.show();
                btns.right.hide();
            } else {
                btns.left.show();
                btns.right.show();
            }
        }

        function reset() {
            btns.left.show();
            btns.right.show();

        }


        this.init();

    }
    /*點點*/
    function DOTS(PARENT, _CURR, _TOTAL, PAGEAMOUNT = 1) {
        var DOM = content;
        var context = this
        var CURR = _CURR
        var TOTAL = _TOTAL;
        var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT)
        this.init = function() {
            reset();
            bind_action();
        }
        this.unbind = function() {
            DOM.find(".dot").each(function() {
                $(this).off('click');
            })
        }
        this.bind = function() {
            bind_action()
        }

        function bind_action() {
            DOM.find(".dot").each(function() {
                $(this).off('click').on('click', function() {
                    PARENT.killloop();
                    var id = $(this).data("id");
                    GLOBAL.ga.GT('index', ".btn.kv" + id)

                    console.log('dot clk');
                    context_parent.updateCurrView(id)
                    context.update_view(id);
                })
            })
        }

        function kill_action() {
            DOM.find(".dot").off("click")
        }
        this.update_view = function(curr) {
            CURR = curr;
            DOM.find(".dot").each(function() {
                var id = Number($(this).data("id"));
                if (id == CURR) {
                    $(this).addClass("act")
                } else {
                    $(this).removeClass("act")
                }
            })
        }

        function reset() {

        }
        this.init();
        this.update_view(CURR)
    }

    /*內容*/
    function CONTENT(PARENT, _CURR, _TOTAL, TITLES, PAGEAMOUNT = 1) {
        var DOM = content;
        var CURR = _CURR;
        var PAGEMAX = Math.ceil(_TOTAL / PAGEAMOUNT)
        this.init = function() {

            this.update_view(CURR);
            //initialPosition();

        }.bind(this);

        function initialPosition() {
            console.log('initialPosition')
            DOM.find(".item").each(function() {
                var id = Number($(this).data('id'));
                $(this).css({ "left": ((id - 1) * item_w + 50).toString() + '%' });
            })
        }

        function updateTitle(curr) {
            $(".title-real > img").each(function() {
                let id = Number($(this).data('id'))
                if (id == curr) {
                    TweenMax.to($(this), .5, { delay: .5, opacity: 1 });

                    TweenMax.to($('.model' + id), .5, { delay: .5, opacity: 1 });
                } else {
                    TweenMax.to($(this), .5, { delay: .5, opacity: 0 })
                    TweenMax.to($('.model' + id), 1, { delay: .5, opacity: 0 });
                }
            })


        }

        function updateBg() {
            $(".bgx").each(function() {
                let id = Number($(this).data('id'))
                if (id == curr) {
                    TweenMax.to($(this), 1, { delay: .5, opacity: 1 })
                } else {
                    TweenMax.to($(this), 1, { delay: .5, opacity: 0 })
                }
            })
        }
        this.update_view = function(curr) {
            var prop = [];

            DOM.find(".item").each(function() {
                let id = Number($(this).data('id'));
                //console.log('update_view...' + curr)
                //update TITLE
                updateTitle(curr);
                //UPDATE BG
                updateBg();
                if (PARENT.getDIRECT() == "R") {
                    if (curr == 1 && PARENT.getLast() == 5) {
                        if (id == 1) {
                            //TweenMax.set($(this) ,{left:(item_w+50).toString() + '%'});
                            $(this).css('left', (item_w + 50).toString() + '%');
                            TweenMax.to($(this), 2.2, { left: (50).toString() + '%', ease: Cubic.easeInOut, onComplete: initialPosition })
                        } else {
                            TweenMax.to($(this), 2.0, { left: ((id - 6) * item_w + 50).toString() + '%', ease: Cubic.easeInOut })
                        }
                    } else {
                        TweenMax.to($(this), 2.2, { left: ((id - curr) * item_w + 50).toString() + '%', ease: Cubic.easeInOut })

                    }
                }
            })
            CURR = curr;
        }

        this.reset = function() {}
        this.init();
    }

    let c = new CONTENT(this, curr, total, titles, pageAmount);
    let b = new BTN_ARROW(this, curr, total, pageAmount);
    let d = new DOTS(this, curr, total, pageAmount);

    //let m = new WHEEL_CONTROLLER(this, curr, total, pageAmount);
    let interval;
    this.killloop = function() {
        clearTimeout(interval);
        interval = setTimeout(loop, 5500);
    }
    this.act_triggered = function(typ) {
        console.log('act_triggered:' + typ)
        try {
            m.unbind();
        } catch (err) {}
        d.unbind();
        b.unbind();
        last = curr;
        if (typ == "L") {
            if (curr > 1) {
                curr--;
                c.update_view(curr)
            } else {
                curr = total;
                c.update_view(curr)
            }

        } else {
            if (curr < total) {
                curr++;
                c.update_view(curr)
            } else {
                curr = 1;
                c.update_view(curr)
            }
        }
        b.update_view(curr);
        d.update_view(curr);
        setTimeout(function() {
            try {
                m.bind();
            } catch (err) {}
            b.bind();
            d.bind();
        }, 2200)

    }


    this.updateCurrView = function(CURR) {
        curr = CURR;
        try {
            m.unbind();
        } catch (err) {}
        d.unbind();
        b.unbind();
        c.update_view(curr);
        b.update_view(curr);
        d.update_view(curr);
        setTimeout(function() {
            try {
                m.bind();
            } catch (err) {}
            b.bind();
            d.bind();
        }, 2200)
    }

    function loop() {
        clearTimeout(interval);
        if (autoplay) {
            if (DIRECT = "R") {
                context_parent.act_triggered("R")
            }
        }
        interval = setTimeout(loop, 5500);
    }
    loop();
}

/*              */
/* SLIDE FINITE*/
/*  _btnleft,_btnright 左右建 */
/*  _dots 可直接選取的DOM */
/*  _content 內容的DOM */
/* _itemW  各ITEM間距*/
/*_total 數量 */
/*_curr 目前id*/
/*_pageAmount 一頁會出現的數量*/
function CONTENT_CAROUSAL_STATIC(_btnleft,_btnright,_dots,_content,_itemW , _total, _curr=1  , _pageAmount = 1, _titles){
	const btns={};
	btns.left = _btnleft;
	btns.right = _btnright;
	const dots = _dots;
	const content = _content;
	const item_w = _itemW ;
	const page_w = _itemW * _pageAmount;
	const total = _total;
	let curr= _curr
	const titles = _titles;
	const pageAmount = _pageAmount
	const autoplay = true;
	const context_parent= this;
    const AUTOPLAY_TIME = 5000;
	let DIRECT = 'R'
	let last;
  ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/
   ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/
   ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/


  this.getCurr = function(){
  	return curr;
  }
  function BTN_ARROW(_PARENT ,_CURR , _TOTAL ,PAGEAMOUNT=1){
	 var CURR = _CURR
	 var TOTAL = _TOTAL;
	 var PARENT = _PARENT;
	 var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT);
	this.init=function(){
	   reset();
	   this.bind();
	   this.update_view(CURR)
	}.bind(this)
	this.unbind=function(){
		btns.left.off('click')
		btns.right.off('click')
	}
	this.bind = function() {
	    btns.left.off('click').on('click', function() {
            //PARENT.killloop();
           
	        PARENT.act_triggered('L');
	    })
	    btns.right.off('click').on('click', function() {
           
	        PARENT.act_triggered('R');
	    })
	}
	this.update_view=function(curr){
	   CURR = curr
	   if(PAGEMAX <=1 )
	   {
			btns.left.hide();
			btns.right.hide();
			//alert("both hide");
	   }
	   else if(curr==1)
	   {
		 btns.left.hide();
		 btns.right.show();
	   }
	   else if(curr==PAGEMAX)
	   {
		btns.left.show();
		btns.right.hide();
	   }
	   else
	   {    btns.left.show();
			btns.right.show();
        }
	}

	function reset() {
		btns.left.show();
		btns.right.show();
	}
	this.init();
  }
  /*點點*/
  function DOTS(PARENT,_CURR , _TOTAL , PAGEAMOUNT = 1){
	 var DOM = dots;
	 var context = this
	 var CURR = _CURR
	 var TOTAL = _TOTAL;
	 var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT)
	 this.init = function() {
	     reset();
	     bind_action();
	 }
	 this.unbind = function() {
	 	 //console.log('unbind action');
	     DOM.find(".dot").each(function() {
	         $(this).off('click');
	     })
	 }
	 this.bind = function() {
	     bind_action()
	 }

	function bind_action() {
	    //console.log('bind action');
	    DOM.find(".dot").each(function() {
	        $(this).off('click').on('click', function() {
	            //PARENT.killloop();
	            var id = $(this).data("id");
	            //console.log('dot clk');
	            context_parent.updateCurrView(id)
	            context.update_view(id);
	        })
	    })
	}


	  function kill_action(){
	  	 //console.log('kill action');
		 DOM.find(".dot").off("click")
	  }
	  this.update_view=function(curr){
		  CURR = curr;
		  DOM.find(".dot").each(function(){
			   var id = Number($(this).data("id"));
			   if(id==CURR)
			   {
                    
					//TweenMax.to($(this) , .5 , {scaleX:1.2 , scaleY:1.2, ease:Back.easeOut});
                    $(this).addClass('act')
			   } else {
                    
					//TweenMax.to($(this) , .5 , {scaleX:1 , scaleY:1,ease:Expo.easeOut});
                    $(this).removeClass('act')
			   }
		  })
	  }

	   function reset (){
			
	   }
	   this.init();
	   this.update_view(CURR)
  }

   /*內容*/
   function CONTENT(PARENT, _CURR ,_TOTAL , TITLES,PAGEAMOUNT = 1 ){
	   var DOM = content;
	   var CURR = _CURR;
	   var PAGEMAX = Math.ceil(_TOTAL / PAGEAMOUNT)
	   this.init=function(){

		   this.update_view(CURR);
		   //initialPosition();
		   
	   }.bind(this);

	   function initialPosition(){
	   		//console.log('initialPosition')
			
	   }
	  
	   this.update_view=function(curr){
		  var prop = []
		  DOM.find(".item").not('.itembg').each(function(){
			  let id = Number($(this).data('id'));
              if(id == curr){
                TweenMax.fromTo($(this) , .3, {opacity:0 , x:((DIRECT=="L")?-50:50)}, {delay:0,x:0 , opacity: 1})                                         
              }else{
                TweenMax.to($(this) , .2,{x:((DIRECT=="L")?50:-50), opacity: 0 })  
              }
 			  
		  })
		  CURR = curr;
	   }

	   this.reset = function(){
	   }
	   this.init();
   }

	let c = new CONTENT(this,curr, total,titles,pageAmount);
	let b = new BTN_ARROW( this ,curr, total,pageAmount);
	let d = new DOTS(this, curr , total, pageAmount);
	
	this.act_triggered = function(typ){ 
		
			d.unbind();
			b.unbind();
            DIRECT = typ 
			   //last = curr;
			  if(typ=="L"){
                   if(curr>1)
                   {
                       curr--;                     
                   }else{
                        curr=total;                   
                   }
                   c.update_view(curr);

               }else{
                   if(curr<total)
                   {
                       curr++;
                       
                   }else{
                        curr =1 ;
                   }
                   c.update_view(curr);
               }

			   b.update_view(curr);
			   d.update_view(curr);
			setTimeout( function(){				
				b.bind(); 
				d.bind();
			}, 300)

	}
	
	this.updateCurrView = function (CURR) {
		curr = CURR;
		try{
			m.unbind(); 
		} catch(err){}
			d.unbind();
			b.unbind(); 
		c.update_view(curr);
		b.update_view(curr);
		d.update_view(curr);
		setTimeout( function(){
				try{
					m.bind(); 
				} catch(err){} 
				b.bind(); 
				d.bind();
			}, 300)
	}
    this.killloop=function(){
        clearTimeout(interval);
        interval = setTimeout(loop , AUTOPLAY_TIME);
    }
    let interval
    function loop(){
        clearTimeout(interval);
        //console.log('loop......')
        if(autoplay){
            //if(DIRECT == "R"){
                context_parent.act_triggered("R")   
            //}
        }
        interval = setTimeout(loop , AUTOPLAY_TIME);
    }
    //setTimeout(loop , AUTOPLAY_TIME);
	
 }


function CONTENT_CAROUSAL_STATIC2(_btnleft,_btnright,_dots,_content,_itemW , _total, _curr=1  , _pageAmount = 1, _titles){
	const btns={};
	btns.left = _btnleft;
	btns.right = _btnright;
	const dots = _dots;
	const content = _content;
	const item_w = _itemW ;
	const page_w = _itemW * _pageAmount;
	const total = _total;
	let curr= _curr
	const titles = _titles;
	const pageAmount = _pageAmount
	const autoplay = true;
	const context_parent= this;
	let DIRECT = "R"
	let last;
  ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/
   ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/
   ////////////////////////
  /*        sub objs    */
  ////////////////////////
  /*左右箭頭*/


  this.getCurr = function(){
  	return curr;
  }
  
  /*點點*/
  function DOTS(PARENT,_CURR , _TOTAL , PAGEAMOUNT = 1){
	 var DOM = content;
	 var context = this
	 var CURR = _CURR
	 var TOTAL = _TOTAL;
	 var PAGEMAX = Math.ceil(TOTAL / PAGEAMOUNT)
	 this.init = function() {
	     reset();
	     bind_action();
	 }
	 this.unbind = function() {
	 	 console.log('unbind action');
	     DOM.find(".dot").each(function() {
	         $(this).off('click');
	     })
	 }
	 this.bind = function() {
	     bind_action()
	 }

	function bind_action() {
	    console.log('bind action');
	    DOM.find(".dot").each(function() {
	        $(this).off('click').on('click', function() {
	            PARENT.killloop();
	            var id = $(this).data("id");
	            GLOBAL.ga.GT('product' , '.btn.product' + id);
	            console.log('dot clk');
	            context_parent.updateCurrView(id)
	            context.update_view(id);
	        })
	    })
	}


	  function kill_action(){
	  	 console.log('kill action');
		 DOM.find(".dot").off("click")
	  }
	  this.update_view=function(curr){
		  CURR = curr;
		  DOM.find(".dot").each(function(){
			   var id = Number($(this).data("id"));
			   if(id==CURR)
			   {
					TweenMax.to($(this).find('.deco') , .5 , {scaleX:1 , scaleY:1,ease:Back.easeOut})
			   } else {
					TweenMax.to($(this).find('.deco') , .5 , {scaleX:0 , scaleY:0,ease:Back.easeIn})
			   }
		  })
	  }

	   function reset (){
			
	   }
	   this.init();
	   this.update_view(CURR)
  }

   /*內容*/
   function CONTENT(PARENT, _CURR ,_TOTAL , TITLES,PAGEAMOUNT = 1 ){
	   var DOM = content;
	   var CURR = _CURR;
	   var PAGEMAX = Math.ceil(_TOTAL / PAGEAMOUNT)
	   this.init=function(){

		   this.update_view(CURR);
		   //initialPosition();
		   
	   }.bind(this);

	   function initialPosition(){
	   		console.log('initialPosition')
			
	   }
	  
	   this.update_view=function(curr){
		  var prop = [];
		  
		  DOM.find(".view").each(function(){
			  let id = Number($(this).data('id'));
 			  TweenMax.to($(this) , .5 ,{delay:(id == curr)? 0:0,  opacity: (id == curr)?1:0});
 			  let rnd = Math.random();
 			  if(curr == id){
 			  	DOM.append($(this));
 			  	if(rnd<.3)
 			  		TweenMax.fromTo($(this).find('.rightbg .bgp') , .7 ,{y:1000,x:0} , {y:0 ,x:0, ease:Cubic.easeInOut});
 			  	else if(rnd<.6){
 			  		TweenMax.fromTo($(this).find('.rightbg .bgp') , .7 ,{x:-1000,y:0} , {x:0 ,y:0, ease:Cubic.easeInOut});
 			  	}else{
 			  		TweenMax.fromTo($(this).find('.rightbg .bgp') , .7 ,{y:-1000,x:0} , {y:0 ,x:0, ease:Cubic.easeInOut});
 			  	}
 			  	let i =0;
 			  	$(this).find('.rightbg > div').not('.bgp').each(function(){
 			  		TweenMax.fromTo($(this), .5 ,{opacity:0 , x:50} , {delay : i , opacity:1 ,x:0, ease:Cubic.easeInOut});
 			  		i+=.1;
 			  	})

 			  	TweenMax.fromTo($(this).find('.main_prd') , 1 ,{opacity :0,y:(rnd>.5)?-30:30} , {opacity :1, y:0 , ease:Cubic.easeOut});
 			  	

 			  }
 			  

		  })
		  CURR = curr;
	   }

	   this.reset = function(){
	   }
	   this.init();
   }

	let c = new CONTENT(this,curr, total,titles,pageAmount);
	let d = new DOTS(this, curr , total, pageAmount);
	
	this.act_triggered = function(typ){ 
		
			d.unbind();
			
			   //last = curr;
			   if(typ=="L"){
				   if(curr>1)
				   {
					   curr--;					   
				   }else{
				   		curr=1;					  
				   }
				   c.update_view(curr);

			   }else{
				   if(curr<total)
				   {
					   curr++;
					   
				   }else{
				   		curr =1 ;
				   }
				   c.update_view(curr);
			   }

			   
			   d.update_view(curr);
			setTimeout( function(){
				
				
				d.bind();
			}, 600)

	}
	
	this.updateCurrView = function (CURR) {
		curr = CURR;
		try{
			m.unbind(); 
		} catch(err){}
			d.unbind();
			//b.unbind(); 
		c.update_view(curr);
		//b.update_view(curr);
		d.update_view(curr);

		setTimeout( function(){
				try{
					m.bind(); 
				} catch(err){} 
				//b.bind(); 
				d.bind();
			}, 600)
	}
	
	this.killloop=function(){
 		clearTimeout(interval);
 		interval = setTimeout(loop , 6500);
 	}
 	let interval
	function loop(){
		clearTimeout(interval);
		if(autoplay){
			if(DIRECT == "R"){
				context_parent.act_triggered("R")	
			}
		}
		interval = setTimeout(loop , 6500);
	}
	loop();
	
 }



/*看似無限的SLIDE SHOW*/
function CAROUSEL(obj){
		let direction = -1;
		let pace = 2;
		let origUnit = (device.mobile())? 640:679; //單元寬度
		let width  = origUnit * 4 * GLOBAL.scale; //一個REPEAT PATTERN的寬度
		let unit = origUnit * GLOBAL.scale; //縮放後單元寬度
		let time = (device.mobile())?.7:.9;
		var interval
		let tx = 0;
		let flag = 0;
		const loopt = 3300 
		var context = this;
		var mGIFS = {}
		var NAME;

		function unbind(){ $('.btn-left , .btn-right').off('click');}
		function clk(){
				unbind()
				var id = $(this).data("id");
				context.act(id);
				setTimeout(function(){ $('.btn-left , .btn-right').click(clk)} , 1100)
		}
		function bind(){
			
			$('.btn-left , .btn-right').click(clk)
			
		}
		
		/**/
		function loop(){
			move();
			interval = setTimeout( loop, loopt);

		}
		/*檢查是否離開VIEW WINDOW (REPEAT PATTERN)*/
		function chkIfLeaveWindow(){
			if(direction==-1){
				if(flag<-3){
					flag = flag%4;
					//console.log("flag ...."+flag)
					tx = flag * unit;
					TweenMax.set(obj ,{x:tx})   
				}
			}else {
				if(flag>0){
					flag = flag%4-4;
					//console.log("flag ...."+flag)
					tx = flag * unit;
					TweenMax.set(obj ,{x:tx})   
				}
			}

			

			if(device.mobile()){
				obj.find(".p.btn").each(function(){
					var id = Number($(this).data('id'));

					if(id != flag){
						TweenMax.set($(this) , {opacity :0});
					}
				})
			}

			 updateAnim(flag);
		}
		function resetAnim(){
			$(obj).find(".btn.p").each(function(){
				var id = Number($(this).data("id"));
				var name = $(this).data("name")
				try{
					mGIFS[name + id].killgif();
					} catch(err){
				}
				TweenMax.to($(this).find('.plabel'), .6, {opacity:0 /*,scaleX:.7,scaleY:.7*/,y:100, ease:Sine.easeInOut})
			})
		}

		function updateAnim(ID){
			mapIDtoName(ID)
			$(obj).find(".btn.p").each(function(){
				var id = Number($(this).data("id"));
				var name = $(this).data("name");
				if(id == ID /*&& name == NAME*/){
					TweenMax.to($(this).find('.plabel'), .6, {delay:0,opacity:1 ,scaleX:1,scaleY:1,y:0, ease:Back.easeOut});
					mGIFS[name + id].play();
				} else {
				}
			})
		}

		/*左右移動*/
		function move(){
			TweenMax.set(obj.find('.btn.p') , {opacity :1});



			if(direction==-1){
				tx -= unit;
				flag --;
				//console.log('loop....' + tx)
				TweenMax.to(obj ,time,{x: tx, ease:(!device.mobile())?Back.easeOut:Cubic.easeOut ,onComplete:chkIfLeaveWindow } )
			} else {
				tx += unit;
				flag ++;
				TweenMax.to(obj ,time,{x: tx, ease:(!device.mobile())?Back.easeOut:Cubic.easeOut ,onComplete:chkIfLeaveWindow} )
			}
			mapIDtoName(flag)
			//check boundary issu
			resetAnim();
			//updateAnim(flag);
		}
		function mapIDtoName(ID){
			$(obj).find(".btn.p").each(function(){
				var id = Number($(this).data("id"));
				var name = $(this).data("name")
				if(id == ID){
					NAME = name;
				} else {
				}
			})
		}
		/*初始每個GIF*/
		function generateGIFS(){
			$(obj).find(".btn.p").each(function(){
				var n = $(this).data('name')
				var id = $(this).data('id')
				//console.log("n + id..." + n+ id)
				mGIFS[n + id] = new GIF($(this) , n);
			 })
		}
		this.getName = function (){
			return NAME;
		}
		this.getFlag = function(){
			return flag;
		}
		/*隨著縮放更新寬度*/
		this.updateScale = function (){
			var sw = getBrowserWidth()
			var vw = (sw<1000)? sw :1000
			width  =  origUnit * 4 * GLOBAL.scale;
			unit = origUnit * GLOBAL.scale  ;
			if(!device.mobile()){
				TweenMax.to($('.kv .btn-left') , .5,{x: (vw - unit)*.5})
				TweenMax.to($('.kv .btn-right') ,.5,  {x:- (vw - unit)*.5})
			}
			
		}
		/*左右動作*/
		this.act=function(typ){
			//cacel loop
			clearTimeout(interval);
			if(typ =="l"){
				direction = -1;
			}else{
				direction = 1;
			}
			//alert('move')
			move();
			interval = setTimeout(loop , time * 2000 + loopt)
		}
		this.killCarousel=function(){
			clearTimeout(interval);

			$(obj).find(".btn.p").each(function(){
				var id = Number($(this).data("id"));
				var name = $(this).data("name")
				try{
					mGIFS[name + id].killgif();
					} catch(err){
				}
			})
		}
		this.init=function(){
			TweenMax.killTweensOf(obj);
			var sw = getBrowserWidth();
			var vw = (sw > 1000)? 1000: sw;
			tx = 0 ;
			flag = 0; 
			chkIfLeaveWindow();
			if(!device.mobile()){
				obj.css({'left': -1 * width + (vw - unit)*.5});     
			} else{
				obj.css({'left':-1 * width });  
			}
			clearTimeout(interval);

			//CAROUSEL!!!!
			loop(); 
			//PAN!!!            
			unbind()
			bind();
		}

		//if(device.mobile()){
			//var _pan = new PAN("sense" , context);    
		//}
		generateGIFS();
		//
		this.init();
	}



