
String.prototype.insert = function (index, string) {
  if (index > 0)
    return this.substring(0, index) + string + this.substring(index, this.length);
  else
    return string + this;
};

function redirectHandleFromMobile(SiteName){
	if ( !(device.mobile() || device.tablet()) ) {
	    let proj = SiteName + '/';
	    if (location.href.indexOf('/dev/') >= 0) {
	        proj += 'dev/';
	    }
	    var ind = location.href.indexOf(proj);
	    //location.href = location.href.insert(ind + proj.length, 'm/');
	    if(ind>=0)
	    location.href = location.href.replace("m/", "")
	} 
}
function redirectHandle(SiteName){
	if (device.mobile() || device.tablet()) {
	    let proj = SiteName + '/';
	    if (location.href.indexOf('/dev/') >= 0) {
	        proj += 'dev/';
	    }
	    var ind = location.href.indexOf(proj);
	    location.href = location.href.insert(ind + proj.length, 'm/');

	} 
}
function getQueryVariable() {
	const query = window.location.search.substring(1);
	return query;
}
function getParameterByName(name, url = window.location.href) {
	const tname = name.replace(/[\[\]]/g, '\\$&');
	// const regex = new RegExp('[?&]' + tname + '(=([^&#]*)|&|#|$)');
	const regex = new RegExp(`[?&]${tname}(=([^&#]*)|&|#|$)`);
	const results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function getBrowserHeight() {
	let objectH;
	
	if (document.body.clientHeight) {
		objectH = document.body.clientHeight * 1;
	}
	if (document.documentElement.clientHeight) {
		objectH = document.documentElement.clientHeight * 1;
	}
	if (window.innerHeight) {
		objectH = window.innerHeight * 1;
	}
	return objectH;
}
function getBrowserWidth() {
	let objectW;
	
	if (document.body.clientWidth) {
		objectW = document.body.clientWidth * 1;
	}
	if (document.documentElement.clientWidth) {
		objectW = document.documentElement.clientWidth * 1;
	}
	if (window.innerWidth) {
		objectW = window.innerWidth * 1;
	}
	return objectW;
}
function onresize() {
	let sw;
	let sh;
	let ratio;
	this.update = function () {
		sw = getBrowserWidth();
		sh = getBrowserHeight();
		
		
	};
	this.get_WHValue = function () {
		return { w: sw, h: sh };
	};


}


function SND_MODEL() {
	const context = this;
	let state = 'off';
	let player;
	this.init = function () {
		context.update_view();
		const audio5js = new Audio5js({
			ready: () => {
				player = this;
				this.load('snd/001.mp3');
			},
		});
	};
	this.switch = function () {
		if (state === 'off') {
			context.setOn(1);
		} else {
			context.setOn(0);
		}
	};
	this.setOn = function (typ) {
		if (typ)	{
			state = 'on';
			player.play();
		} else {
			state = 'off';
			player.pause();
		}
		context.update_view();
	};
	this.update_view = function () {
		if (state === 'off') {
			$('.mmu').css('opacity', 0.5);
		} else {
			$('.mmu').css('opacity', 1);
		}
	};
	this.init();
}
function getInternetExplorerVersion() {
    var rv = -1; // Return value assumes failure.
    
        var ua = navigator.userAgent;
        var re = ua.indexOf("MSIE ");
        if (ua.indexOf("MSIE ") >=0 || ua.indexOf("Trident/") >=0 || ua.indexOf("Edge/") >=0 )
        {
        	rv = "IE"
        };
    	console.log("rv:" + rv)
    return rv;
}
function checkVersion() {
    var msg = "You’re not using Windows Internet Explorer.";
    var ver = getInternetExplorerVersion();
    if (ver > -1) {
        if (ver >= 9.0)
            msg = "Internet Explorer >= 9";
        else
            msg = "ie8"
    }
    return msg;
}

class LoadModle {	
	constructor(imgs , cb = null){
		this.$imgs = imgs
		this.imagesN = imgs.length;
		this.cb = cb;
		this.c = 0;
		this.count = 0;
		this.oldInd = 0;
		this.init();
	}
	reset(){
	}
	anim(typ) {
		console.log('anim...............');
	}
	pngFix() {
		const self = $(this);
		self.find('img[src$=".png"],img[src$=".gif"]').each(() => {
			console.log('png Fix!....')
			this.style.filter =
			`progid:DXImageTransform.Microsoft.AlphaImageLoader(enabled='true',sizingMethod='image',src='${this.src}')`;
		});
	}
	init() {
		//preventScroll()
		this.reset();
		this.$imgs.imagesLoaded().progress((instance, image) => {
			this.count++;
			let percent = Math.floor((this.count / this.$imgs.length) * 100) ;
			let txt = $('.loading .ld .txt');
			txt.html(percent)
			const ind = parseInt(percent / 11, 10) + 1;
			
			this.oldInd = this.ind;
			if (this.count === this.$imgs.length) {
				this.pngFix();
				
				if(this.cb){
					this.cb();
				}
			}
		});
		
	};
	
}
function preventScroll(typ = true){
	if(typ){
		if (device.mobile()) {

            var fixed = [document.getElementById('pop-about'),document.getElementById('partmb') ];
            for(var i in fixed){
            	//fixed[i].removeEventListener('touchmove', false);
                fixed[i].addEventListener('touchmove', function(e) {
                e.preventDefault();
            }, false);
            }
        }
	}else {
		var fixed = [document.getElementById('pop-about'),document.getElementById('partmb') ];
            for(var i in fixed){
                fixed[i].removeEventListener('touchmove', false);
            }
	}
        
}

function updateImg(obj, _src) {
	obj.attr('src', _src);
}
function Blength() {
	const arr = this.match(/[^\x00-\xff]/ig);
	return (arr == null) ? this.length : this.length + arr.length;
}
function getLengthInBytes(str) {
  var b = str.match(/[^\x00-\xff]/g);
  return (str.length + (!b ? 0: b.length)); 
}

export {
	getInternetExplorerVersion as getInternetExplorerVersion , 
	checkVersion as checkVersion,
	LoadModle as LoadModle,
	getBrowserWidth as getBrowserWidth,
	getBrowserHeight as getBrowserHeight,
	getParameterByName as getParameterByName,
	updateImg as updateImg,
	redirectHandle as redirectHandle,
	getQueryVariable,
	getLengthInBytes,
	redirectHandleFromMobile,
}
