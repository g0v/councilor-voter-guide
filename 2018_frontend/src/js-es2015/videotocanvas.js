import {GLOBAL} from './config.js';
function VideoSolutions(){
    var audioLoaded = false;
    var call;
    var video;
    var isTouched = false;

    var meter
    var canvasVideo;
    var isiOS = navigator.userAgent.match(/iPhone|iPad|iPod/i);
    var isiPad = navigator.userAgent.match(/iPad/i);
    var isiOSFB = navigator.userAgent.match(/MessengerForiOS|FBIOS/i);
    var isiOSFBMessenger = navigator.userAgent.match(/MessengerForiOS/i);
    var isWechat = navigator.userAgent.match(/MicroMessenger/i);
    var isLine = navigator.userAgent.match(/Line/i);
    var isChrome = navigator.userAgent.match(/Chrome/i);
    var language = "cn";
    var oldiOS = false;
    var useCanvas = true;    

    this.playVideo = function(){
         GLOBAL.vstate = 'play';
         if(useCanvas){

            canvasVideo.play();
         }
         else {
            video.play();
         }
    }



    this.stopVideo = function(){
         GLOBAL.vstate = 'stop';
         if(useCanvas){
            canvasVideo.pause();
         }
         else {
            video.pause();
         }
    }
    this.getCurrentTime=function(){
         if(useCanvas){
            return video.currentTime;
         }
         else {
            return video.currentTime;
         }
    }

    this.getuseCanvas = function(){
        return useCanvas;
    }  
    this.init = function(){
        if (isiOS) {
            var v = (navigator.appVersion).match(/OS (\d+)_(\d+)_?(\d+)?/);
            var iOSversion = [parseInt(v[1], 10), parseInt(v[2], 10), parseInt(v[3] || 0, 10)];
            if (isiPad || iOSversion[0] < 8) {
                oldiOS = true;
            }
        }
        if (isiOS && !isWechat && !oldiOS ) {
            useCanvas = true;
        } else {
            useCanvas = false;
        }
        const requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };
        window.requestAnimationFrame = requestAnimationFrame;
        //meter = new FPSMeter();
    }

    this.clkCharactor = function(){
        isTouched = false;
        video  = document.getElementById('video_p');
        GLOBAL.canplay = false;
        //正常與否
        let normal = (GLOBAL.NORMAL)? 'A':'B';
        var path = (Math.random() > .5)? 'http://819c375429527e275f54-b1b6e7de992e67a5fcec75da074835f8.r32.cf6.rackcdn.com/' :'http://1576f313e8e0e85b348b-34f6c4fb34bf5129b497f2e2442e93cb.r3.cf6.rackcdn.com/' ;
        //
        //
        if(device.mobile())
        $(video).html('<source src="'+path +GLOBAL.CHOOSE+'_'+normal+'_400x724.mp4" type="video/mp4">');
        else
        $(video).html('<source src="'+path+'/ten/'+GLOBAL.CHOOSE+'_'+normal+'_400x624.mp4" type="video/mp4">');

        if(!audioLoaded)
        {
            loadMedia();
        }


        video.oncanplaythrough = function() {
           console.log("Can start playing video");
           GLOBAL.canplay = true;
            
        };

    }

    function loadMedia() {
//        console.log(useCanvas, audioLoaded);
        if(useCanvas){
            if (!audioLoaded) {
                audioLoaded = true;
                if (useCanvas) {
                    canvasVideo = new CanvasVideoPlayer({
                        videoSelector: '.video_p',
                        canvasSelector: '.canvas_p',
                        audio: true,
                        fullscreen: true,
                        pausable: false
                    });
                    //$(introVideo).css({width:"1px", height:"1px"});
                    //alert('load!')
                }
            }

        } else{        

            $('canvas').remove();
            //
            if (!device.mobile()) {
                    $(video).css({ "width": "350px", "height": "625px" });
                    $('.vdo_box').css({ "width": "350px", "height": "625px", 'margin': '0 auto' })
                } else {
                    
                    $(video).css({ "width": "640px", "height": "1125px"  });
            }
                $(video).css({ "margin": "0 auto" })
        }

    }

    this.PlayMedia =function (){
        GLOBAL.vstate = 'playing';
        if (useCanvas) {

            canvasVideo.setCanvasSize();
            //alert("6秒後播放!")
            canvasVideo.play(); 
            //setTimeout(function() { canvasVideo.play(); }, 6000)

        } else {
            video.play();
        }
       
    }
    this.PlayMediaAndPause =function (){
        GLOBAL.vstate = 'stop';
        if (useCanvas) {

            canvasVideo.setCanvasSize();
            //alert("6秒後播放!")
            canvasVideo.play(); 
            //setTimeout(function() { canvasVideo.play(); }, 6000)

        } else {
            video.play();
        }
        setTimeout(function(){
        if(useCanvas){
            canvasVideo.pause();
         }
         else {
            video.pause();
         }
        } , 200)
       
    }
    
    

}
var cvpHandlers = {
    canvasClickHandler: null,
    videoTimeUpdateHandler: null,
    videoCanPlayHandler: null,
    windowResizeHandler: null
    };

var CanvasVideoPlayer = function(options) {
    var i;

    this.options = {
        framesPerSecond: 20,
        hideVideo: true,
        autoplay: false,
        audio: false,
        timelineSelector: false,
        resetOnLastFrame: true,
        loop: false,
        fullscreen: false,
        followAudio: true,
        pausable: true
    };
    
    

    for (i in options) {
        this.options[i] = options[i];
    }
    this.videoLoaded = false;
    this.video = document.querySelector(this.options.videoSelector);
    this.canvas = document.querySelector(this.options.canvasSelector);
    this.timeline = document.querySelector(this.options.timelineSelector);
    this.timelinePassed = document.querySelector(this.options.timelineSelector + '> div');

    if (!this.options.videoSelector || !this.video) {
        console.error('No "videoSelector" property, or the element is not found');
        return;
    }

    if (!this.options.canvasSelector || !this.canvas) {
        console.error('No "canvasSelector" property, or the element is not found');
        return;
    }

    if (this.options.timelineSelector && !this.timeline) {
        console.error('Element for the "timelineSelector" selector not found');
        return;
    }

    if (this.options.timelineSelector && !this.timelinePassed) {
        console.error('Element for the "timelinePassed" not found');
        return;
    }

    if (this.options.audio) {
        if (typeof(this.options.audio) === 'string'){
            // Use audio selector from options if specified
            this.audio = document.querySelectorAll(this.options.audio)[0];

            if (!this.audio) {
                console.error('Element for the "audio" not found');
                return;
            }
        } else {

            // Creates audio element which uses same video sources
            this.audio = document.createElement('audio');
            this.audio.innerHTML = this.video.innerHTML;
            this.video.parentNode.insertBefore(this.audio, this.video);
            this.audio.load();
        }

        var iOS = /iPad|iPhone|iPod/.test(navigator.platform);
        if (iOS) {
            // Autoplay doesn't work with audio on iOS
            // User have to manually start the audio
            this.options.autoplay = false;
        }
    }

    // Canvas context
    this.ctx = this.canvas.getContext('2d');

    this.playing = false;

    this.resizeTimeoutReference = false;
    this.RESIZE_TIMEOUT = 1000;

    this.init();
    this.bind();
};

CanvasVideoPlayer.prototype.init = function() {
    this.videoLoaded = false;
    this.video.load();
    this.video.onload=function(){this.videoLoaded=true;};

    this.setCanvasSize();

    if (this.options.hideVideo) {
        //this.video.style.display = 'none';
    }
};

// Used most of the jQuery code for the .offset() method
CanvasVideoPlayer.prototype.getOffset = function(elem) {
    var docElem, rect, doc;

    if (!elem) {
        return;
    }

    rect = elem.getBoundingClientRect();

    // Make sure element is not hidden (display: none) or disconnected
    if (rect.width || rect.height || elem.getClientRects().length) {
        doc = elem.ownerDocument;
        docElem = doc.documentElement;

        return {
            top: rect.top + window.pageYOffset - docElem.clientTop,
            left: rect.left + window.pageXOffset - docElem.clientLeft
        };
    }
};

CanvasVideoPlayer.prototype.jumpTo = function(percentage) {
    this.video.currentTime = this.video.duration * percentage;

    if (this.options.audio) {
        this.audio.currentTime = this.audio.duration * percentage;
    }
};

CanvasVideoPlayer.prototype.bind = function() {
    var self = this;

    // Playes or pauses video on canvas click
    this.canvas.addEventListener('click', cvpHandlers.canvasClickHandler = function() {
        if(self.options.pausable)
            self.playPause();
    });

    // On every time update draws frame
    this.video.addEventListener('timeupdate', cvpHandlers.videoTimeUpdateHandler = function() {
        
        self.drawFrame();
        if (self.options.timelineSelector) {
            self.updateTimeline();
        }
    });

    // Draws first frame
    this.video.addEventListener('canplay', cvpHandlers.videoCanPlayHandler = function() {
        self.drawFrame();
    });

    // To be sure 'canplay' event that isn't already fired
    if (this.video.readyState >= 2) {
        self.drawFrame();
    }

    if (self.options.autoplay) {
      self.play();
    }

    // Click on the video seek video
    if (self.options.timelineSelector) {
        this.timeline.addEventListener('click', function(e) {
            var offset = e.clientX - self.getOffset(self.canvas).left;
            var percentage = offset / self.timeline.offsetWidth;
            self.jumpTo(percentage);
        });
    }

    // Cache canvas size on resize (doing it only once in a second)
    window.addEventListener('resize', cvpHandlers.windowResizeHandler = function() {
        clearTimeout(self.resizeTimeoutReference);

        self.resizeTimeoutReference = setTimeout(function() {
            self.setCanvasSize();
            self.drawFrame();
        }, self.RESIZE_TIMEOUT);
    });

    this.unbind = function() {
        this.canvas.removeEventListener('click', cvpHandlers.canvasClickHandler);
        this.video.removeEventListener('timeupdate', cvpHandlers.videoTimeUpdateHandler);
        this.video.removeEventListener('canplay', cvpHandlers.videoCanPlayHandler);
        window.removeEventListener('resize', cvpHandlers.windowResizeHandler);

        if (this.options.audio) {
            this.audio.parentNode.removeChild(this.audio);
        }
    };
};

CanvasVideoPlayer.prototype.updateTimeline = function() {
    var percentage = (this.video.currentTime * 100 / this.video.duration).toFixed(2);
    this.timelinePassed.style.width = percentage + '%';
};
    //var clipY = 0;
    //var clipH = 1280;
CanvasVideoPlayer.prototype.setCanvasSize = function() {
    
    //console.log("this.options.fullscreen", this.options.fullscreen)
    if (!this.options.fullscreen)
    {
        this.width = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        this.canvas.setAttribute('width', this.width);
        this.canvas.setAttribute('height', this.height);
        
    }else{
        
        var scaleX = window.innerWidth / this.canvas.width;
        var scaleY = window.innerHeight / this.canvas.height;
        
        
        var scale =  window.innerHeight/window.innerWidth;
        
        if(scale>16/9)
        {
            this.canvas.style.width = "100%";
            this.canvas.style.height = "auto";
        }
        //console.log("set not full screen", this.canvas.clientWidth, this.canvas.clientHeight);
        this.width = this.canvas.clientWidth;
        //this.height = this.canvas.clientWidth * scale;
        //scale = this.width/this.height;
        //this.clipH = parseInt(720*scale);
        //this.clipY = parseInt((1280-this.clipH)/2);
        //console.log('width', this.width, 'height', this.height, this.clipH, this.clipY, 1280-this.clipH)
        
        this.height = this.canvas.clientWidth/9*16;
        if(this.width<=0) this.width=640;
        if(this.height<=0) this.height=720 * 640 / 404;
        //this.canvas.setAttribute('width', this.width);
        //this.canvas.setAttribute('height', this.height);
        
        this.clipH = window.innerHeight;
        this.clipY = parseInt((window.innerWidth/9*16-this.clipH)/2);
        
    //console.log('width', this.width, 'height', this.height, this.clipH, this.clipY, 1280-this.clipH)
        //var scaleToFit = Math.min(scaleX, scaleY);
        var scaleToCover = Math.max(scaleX, scaleY);
        //console.log(this.canvas.parentNode.style.transform, scaleToCover, window.pageYOffset, document.body.scrollTop)
        var string = "scale(" + scaleToCover + ") translateY(-"+this.clipY/scaleToCover+"px)";
        this.canvas.parentNode.style.transform = null;  
        this.canvas.parentNode.style.transform = string;
        this.canvas.parentNode.style.webkitTransform = string;
        this.canvas.parentNode.style.mozTransform = string;
        this.canvas.parentNode.style.oTransform = string;
        this.canvas.parentNode.style.msTransform = string;
    }
};

CanvasVideoPlayer.prototype.play = function() {
    //this.video = self.video;
    //this.audio = self.audio;
    this.lastTime = Date.now();
    this.playing = true;
    this.loop();
    if (this.options.audio) {
        //console.log("audio", this.options.audio, this.audio)
        if(this.options.followAudio)
        {
        // Resync audio and video
        //this.audio.currentTime = this.video.currentTime;
            this.video.currentTime = this.audio.currentTime;
        }else{
            this.audio.currentTime = this.video.currentTime;
        }
        this.audio.play();
        
    }
};

CanvasVideoPlayer.prototype.pause = function() {

    this.playing = false;

    if (this.options.audio) {
        this.audio.pause();
    }
};

CanvasVideoPlayer.prototype.playPause = function() {
    if (this.playing) {
        this.pause();
    }
    else {
        this.play();
    }
};

CanvasVideoPlayer.prototype.dispose = function() {
    this.video.src = "";
    this.audio.src = ""; 
}

CanvasVideoPlayer.prototype.resume = function()
{
    this.play();
}
CanvasVideoPlayer.prototype.loop = function() {
    var self = this;

    var time = Date.now();
    var elapsed = (time - this.lastTime) / 1000;
    
    // Render
    if(elapsed >= (1 / this.options.framesPerSecond)) {
        this.video.currentTime = this.video.currentTime + elapsed;
        this.lastTime = time;
        // Resync audio and video if they drift more than 300ms apart
        if(this.audio && Math.abs(this.audio.currentTime - this.video.currentTime) > 0.3){
            //this.audio.currentTime = this.video.currentTime;
            if(this.options.followAudio)
            {
            // Resync audio and video
            //this.audio.currentTime = this.video.currentTime;
                //console.log("sync video")
                this.video.currentTime = this.audio.currentTime;
            }else{
                //console.log("sync audio")
                this.audio.currentTime = this.video.currentTime;
            }
            
            if(this.options.pausable)
            {
                this.pause();
                
                spinner.spin();
                $("#videoBox").append(spinner.el);
                
                setTimeout(function(){
                    spinner.stop();
                    self.play();
                }, 3000);
            }
                
        }
    }

    // If we are at the end of the video stop
    if (this.video.currentTime >= this.video.duration) {
        this.playing = false;

        if (this.options.resetOnLastFrame === true) {
            this.video.currentTime = 0;
        }

        if (this.options.loop === true) {
            this.video.currentTime = 0;
            this.play();
        }
    }

    if (this.playing) {
        this.animationFrame = requestAnimationFrame(function(){
            self.loop();
        });
    }
    else {
        cancelAnimationFrame(this.animationFrame);
    }
};

CanvasVideoPlayer.prototype.drawFrame = function() {
    
    //this.ctx.drawImage(this.video, 0,this.clipY,720,this.clipH, 0, 0, this.width, this.height);
    //if(this.videoLoaded)
    this.ctx.drawImage(this.video, 0, 0, this.width, this.height);
    //meter.tick();
};
export {
    VideoSolutions as VideoSolutions , 
    CanvasVideoPlayer as CanvasVideoPlayer
    
};