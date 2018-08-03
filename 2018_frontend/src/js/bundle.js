(function () {
'use strict';

var classCallCheck = function (instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
};

var createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);
    if (staticProps) defineProperties(Constructor, staticProps);
    return Constructor;
  };
}();







var get = function get(object, property, receiver) {
  if (object === null) object = Function.prototype;
  var desc = Object.getOwnPropertyDescriptor(object, property);

  if (desc === undefined) {
    var parent = Object.getPrototypeOf(object);

    if (parent === null) {
      return undefined;
    } else {
      return get(parent, property, receiver);
    }
  } else if ("value" in desc) {
    return desc.value;
  } else {
    var getter = desc.get;

    if (getter === undefined) {
      return undefined;
    }

    return getter.call(receiver);
  }
};

var inherits = function (subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
  }

  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      enumerable: false,
      writable: true,
      configurable: true
    }
  });
  if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
};











var possibleConstructorReturn = function (self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }

  return call && (typeof call === "object" || typeof call === "function") ? call : self;
};



var set = function set(object, property, value, receiver) {
  var desc = Object.getOwnPropertyDescriptor(object, property);

  if (desc === undefined) {
    var parent = Object.getPrototypeOf(object);

    if (parent !== null) {
      set(parent, property, value, receiver);
    }
  } else if ("value" in desc && desc.writable) {
    desc.value = value;
  } else {
    var setter = desc.set;

    if (setter !== undefined) {
      setter.call(receiver, value);
    }
  }

  return value;
};

String.prototype.insert = function (index, string) {
	if (index > 0) return this.substring(0, index) + string + this.substring(index, this.length);else return string + this;
};

function getBrowserHeight() {
	var objectH = void 0;

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
	var objectW = void 0;

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
var LoadModle = function () {
	function LoadModle(imgs) {
		var cb = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
		classCallCheck(this, LoadModle);

		this.$imgs = imgs;
		this.imagesN = imgs.length;
		this.cb = cb;
		this.c = 0;
		this.count = 0;
		this.oldInd = 0;
		this.init();
	}

	createClass(LoadModle, [{
		key: 'reset',
		value: function reset() {}
	}, {
		key: 'anim',
		value: function anim(typ) {
			console.log('anim...............');
		}
	}, {
		key: 'pngFix',
		value: function pngFix() {
			var _this2 = this;

			var self = $(this);
			self.find('img[src$=".png"],img[src$=".gif"]').each(function () {
				console.log('png Fix!....');
				_this2.style.filter = 'progid:DXImageTransform.Microsoft.AlphaImageLoader(enabled=\'true\',sizingMethod=\'image\',src=\'' + _this2.src + '\')';
			});
		}
	}, {
		key: 'init',
		value: function init() {
			var _this3 = this;

			//preventScroll()
			this.reset();
			this.$imgs.imagesLoaded().progress(function (instance, image) {
				_this3.count++;
				var percent = Math.floor(_this3.count / _this3.$imgs.length * 100);
				var txt = $('.loading .ld .txt');
				txt.html(percent);
				var ind = parseInt(percent / 11, 10) + 1;

				_this3.oldInd = _this3.ind;
				if (_this3.count === _this3.$imgs.length) {
					_this3.pngFix();

					if (_this3.cb) {
						_this3.cb();
					}
				}
			});
		}
	}]);
	return LoadModle;
}();

function updateImg(obj, _src) {
	obj.attr('src', _src);
}

var GLOBAL = {};
GLOBAL.TEST = 0;
GLOBAL.host = './';
GLOBAL.mobile_root = './';
GLOBAL.api_root = './';
GLOBAL.gaId = '';
GLOBAL.fbAppId = '135077620505268';
//GLOBAL.CDN = 'https://0aeeaec76b7f9d2c4285-1aea3a9a72fefa77bacf84f29a803dcb.ssl.cf6.rackcdn.com/'

GLOBAL.geo = {
    "六都": {
        cities: [{ cne: '臺北市', eng: 'TPE' }, { cne: '新北市', eng: 'TPH' }, { cne: '桃園市', eng: 'TYC' }, { cne: '臺中市', eng: 'TXG' }, { cne: '臺南市', eng: 'TNN' }, { cne: '高雄市', eng: 'KHH' }]
    },
    "北部": {
        cities: [{ cne: '臺北市', eng: 'TPE' }, { cne: '新北市', eng: 'TPH' }, { cne: '基隆市', eng: 'KLU' }, { cne: '桃園市', eng: 'TYC' }, { cne: '新竹市', eng: 'HSC' }, { cne: '新竹縣', eng: 'HSH' }]
    },
    "中部": {
        cities: [{ cne: '苗栗縣', eng: 'MAL' },
        // { cne: '苗栗市', eng: 'MAC' },
        { cne: '臺中市', eng: 'TXG' }, { cne: '彰化縣', eng: 'CWH' },
        // { cne: '彰化市', eng: 'CWS' },
        // { cne: '南投市', eng: 'NTC' },
        { cne: '南投縣', eng: 'NTO' }, { cne: '雲林縣', eng: 'YUN' }]
    },
    "南部": {
        cities: [{ cne: '嘉義縣', eng: 'CHY' }, { cne: '嘉義市', eng: 'CYI' }, { cne: '臺南市', eng: 'TNN' }, { cne: '高雄市', eng: 'KHH' }, { cne: '屏東縣', eng: 'IUH' }]
    },
    "東部": {
        cities: [{ cne: '宜蘭縣', eng: 'ILN' },
        // { cne: '宜蘭市', eng: 'ILC' },
        { cne: '花蓮縣', eng: 'HWA' },
        // { cne: '花蓮市', eng: 'HWC' },
        // { cne: '臺東市', eng: 'TTC' },
        { cne: '臺東縣', eng: 'TTT' }]
    },
    "離島": {
        cities: [{ cne: '金門縣', eng: 'KMN' }, { cne: '連江縣', eng: 'LNN' }, { cne: '澎湖縣', eng: 'PEH' }]
    }

};

GLOBAL.allcities = [{ cne: '臺北市', eng: 'TPE' }, { cne: '新北市', eng: 'TPH' }, { cne: '桃園市', eng: 'TYC' }, { cne: '臺中市', eng: 'TXG' }, { cne: '臺南市', eng: 'TNN' }, { cne: '高雄市', eng: 'KHH' }, { cne: '臺北市', eng: 'TPE' }, { cne: '新北市', eng: 'TPH' }, { cne: '基隆市', eng: 'KLU' }, { cne: '桃園市', eng: 'TYC' }, { cne: '新竹市', eng: 'HSC' }, { cne: '新竹縣', eng: 'HSH' }, { cne: '苗栗縣', eng: 'MAL' }, { cne: '苗栗市', eng: 'MAC' }, { cne: '臺中市', eng: 'TXG' }, { cne: '彰化縣', eng: 'CWH' }, { cne: '彰化市', eng: 'CWS' }, { cne: '南投市', eng: 'NTC' }, { cne: '南投縣', eng: 'NTO' }, { cne: '雲林縣', eng: 'YUN' }, { cne: '嘉義縣', eng: 'CHY' }, { cne: '嘉義市', eng: 'CYI' }, { cne: '臺南市', eng: 'TNN' }, { cne: '高雄市', eng: 'KHH' }, { cne: '屏東縣', eng: 'IUH' }, { cne: '屏東市', eng: 'PTS' }, { cne: '宜蘭縣', eng: 'ILN' }, { cne: '宜蘭市', eng: 'ILC' }, { cne: '花蓮縣', eng: 'HWA' }, { cne: '花蓮市', eng: 'HWC' }, { cne: '臺東市', eng: 'TTC' }, { cne: '臺東縣', eng: 'TTT' }, { cne: '金門縣', eng: 'KMN' }, { cne: '連江縣', eng: 'LNN' }, { cne: '澎湖縣', eng: 'PEH' }];

function YTT(vid, ElementID) {
  var tag = document.createElement('script');
  var state = "init";

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  var player;
  this.get_state = function () {
    return state;
  };
  this.onYouTubeIframeAPIReady = function () {

    player = new YT.Player(ElementID, {

      height: '100%',
      width: '100%',
      videoId: vid,
      playerVars: { 'autoplay': 0, 'rel': 0, 'showinfo': 0 },
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }
    });
  };

  this.stop = function () {
    stopVideo();
  };
  this.play = function () {
    player.playVideo();
  };
  this.loadvdo = function (id) {
    player.loadVideoById(id);
    player.stopVideo();
  };

  function onPlayerReady(event) {
    state = "ready";
    if (device.mobile() || device.tablet()) {} else {}
    //event.target.playVideo();


    //console.log("vdo:"+event)
  }

  var done = false;

  function onPlayerStateChange(event) {
    if (event.data == "1") {
      console.log("vdo:" + event.data);
      GLOBAL.ga.GT('/video.' + vid, '.btn.play-' + ElementID);
    }
  }
  function stopVideo() {
    player.stopVideo();
  }
}

var STATUS_POLLING_INTERVAL_MILLIS = 60 * 1000; // One minute.


/**
 * YouTube video uploader class
 *
 * @constructor
 */
var UploadVideo = function UploadVideo() {
  /**
   * The array of tags for the new YouTube video.
   *
   * @attribute tags
   * @type Array.<string>
   * @default ['google-cors-upload']
   */
  this.tags = ['360-cors-upload'];

  /**
   * The numeric YouTube
   * [category id](https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.videoCategories.list?part=snippet®ionCode=us).
   *
   * @attribute categoryId
   * @type number
   * @default 22
   */
  this.categoryId = 22;

  /**
   * The id of the new video.
   *
   * @attribute videoId
   * @type string
   * @default ''
   */
  this.videoId = '';

  this.uploadStartTime = 0;
};

UploadVideo.prototype.ready = function (accessToken) {
  this.accessToken = accessToken;
  this.gapi = gapi;
  this.authenticated = true;
  this.gapi.client.request({
    path: '/youtube/v3/channels',
    params: {
      part: 'snippet',
      mine: true
    },
    callback: function (response) {
      if (response.error) {
        console.log(response.error.message);
      } else {
        $('#channel-name').text(response.items[0].snippet.title);
        $('#channel-thumbnail').attr('src', response.items[0].snippet.thumbnails.default.url);

        $('.pre-sign-in').hide();
        $('.post-sign-in').show();
      }
    }.bind(this)
  });
  $('#button').on("click", this.handleUploadClicked.bind(this));
};

/**
 * Uploads a video file to YouTube.
 *
 * @method uploadFile
 * @param {object} file File object corresponding to the video to upload.
 */
UploadVideo.prototype.uploadFile = function (file) {
  var metadata = {
    snippet: {
      title: $('#title').val(),
      description: $('#description').text(),
      tags: this.tags,
      categoryId: this.categoryId
    },
    status: {
      privacyStatus: $('#privacy-status option:selected').text()
    }
  };
  var uploader = new MediaUploader({
    baseUrl: 'https://www.googleapis.com/upload/youtube/v3/videos',
    file: file,
    token: this.accessToken,
    metadata: metadata,
    params: {
      part: Object.keys(metadata).join(',')
    },
    onError: function (data) {
      var message = data;
      // Assuming the error is raised by the YouTube API, data will be
      // a JSON string with error.message set. That may not be the
      // only time onError will be raised, though.
      try {
        var errorResponse = JSON.parse(data);
        message = errorResponse.error.message;
      } finally {
        alert(message);
      }
    }.bind(this),
    onProgress: function (data) {
      var currentTime = Date.now();
      var bytesUploaded = data.loaded;
      var totalBytes = data.total;
      // The times are in millis, so we need to divide by 1000 to get seconds.
      var bytesPerSecond = bytesUploaded / ((currentTime - this.uploadStartTime) / 1000);
      var estimatedSecondsRemaining = (totalBytes - bytesUploaded) / bytesPerSecond;
      var percentageComplete = bytesUploaded * 100 / totalBytes;

      $('#upload-progress').attr({
        value: bytesUploaded,
        max: totalBytes
      });

      $('#percent-transferred').text(percentageComplete);
      $('#bytes-transferred').text(bytesUploaded);
      $('#total-bytes').text(totalBytes);

      $('.during-upload').show();
    }.bind(this),
    onComplete: function (data) {
      var uploadResponse = JSON.parse(data);
      this.videoId = uploadResponse.id;
      $('#video-id').text(this.videoId);
      $('.post-upload').show();
      this.pollForVideoStatus();
    }.bind(this)
  });
  // This won't correspond to the *exact* start of the upload, but it should be close enough.
  this.uploadStartTime = Date.now();
  uploader.upload();
};

UploadVideo.prototype.handleUploadClicked = function () {
  $('#button').attr('disabled', true);
  this.uploadFile($('#file').get(0).files[0]);
};

UploadVideo.prototype.pollForVideoStatus = function () {
  this.gapi.client.request({
    path: '/youtube/v3/videos',
    params: {
      part: 'status,player',
      id: this.videoId
    },
    callback: function (response) {
      if (response.error) {
        // The status polling failed.
        console.log(response.error.message);
        setTimeout(this.pollForVideoStatus.bind(this), STATUS_POLLING_INTERVAL_MILLIS);
      } else {
        var uploadStatus = response.items[0].status.uploadStatus;
        switch (uploadStatus) {
          // This is a non-final status, so we need to poll again.
          case 'uploaded':
            $('#post-upload-status').append('<li>Upload status: ' + uploadStatus + '</li>');
            setTimeout(this.pollForVideoStatus.bind(this), STATUS_POLLING_INTERVAL_MILLIS);
            break;
          // The video was successfully transcoded and is available.
          case 'processed':
            $('#player').append(response.items[0].player.embedHtml);
            $('#post-upload-status').append('<li>Final status.</li>');
            break;
          // All other statuses indicate a permanent transcoding failure.
          default:
            $('#post-upload-status').append('<li>Transcoding failed.</li>');
            break;
        }
      }
    }.bind(this)
  });
};

var Main = function () {
	function Main() {
		var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'main';
		var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
		var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
		var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;
		classCallCheck(this, Main);

		this.NAME = NAME;
		this.ifFB = ifFB;
		this.ifYT = ifYT;
		this.ifScrollHandle = ifScrollHandle;
	}

	createClass(Main, [{
		key: 'bind',
		value: function bind() {
			console.log(this.NAME + ' binding.....');
		}
	}, {
		key: 'init',
		value: function init() {
			console.log(this.NAME + ' initialing.....');
			var interval = void 0;
			if (this.ifFB) {
				console.log('page:' + this.NAME + ' add fb ing.....');
			}
			if (this.ifYT) {
				console.log('page:' + this.NAME + ' add youtube.....');
				this.YT = new YTT($('.yt').data('id'), 'player');
				onYouTubeIframeAPIReady = this.YT.onYouTubeIframeAPIReady;
			}
			if (this.ifScrollHandle) {
				var _scrollHandle2 = function _scrollHandle2(e) {
					// if(e){
					// 	e.preventDefault();
					// }
					var page = $('#page').val();
					var top = $(window).scrollTop();
					var bg = $('.navbar .bg-cover');
					var statenav = $('.navbar-menu').attr('data-toggle');
					var dir = GLOBAL.oldtop < top ? 'down' : 'up';
					GLOBAL.top = top;if (top > 60 || statenav == 'expand') {
						TweenMax.to(bg, .5, { opacity: 1, ease: Expo.easeOut });
					} else {
						TweenMax.to(bg, .5, { opacity: 0, ease: Expo.easeOut });
					}

					if (page == 'index') {
						var vh = getBrowserHeight();
						clearTimeout(interval);

						if (top >= vh - 80) {
							$('.navbar-brand').stop().fadeIn(500);
						} else {
							$('.navbar-brand').stop().fadeOut();
						}
					} else {
						$('.navbar-brand').fadeIn(500);
					}

					if (page.indexOf('resume') >= 0) {
						if (statenav == 'collapse') {
							if (top > 60) {
								TweenMax.to($('.navbar'), .5, { top: -$('.navbar').height(), ease: Expo.easeOut });
								TweenMax.to($('.wrapper-header'), .5, { top: 0, ease: Expo.easeOut });
							} else {
								TweenMax.to($('.navbar'), .5, { top: 0, ease: Expo.easeOut });
								TweenMax.to($('.wrapper-header'), .5, { top: $('.navbar').height(), ease: Expo.easeOut });
							}
						}
					}
					GLOBAL.oldtop = top;
				};

				window.onscroll = function (e) {
					_scrollHandle2(e);
				};

				_scrollHandle2();
			}
			if (location.href.indexOf('localhost') >= 0) {
				this.TEST = true;
				console.log('run test mode......');
			}

			/*common component*/
			//new SUB_MENU();
			this.bind();
		}
	}, {
		key: 'onresize',
		value: function onresize(handle) {
			$(window).resize(handle);
		}
	}]);
	return Main;
}();
/*
處理滾動頁面選單
 */

function FB_ASSET() {
	var context = this;
	var PARAM_SCOPE = 'public_profile,email,user_friends';
	var albIds = [];
	var albNames = [];
	var albCovers = [];
	var FB_STATE = 'init';
	var FB_ID = '0';
	var FB_NAME = 'DEFAULT';
	var scr = void 0;
	var scr2 = void 0;
	var loginCb = void 0;

	(function (d, s, id) {
		// const js = d.createElement(s); js.id = id;
		// const fjs = d.getElementsByTagName(s)[0];
		// if (d.getElementById(id)) { return; }
		// js.src = '//connect.facebook.net/zh_TW/sdk.js';
		// fjs.parentNode.insertBefore(js, fjs);
		var js,
		    fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {
			return;
		}
		js = d.createElement(s);js.id = id;
		js.src = "https://connect.facebook.net/zh_TW/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	})(document, 'script', 'facebook-jssdk');

	function getFBInfo(cb) {
		FB.api('/me', function (response) {
			FB_ID = response.id;
			FB_NAME = response.name;
			GLOBAL.fbid = FB_ID;
			GLOBAL.fbname = FB_NAME;
			if (cb) cb();
		});
	}
	function statusChangeCallback2(cb, response) {
		if (response.status === 'connected') {
			getFBInfo(cb);
			FB_STATE = 'in';
		} else {
			// _jconsole('non connected..........');
		}
	}

	function statusChangeCallback(cb, response) {
		$('.loading').hide();
		if (response.status === 'connected') {
			if (FB_STATE !== 'in') {
				getFBInfo(cb);
			} else {
				getFBInfo(cb);
			}
			FB_STATE = 'in';
		} else {
			//updateImg($('#cfa_index img'), 'img/btn_fb.png');
			FB_STATE = 'out';
		}
	}
	function checkLoginState2(cb) {
		FB.getLoginStatus(function (response) {
			statusChangeCallback2(cb, response);
		});
	}
	function checkLoginState(cb) {
		FB.getLoginStatus(function (response) {
			statusChangeCallback(cb, response);
		});
	}
	function fbLogin(cb) {
		var isSafari = navigator.userAgent.indexOf('Safari') > -1;
		var isChrome = navigator.userAgent.indexOf('Chrome') > -1;
		var isLine = window.navigator.userAgent.toLowerCase().indexOf('line');

		if (isLine < 0) {
			FB.login(function (response) {
				checkLoginState(cb);
			}, { scope: PARAM_SCOPE });
		} else {
			//alert(document.location.href)
			var redUrl = GLOBAL.host + 'm/share.html'; //+GLOBAL.uid;		
			var state = '{uid=' + GLOBAL.uid + '}'; //'{uid='+GLOBAL.uid+'}'
			location.href = 'https://www.facebook.com/v3.0/dialog/oauth?client_id=' + GLOBAL.fbAppId + '&redirect_uri=' + redUrl + '&state=' + state;
		}
	}
	function uiPost(title, msg, picurl, url) {
		var hash = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : null;
		var cb = arguments[5];

		var isSafari = navigator.userAgent.indexOf('Safari') > -1;
		var isChrome = navigator.userAgent.indexOf('Chrome') > -1;
		var isLine = window.navigator.userAgent.toLowerCase().indexOf('line');

		if (isLine < 0) {
			FB.ui({
				method: 'feed',
				caption: title,
				// description: msg,
				//hashtag:hash,
				link: url
				/*picture: picurl,*/
				// privacy:{'value':'EVERYONE'},
			}, function (response) {
				if (cb) cb();
				if (response && response.post_id) {
					GLOBAL.isSHARE = 1;
				} else {
					GLOBAL.isSHARE = 0;
				}
			});
		} else {

			location.href = "https://www.facebook.com/dialog/feed?app_id=" + GLOBAL.fbAppId + "&display=popup&amp;caption=" + title + "&link=" + url + "&redirect_uri=" + GLOBAL.host;
		}
	}
	function createAlbsNodes() {}

	function createPhotosFromAlbum(imgurl) {
		// var arr = $('.cover_detail')
		// var len = $(arr).length;
	}

	function albumClk(ind) {}
	var nextCount = 0;
	var MAX_PAGING = 2;
	function getPhotos(albId, next) {
		var photosStatus = void 0;
		if (!next) {
			nextCount = 0;
			photosStatus = 'load';
			FB.api('/' + albId + '/photos?pretty=0&limit=50', function (response) {
				var obj = response.data;
				var _iteratorNormalCompletion = true;
				var _didIteratorError = false;
				var _iteratorError = undefined;

				try {
					for (var _iterator = obj[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
						var index = _step.value;

						var photo = obj[index];
						var imgs = photo.images;
						var len = imgs.length;
						var imgb = imgs[len - 1];
						var imgUrl = imgb.source;
						createPhotosFromAlbum(imgUrl);
					}
				} catch (err) {
					_didIteratorError = true;
					_iteratorError = err;
				} finally {
					try {
						if (!_iteratorNormalCompletion && _iterator.return) {
							_iterator.return();
						}
					} finally {
						if (_didIteratorError) {
							throw _iteratorError;
						}
					}
				}

				var pg = response.paging;
				if (!pg) {
					photosStatus = 'ready';
					if (!scr2) {
						scr2 = new ScrollerOBJ();
						scr2.set_obj($('.photos_alb'));
						scr2.init();
					}
					return;
				}
				var cur = pg.cursors;
				if (!cur) {
					photosStatus = 'ready';
					if (!scr2) {
						scr2 = new ScrollerOBJ();
						scr2.set_obj($('.photos_alb'));
						scr2.init();
					}
					return;
				}
				// console.log("next" + next);
				if (cur.after) {
					getPhotos(albId, cur.after);
				}
			});
		} else {
			nextCount++;
			FB.api('/' + albId + '/photos?pretty=0&after=' + next + '&limit=50', function (response) {
				var obj = response.data;
				var _iteratorNormalCompletion2 = true;
				var _didIteratorError2 = false;
				var _iteratorError2 = undefined;

				try {
					for (var _iterator2 = obj[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
						var index = _step2.value;

						var photo = obj[index];
						var imgs = photo.images;
						var imgb = imgs[0];
						var imgUrl = imgb.source;
						createPhotosFromAlbum(imgUrl);
					}
				} catch (err) {
					_didIteratorError2 = true;
					_iteratorError2 = err;
				} finally {
					try {
						if (!_iteratorNormalCompletion2 && _iterator2.return) {
							_iterator2.return();
						}
					} finally {
						if (_didIteratorError2) {
							throw _iteratorError2;
						}
					}
				}

				var pg = response.paging;
				if (!pg || nextCount > MAX_PAGING) {
					photosStatus = 'ready';
					if (!scr2) {
						scr2 = new ScrollerOBJ();
						scr2.set_obj($('.photos_alb'));
						scr2.init();
					}
					return;
				}
				var cur = pg.cursors;
				if (!cur) {
					photosStatus = 'ready';
					if (!scr2) {
						scr2 = new ScrollerOBJ();
						scr2.set_obj($('.photos_alb'));
						scr2.init();
					}
					return;
				}
				if (cur.after) {
					getPhotos(albId, cur.after);
				}
			});
		}
	}
	function getAlbums() {
		FB.api('/me/albums', function (response) {
			if (response) {
				var obj = response.data;
				var _iteratorNormalCompletion3 = true;
				var _didIteratorError3 = false;
				var _iteratorError3 = undefined;

				try {
					for (var _iterator3 = obj[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
						var index = _step3.value;

						var album = obj[index];
						albIds.push(album.id);
						albNames.push(album.name);
						if (album.cover_photo) {
							albCovers.push(album.cover_photo);
						} else {
							albCovers.push('0');
						}
					}
				} catch (err) {
					_didIteratorError3 = true;
					_iteratorError3 = err;
				} finally {
					try {
						if (!_iteratorNormalCompletion3 && _iterator3.return) {
							_iterator3.return();
						}
					} finally {
						if (_didIteratorError3) {
							throw _iteratorError3;
						}
					}
				}

				createAlbsNodes();
				scr = new ScrollerOBJ();
				scr.set_obj($('.album_list'));
				scr.init();
				getPhotos(albIds[0], false);
			} else {
				// 未取得權限	偵測後可通知
			}
		});
	}
	function coverPhoto(id) {
		FB.api('/' + id + '?fields=picture&type=small', function (responseIn) {
			// const ind = albCovers.indexOf(id);
			// const arrs = $('.cover');
		});
	}
	this.get_FBID = function () {
		return FB_ID;
	};
	this.get_FBNAME = function () {
		return FB_NAME;
	};
	this.get_state = function () {
		return FB_STATE;
	};
	this.get_ui_post = function (title, msg, purl, url) {
		var hash = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : null;
		var cb = arguments[5];

		uiPost(title, msg, purl, url, hash, cb);
	};
	this.get_login = function (cb) {
		fbLogin(cb);
	};
	this.get_checkLoginState = function (cb) {
		checkLoginState2(cb);
	};
	this.initialize = function (cb) {
		console.log('fb app start:' + GLOBAL.fbAppId + '.....');
		loginCb = cb;
	};
	window.fbAsyncInit = function () {
		FB.init({
			appId: GLOBAL.fbAppId, //'108536939812687',
			xfbml: true,
			version: 'v3.0'
		});
		FB.AppEvents.logPageView();
		context.get_checkLoginState(null);
	};
}

function STEP(SECTION, NEXT) {
	var ANIM = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;

	var _delay = 1000 / 5;
	var state = -1;
	var old_state = -1;

	function render_loop() {

		var sh = parseInt(getBrowserHeight());
		if (GLOBAL.top < $(SECTION).offset().top - sh * .9) {
			state = 0;
			if (state != old_state) {
				animat('dis');
			}
		} else if (GLOBAL.top >= $(SECTION).offset().top - sh * .5 && GLOBAL.top < $(NEXT).offset().top - sh * .5) {
			state = 1;
			if (state != old_state) {
				animat('act');
			}
		} else {
			state = 2;
			if (state != old_state) {
				animat('dis');
			}
		}
		old_state = state;
		setTimeout(render_loop, _delay);
	}
	this.getanimat = animat;
	function animat(typ) {
		//console.log(SECTION + ' animat typ' + typ)


		if (typ == "act") {
			ANIM(true, SECTION);
		} else {
			ANIM(false, SECTION);
		}
	}
	function reset() {
		ANIM(false, SECTION);
	}
	this.init = function () {
		reset();
		render_loop();
	};
	this.init();
}

function GIF(SELECT, NAME) {
	var interval;
	var count = 1;
	var tloop = 400; //msec
	function loop() {
		//console.log("GIF loop")
		if (count < 3) count++;else count = 1;
		updateImg(SELECT.find('.char'), "http://819c375429527e275f54-b1b6e7de992e67a5fcec75da074835f8.r32.cf6.rackcdn.com/img/dest/" + NAME + count + ".png");

		interval = setTimeout(loop, tloop);
	}

	function reset() {

		count = 1;
		updateImg(SELECT.find('.char'), "http://819c375429527e275f54-b1b6e7de992e67a5fcec75da074835f8.r32.cf6.rackcdn.com/img/dest/" + NAME + count + ".png");
	}

	this.play = function () {
		clearTimeout(interval);
		loop();
	};
	this.killgif = function () {
		reset();
		clearTimeout(interval);
	};
	this.init = function () {
		reset();
	};
	this.init();
}

function Particle() {

    var SEPARATION = 100,
        AMOUNTX = 50,
        AMOUNTY = 50;
    var container, stats;
    var camera, scene, renderer;
    var particles,
        particle,
        count = 0;
    var mouseX = 0,
        mouseY = 0;
    var windowHalfX = window.innerWidth / 2;
    var windowHalfY = window.innerHeight / 2;

    function init() {
        container = document.getElementById('canv_far');

        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 10000);
        camera.position.z = 1000;

        scene = new THREE.Scene();
        particles = new Array();
        var PI2 = Math.PI * 2;
        var material = new THREE.SpriteCanvasMaterial({
            color: 0xe19676,
            program: function program(context) {
                context.beginPath();
                context.arc(0, 0, 0.5, 0, PI2, true);
                context.fill();
            }
        });
        var i = 0;
        for (var ix = 0; ix < AMOUNTX; ix++) {
            for (var iy = 0; iy < AMOUNTY; iy++) {
                particle = particles[i++] = new THREE.Sprite(material);

                particle.position.x = ix * SEPARATION - AMOUNTX * SEPARATION / 2;
                particle.position.z = iy * SEPARATION - AMOUNTY * SEPARATION / 2;
                scene.add(particle);
            }
        }
        renderer = new THREE.CanvasRenderer();
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0xffffff, 1);
        container.appendChild(renderer.domElement);
        //stats = new Stats();
        //container.appendChild( stats.dom );
        // document.addEventListener('mousemove', onDocumentMouseMove, false);
        // document.addEventListener('touchstart', onDocumentTouchStart, false);
        // document.addEventListener('touchmove', onDocumentTouchMove, false);
        //
        window.addEventListener('resize', onWindowResize, false);
    }

    function onWindowResize() {
        windowHalfX = window.innerWidth / 2;
        windowHalfY = window.innerHeight / 2;
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
    //
    function onDocumentMouseMove(event) {
        mouseX = 0;
        mouseY = -100; //event.clientY - windowHalfY;
    }

    function onDocumentTouchStart(event) {
        if (event.touches.length === 1) {
            event.preventDefault();
            mouseX = event.touches[0].pageX - windowHalfX;
            mouseY = event.touches[0].pageY - windowHalfY;
        }
    }

    function onDocumentTouchMove(event) {
        if (event.touches.length === 1) {
            event.preventDefault();
            mouseX = event.touches[0].pageX - windowHalfX;
            mouseY = event.touches[0].pageY - windowHalfY;
        }
    }
    //
    function animate() {
        requestAnimationFrame(animate);
        render();
        //stats.update();
    }

    function render() {
        camera.position.x += (0 - camera.position.x) * .05;
        camera.position.y += (100 - camera.position.y) * .05;
        camera.lookAt(scene.position);
        var i = 0;
        for (var ix = 0; ix < AMOUNTX; ix++) {
            for (var iy = 0; iy < AMOUNTY; iy++) {
                particle = particles[i++];
                particle.position.y = -100 + Math.sin((ix + count) * 0.3) * 50 + Math.sin((iy + count) * 0.5) * 50;
                particle.scale.x = particle.scale.y = (Math.sin((ix + count) * 0.3) + 1) * 4 + (Math.sin((iy + count) * 0.5) + 1) * 4;
            }
        }
        renderer.render(scene, camera);
        count += 0.1;
    }
    init();
    animate();
}

function FullPagejs() {
    var events = void 0;
    var touchStartY = 0;
    var touchStartX = 0;
    var touchEndY = 0;
    var touchEndX = 0;
    var secys = [$('#kv'), $('#MayorAndCouncilor'), $('#seemore'), $('#bills'), $('#votes'), $('#wishingwell'), $('.footer')];
    function touchhandle(scrollDirection) {

        var targetUp = void 0,
            targetDown = void 0,
            targetElement = void 0;
        var lastScrollTop = $(window).scrollTop();
        var navh = $('nav').height() * 1.5;

        if (lastScrollTop >= secys[0].offset().top - navh && lastScrollTop < secys[1].offset().top - navh) {
            //console.log('SEC1..... ')
            targetUp = secys[0];
            targetDown = secys[1];
        } else if (lastScrollTop >= secys[1].offset().top - navh && lastScrollTop < secys[2].offset().top - navh) {
            //console.log('SEC2..... ')
            targetUp = secys[0];
            targetDown = secys[2];
        } else if (lastScrollTop >= secys[2].offset().top - navh && lastScrollTop < secys[3].offset().top - navh) {
            //console.log('SEC3..... ')
            targetUp = secys[1];
            targetDown = secys[3];
        } else if (lastScrollTop >= secys[3].offset().top - navh && lastScrollTop < secys[4].offset().top - navh) {
            //console.log('SEC4..... ')
            targetUp = secys[2];
            targetDown = secys[4];
        } else if (lastScrollTop >= secys[4].offset().top - navh && lastScrollTop < secys[5].offset().top - navh) {
            //console.log('SEC5..... ')
            targetUp = secys[3];
            targetDown = secys[5];
        } else if (lastScrollTop >= secys[5].offset().top - navh && lastScrollTop < secys[6].offset().top - navh) {
            //console.log('SEC6..... ')
            targetUp = secys[4];
            targetDown = secys[6];
        } else if (lastScrollTop >= secys[6].offset().top - navh) {
            //console.log('SEC7..... ')
            targetUp = secys[5];
            targetDown = secys[7];
        } else {
            //console.log('SEC ELSE..... ')
        }
        if (scrollDirection === 'down') {
            targetElement = targetDown;
        } else if (scrollDirection === 'up') {
            targetElement = targetUp;
        } // end else if

        scrolltoDom(targetElement);
    }

    function scrollhandle(scrollDirection) {
        var targetUp = void 0,
            targetDown = void 0,
            targetElement = void 0;
        var lastScrollTop = $(window).scrollTop();
        var navh = $('nav').height() * 1.5;

        if (lastScrollTop >= secys[0].offset().top - navh && lastScrollTop < secys[1].offset().top - navh) {
            targetUp = secys[0];
            targetDown = secys[1];
        } else if (lastScrollTop >= secys[1].offset().top - navh && lastScrollTop < secys[2].offset().top - navh) {
            //console.log('SEC2..... ')
            targetUp = secys[0];
            targetDown = secys[2];
        } else if (lastScrollTop >= secys[2].offset().top - navh && lastScrollTop < secys[3].offset().top - navh) {
            //console.log('SEC3..... ')
            targetUp = secys[1];
            targetDown = secys[3];
        } else if (lastScrollTop >= secys[3].offset().top - navh && lastScrollTop < secys[4].offset().top - navh) {
            //console.log('SEC4..... ')
            targetUp = secys[2];
            targetDown = secys[4];
        } else if (lastScrollTop >= secys[4].offset().top - navh && lastScrollTop < secys[5].offset().top - navh) {
            //console.log('SEC5..... ')
            targetUp = secys[3];
            targetDown = secys[5];
        } else if (lastScrollTop >= secys[5].offset().top - navh) {
            //console.log('SEC6..... ')
            targetUp = secys[4];
            targetDown = secys[6];
        } else {
            //console.log('SEC ELSE..... ')
        }
        if (scrollDirection === 'down') {
            targetElement = targetDown;
        } else if (scrollDirection === 'up') {
            targetElement = targetUp;
        } // end else if

        scrolltoDom(targetElement);
    }
    var prevTime = new Date().getTime();
    var scrollings = [];
    var isScrolling = false;
    function getAverage(elements, number) {
        var sum = 0;

        //taking `number` elements from the end to make the average, if there are not enought, 1
        var lastElements = elements.slice(Math.max(elements.length - number, 1));

        for (var i = 0; i < lastElements.length; i++) {
            sum = sum + lastElements[i];
        }

        return Math.ceil(sum / number);
    }
    function MouseWheelHandler(e) {
        var curTime = new Date().getTime();
        var scrollDirection = void 0;

        e = e || window.event;
        var value = (e.wheelDelta || -e.deltaY || -e.detail) / 2;
        var delta = Math.max(-1, Math.min(1, value));
        var horizontalDetection = typeof e.wheelDeltaX !== 'undefined' || typeof e.deltaX !== 'undefined';
        var isScrollingVertically = Math.abs(e.wheelDeltaX) < Math.abs(e.wheelDelta) || Math.abs(e.deltaX) < Math.abs(e.deltaY) || !horizontalDetection;

        if (scrollings.length > 149) {
            scrollings.shift();
        }
        scrollings.push(Math.abs(value));
        // get scroll direction:

        e.preventDefault();
        if (isScrolling) {
            return false;
        }

        var timeDiff = curTime - prevTime;
        prevTime = curTime;

        if (timeDiff > 200) {
            console.log('clean array');
            scrollings = [];
        }
        var averageEnd = getAverage(scrollings, 10);
        var averageMiddle = getAverage(scrollings, 70);
        var isAccelerating = averageEnd >= averageMiddle;
        if (isAccelerating && isScrollingVertically) {
            //scrolling down?
            if (delta < 0) {
                console.log('scroll down');
                scrollhandle('down');

                //scrolling up?
            } else {
                console.log('scroll up');
                scrollhandle('up');
            }
            isScrolling = true;
            // removeMouseWheelHandler();
            setTimeout(function () {
                isScrolling = false;
            }, 1500);
        } else {
            isScrolling = false;
        }
        return false;
    }
    function removeMouseWheelHandler() {
        if (document.addEventListener) {
            document.removeEventListener('mousewheel', MouseWheelHandler, false); //IE9, Chrome, Safari, Oper
            document.removeEventListener('wheel', MouseWheelHandler, false); //Firefox
            document.removeEventListener('MozMousePixelScroll', MouseWheelHandler, false); //old Firefox
        } else {
            document.detachEvent('onmousewheel', MouseWheelHandler); //IE 6/7/8
        }
    }
    function addMouseWheelHandler() {
        var prefix = '';
        var _addEventListener;

        if (window.addEventListener) {
            _addEventListener = "addEventListener";
        } else {
            _addEventListener = "attachEvent";
            prefix = 'on';
        }

        // detect available wheel event
        var support = 'onwheel' in document.createElement('div') ? 'wheel' : // Modern browsers support "wheel"
        document.onmousewheel !== undefined ? 'mousewheel' : // Webkit and IE support at least "mousewheel"
        'DOMMouseScroll'; // let's assume that remaining browsers are older Firefox


        if (support == 'DOMMouseScroll') {
            document[_addEventListener](prefix + 'MozMousePixelScroll', MouseWheelHandler, false);
        }

        //handle MozMousePixelScroll in older Firefox
        else {
                document[_addEventListener](prefix + support, MouseWheelHandler, false);
            }
    }
    function getEventsPage(e) {
        var events = [];

        events.y = typeof e.pageY !== 'undefined' && (e.pageY || e.pageX) ? e.pageY : e.touches[0].pageY;
        events.x = typeof e.pageX !== 'undefined' && (e.pageY || e.pageX) ? e.pageX : e.touches[0].pageX;

        //in touch devices with scrollBar:true, e.pageY is detected, but we have to deal with touch events. #1008
        if (typeof e.touches !== 'undefined') {
            events.y = e.touches[0].pageY;
            events.x = e.touches[0].pageX;
        }

        return events;
    }
    function touchMoveHandler(e) {

        var touchEvents = getEventsPage(e);

        touchEndY = touchEvents.y;
        touchEndX = touchEvents.x;
        if (Math.abs(touchStartY - touchEndY) > 10) {
            e.preventDefault();
            if (touchStartY > touchEndY) {
                touchhandle('down');
            } else if (touchEndY > touchStartY) {
                touchhandle('up');
            }
        }
    }
    function touchStartHandler(e) {
        var touchEvents = getEventsPage(e);
        touchStartY = touchEvents.y;
        touchStartX = touchEvents.x;
    }
    function addTouchHandler() {
        events = {
            touchmove: 'ontouchmove' in window ? 'touchmove' : MSPointer.move,
            touchstart: 'ontouchstart' in window ? 'touchstart' : MSPointer.down
        };
        document.removeEventListener(events.touchstart, touchStartHandler);
        document.removeEventListener(events.touchmove, touchMoveHandler, { passive: false });
        document.addEventListener(events.touchstart, touchStartHandler);
        document.addEventListener(events.touchmove, touchMoveHandler, { passive: false });
    }
    function init() {
        if (device.mobile() || device.tablet()) {
            secys = [$('#kv'), $('#findmayor'), $('#findcouncilor'), $('#seemore'), $('#bills'), $('#votes'), $('#wishingwell'), $('.footer')];
            addTouchHandler();
        } else {
            addMouseWheelHandler();
        }
    }
    init();
}

function scrolltoDom(dom) {
    var $body = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');
    var top = void 0;
    var navh = $('nav').height();
    top = dom.offset().top;
    var t = 700;
    //TweenMax.set(window, {scrollTo:{y:top}});
    $body.stop().animate({
        scrollTop: top - navh
    }, t);
}

//import _ from 'underscore';
//import answer from 'the-answer';
//import {test} from 'youtubeiframe-jojo'
//import * as PIXI from 'pixi.js';
//import TweenMax from "TweenMax";
//import CSSPlugin from "gsap/CSSPlugin";
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');
var cm;
var council;
var lu;

var INDEX = function (_Main) {
    inherits(INDEX, _Main);

    function INDEX() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'index';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, INDEX);

        var _this = possibleConstructorReturn(this, (INDEX.__proto__ || Object.getPrototypeOf(INDEX)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.bind = _this.bind.bind(_this);
        lu = new LocateUpdator();

        _this.watchScroll();
        _this.map = new MAP();

        new Particle();
        cm = new CountyMayo();
        council = new Councilor();

        new FullPagejs();
        _this.init();

        return _this;
    }

    createClass(INDEX, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(INDEX.prototype.__proto__ || Object.getPrototypeOf(INDEX.prototype), 'init', this).call(this);

            $(window).resize(onresize);
            function onresize() {
                var vh = Number(getBrowserHeight());
                var vw = Number(getBrowserWidth());
                var s = vh / 1080;
                TweenMax.set($('svg'), { scaleX: s, scaleY: s, transformOrigin: "40% 0%" });
                if (vw < 768) {
                    $(".step1").mCustomScrollbar('destroy');
                    $(".step1").mCustomScrollbar({
                        theme: "my-theme1",
                        axis: "y"
                    });
                } else {
                    $(".step1").mCustomScrollbar('destroy');
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
            var timer = 0;
            function anim(typ) {
                var sec = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : ".kv1";

                var dom = $(sec);

                if (typ) {
                    if (sec == '#kv') {
                        var d = timer > 0 ? 1 : 2;
                        TweenMax.fromTo($('#kv .title '), .7, { opacity: 0 }, { delay: d, opacity: 1 });
                        var count = 0;
                        $('#kv .sub > * ').each(function () {
                            TweenMax.fromTo($(this), 1, { opacity: 0, y: 20 }, { delay: d + .1 * count, y: 0, opacity: 1 });
                            count++;
                        });
                    } else if (sec == '#MayorAndCouncilor') {
                        var _d = 0;
                        var _count = 0;

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.fromTo($(this), .5, { x: 30, opacity: 0 }, { delay: _d + .1 * _count, x: 0, opacity: 1, ease: Back.easeOut });
                            _count++;
                        });

                        /**
                         * ICON ANIMATION
                         */
                        var icos = dom.find('.ico');
                        _count = 0;
                        _d = 1;
                        icos.each(function () {
                            var fromy = _count == 0 ? 500 : -500;
                            TweenMax.fromTo($(this), .7, { y: fromy }, { delay: _d, y: 0, opacity: 1, ease: Cubic.easeOut });
                            _count++;
                        });
                    } else if (sec == '#seemore') {
                        var _d2 = 0;
                        var _count2 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.fromTo($(this), .5, { x: 30, opacity: 0 }, { delay: _d2 + .1 * _count2, x: 0, opacity: 1, ease: Back.easeOut });
                            _count2++;
                        });
                        _d2 = 1;
                        var _icos = dom.find('.ico');
                        //TweenMax.killTweensOf( icos.find('.eyeball')) ;
                        TweenMax.fromTo(_icos, 1.5, { x: -50 }, { delay: 0, x: 0, ease: Back.easeInOut });
                        TweenMax.fromTo(_icos.find('.eyeball'), .7, { x: -50 }, { delay: 0, x: 50, yoyo: true, repeat: 1, repeatDelay: .7, ease: Sine.easeInOut, onComplete: function onComplete() {
                                TweenMax.to(_icos.find('.eyeball'), .7, { delay: .7, x: 0 });
                            } });
                    } else if (sec == '#bills') {
                        var _d3 = 0;
                        var _count3 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.fromTo($(this), .5, { x: 30, opacity: 0 }, { delay: _d3 + .1 * _count3, x: 0, opacity: 1, ease: Back.easeOut });
                            _count3++;
                        });
                        _d3 = 1;
                        var _icos2 = dom.find('.ico');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.fromTo(_icos2, 1.2, { x: 800 }, { delay: 0, y: 0, x: 0, ease: Sine.easeInOut });
                    } else if (sec == '#votes') {
                        var _d4 = 0;
                        var _count4 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.fromTo($(this), .5, { x: 30, opacity: 0 }, { delay: _d4 + .1 * _count4, x: 0, opacity: 1, ease: Back.easeOut });
                            _count4++;
                        });
                        _d4 = 1;
                        var hammer = dom.find('.hammer'),
                            dong = dom.find('.dong');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.fromTo(hammer, 1.2, { x: 100, y: -100, rotation: 30, transformOrigin: "100% 100%" }, { delay: 0, transformOrigin: "100% 100%", y: 0, x: 0, rotation: 0, ease: Back.easeInOut });
                        TweenMax.fromTo(dong, .1, { opacity: 0 }, { delay: .9, opacity: 1, ease: Sine.easeInOut });
                    } else if (sec == '#wishingwell') {
                        var _d5 = 0;
                        var _count5 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.fromTo($(this), .5, { x: 30, opacity: 0 }, { delay: _d5 + .1 * _count5, x: 0, opacity: 1, ease: Back.easeOut });
                            _count5++;
                        });
                        _d5 = 1;
                        var ico = dom.find('.ico');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.fromTo(ico, 1.5, { x: -500, y: 500 }, { delay: 0, y: 0, x: 0, rotation: 0, ease: Sine.easeInOut });
                    }

                    timer++;
                } else {

                    if (sec == '#kv') {
                        TweenMax.to($('#kv .title '), .7, { opacity: 0 });
                        $('#kv .sub > * ').each(function () {
                            TweenMax.to($(this), .7, { opacity: 0, y: 20 });
                        });
                    } else if (sec == '#MayorAndCouncilor') {
                        var _d6 = .5;
                        var _count6 = 0;
                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.to($(this), .7, { x: 30, opacity: 0 });
                            _count6++;
                        });
                        var _icos3 = dom.find('.ico');
                        _icos3.each(function () {
                            var fromy = _count6 == 0 ? 500 : -500;
                            TweenMax.to($(this), .7, { y: fromy });
                        });
                    } else if (sec == '#seemore') {
                        var _d7 = .5;
                        var _count7 = 0;
                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.to($(this), .7, { x: 30, opacity: 0 });
                            _count7++;
                        });
                        var _icos4 = dom.find('.ico');
                        TweenMax.to(_icos4, 1, { x: -50 });
                        //  let icos = dom.find('.ico');
                        //  icos.each(function(){
                        //     let fromy = (count ==0)?500 : -500

                        // })

                    } else if (sec == '#bills') {
                        var _d8 = 0;
                        var _count8 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.to($(this), .7, { x: 30, opacity: 0 });
                            _count8++;
                        });
                        _d8 = 1;
                        var _icos5 = dom.find('.ico');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.to(_icos5, 1.2, { x: 800 });
                    } else if (sec == '#votes') {
                        var _d9 = 0;
                        var _count9 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.to($(this), .5, { x: 30, opacity: 0 });
                            _count9++;
                        });
                        _d9 = 1;
                        var _hammer = dom.find('.hammer'),
                            _dong = dom.find('.dong');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.to(_hammer, 1, { x: 100, y: -100, rotation: 30, transformOrigin: "100% 100%" });
                        TweenMax.to(_dong, .5, { opacity: 0 }, { delay: 1.2, opacity: 1, ease: Sine.easeInOut });
                    } else if (sec == '#wishingwell') {
                        var _d10 = 0;
                        var _count10 = 0;
                        console.log('sec .... ' + sec);

                        dom.find('.tit , .sub ,.select-area ,.select-county ,.select-opt1').each(function () {
                            TweenMax.to($(this), .5, { x: 30, opacity: 0 });
                            _count10++;
                        });
                        _d10 = 1;
                        var _ico = dom.find('.ico');
                        //TweenMax.killTweensOf( icos.find('.eyeball'))    ;
                        TweenMax.to(_ico, 1, { x: -500, y: 500 });
                    }
                }
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            // TweenMax.fromTo($('#kv .title '), .7, { opacity: 0 }, { delay: 2, opacity: 1 })
            // let count = 0;
            // $('#kv .sub > * ').each(function() {
            //     TweenMax.fromTo($(this), 1, { opacity: 0, y: 20 }, { delay: 2 + .1 * count, y: 0, opacity: 1 })
            //     count++
            // })
            if (typeof global_location.county == 'undefined') {
                TweenMax.fromTo($('#kv .locator > .ico '), .8, { opacity: 0, scaleX: 1.1, scaleY: 1.1 }, { delay: 3, y: 0, opacity: 1, scaleX: 1, scaleY: 1 });
                TweenMax.fromTo($('#kv .locator  span '), .8, { opacity: 0 }, { delay: 3.2, y: 0, opacity: 1 });
            } else {
                $('#kv .locator ').hide();
                lu.updateLocation();
                $('#kv .locator-ed ').delay(3000).fadeIn();
            }
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            get(INDEX.prototype.__proto__ || Object.getPrototypeOf(INDEX.prototype), 'bind', this).call(this);
            var context = this;
            $('.btn-findCouncilmen,.btn-findMayor').hover(function () {
                TweenMax.to($(this).find('.ico'), .5, { y: -5, repeat: -1, yoyo: true });
            }, function () {
                TweenMax.killTweensOf($(this).find('.ico'));
                TweenMax.to($(this).find('.ico'), .2, { y: 0 });
            });
            $('.btn-findCouncilmen').click(function () {
                var href = $(this).attr('href');
                if (href == "#") route('findcouncilor');else {
                    location.href = href;
                }
            });
            $('.btn-findMayor').click(function () {
                var href = $(this).attr('href');
                if (href == "#") route('findmayor');else {
                    location.href = href;
                }
            });

            /*
             *update locator by 
             */

            $('.locator').click(function () {
                $('.locator').fadeOut(500);

                ///////update View.....
                function error(err) {

                    lu.updateLocation();
                }
                navigator.geolocation.getCurrentPosition(function (position) {
                    $.ajax({
                        url: global_geolookupApi,
                        type: 'GET',
                        data: {
                            zoom: 19,
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        },
                        success: function success(data) {
                            global_location = { county: data[0].values[1], area: data[0].values[2] };

                            lu.updateLocation();
                            //update highlight
                            //

                        },
                        error: function error() {
                            alert('抱歉，定位失敗，請手動選擇～');
                            lu.updateLocation();
                        }
                    });
                }, error, { enableHighAccuracy: true });
            });
            if (global_location.county != undefined) {
                $('.locator-ed').click(function () {
                    context.map.addMap();
                });
            } else {
                $('.btn-chooseLocation').click(function () {
                    context.map.addMap();
                });
            }
            $('.pop-map .btn-close').click(function () {
                context.map.removeMap();
            });
        }
    }]);
    return INDEX;
}(Main);

function LocateUpdator() {

    this.updateLocation = function () {
        __updateLocation();
    };
    function __updateLocation() {
        if (global_location.county != undefined) {
            $('.locator').hide();
            $('.locator-ed .desc p:first').html('您已標定的區域');
            $('.county_val').html(global_location.county);
            if (global_location.area != undefined) {
                $('.area_val').html(', ' + global_location.area);
            } else {
                $('.area_val').html('');
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
                district: global_location.area
            },
            success: function success(data) {
                //                {"county":"臺北市","constituency":1,"type":"councilor","district":"萬華區"}
                setCookies(data);
                updateMayorCouncilorURL(data);
            },
            error: function error() {
                console.log('error : cant get constituencies...');
                if (location.href.indexOf('localhost') >= 0) {
                    setCookies({ county: '臺北市', district: '萬華區', constituency: '1' });
                    updateMayorCouncilorURL({ county: '臺北市', district: '萬華區', constituency: '1' });
                }
            }
        });
    }

    function updateMayorCouncilorURL(d) {
        console.log('chg mayor councilor url....');
        $('#kv .btn-findMayor').attr('href', '' + prefixUrlMayor_global + d.county + '/');
        $('#kv .btn-findCouncilmen').attr('href', '' + prefixUrlCouncilor_global + d.county + '/' + d.constituency + '/');
        $('#bills a:first').attr('href', '' + prefixUrlMayorForBills_global + d.county + '/');
        $('#bills a:nth-child(2)').attr('href', '' + prefixUrlCouncilorForBills_global + d.county + '/');
    }

    function updateHighlights() {
        cm.findAreaBycounty(global_location.county);
        council.findAreaBycounty(global_location.county);
    }

    function setCookies(d) {
        console.log('saving coockies...');
        setCookie('county', d.county, 30);
        setCookie('district', d.district, 30);
        setCookie('constituency', d.constituency, 30);
    }

    function init() {

        console.log('locateUpdator init ....');
        //檢查cookie
        global_location.county = getCookie('county') != null ? getCookie('county') : undefined;
        global_location.area = getCookie('district') != null ? getCookie('district') : undefined;

        //global_location = getCookie('constituency');
        //__updateLocation();
    }
    init();
}

function Councilor() {
    var dom = $('.sec2 .findcouncilor');
    var area = void 0;

    function bind() {

        dom.find('.select-area a').click(function (e) {
            e.preventDefault();
            var vw = Number(getBrowserWidth());
            var area = $(this).data('id');

            if (vw < 768) {
                location.href = prefixUrlCouncilor_global + '#' + area;
                return;
            }

            if (area == "") {
                area = "六都";
            }
            var cityies = GLOBAL.geo[area].cities;

            updateViewUi(area);
            updateView(cityies, 'city', area);
            var ct = updateViewUiCounty(0);
        });
    }

    function bindcounty() {
        var context = this;
        dom.find('.select-county > a').off('click').click(function () {
            var id = $(this).data('id');
            var ct = updateViewUiCounty(id);
        });
    }

    this.findAreaBycounty = function (county) {
        var area = void 0;
        for (var i in GLOBAL.geo) {
            var cities = GLOBAL.geo[i].cities;
            console.log('iterate ...area:' + i);
            for (var j in cities) {
                var ct = GLOBAL.geo[i].cities[j].cne;
                if (county == ct) {
                    console.log('city match ...area:' + county);
                    area = i;
                    break;
                }
            }

            if (typeof area != 'undefined') break;
        }
        console.log('find ...area:' + area);
        if (area != undefined) {

            var cityies = GLOBAL.geo[area].cities;

            updateViewUi(area);
            updateView(cityies, area);
            updateViewUiCounty(county);
        } else {
            console.log('area undefined!...');
        }
    };

    // function findAreaBycounty(county) {
    //     let area;

    //     return area;

    // }

    function updateView(cityies, typ, area) {
        dom.find('.select-county').html('');
        for (var i in cityies) {
            dom.find('.select-county').append('\n             <a href="' + prefixUrlCouncilor_global + cityies[i].cne + '#' + area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              ');
        }
        bindcounty();
    }

    function updateViewUiCounty() {
        var county = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

        if (county == 0) {
            county = dom.find('.select-county a:first').data('id');
        }

        dom.find('.select-county a').each(function () {

            var id = $(this).data('id');

            if (id == county) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }
        });

        return county;
    }

    function updateViewUi(area) {

        dom.find('.select-area > a').each(function () {
            var id = $(this).data('id');
            if (id == area) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }
        });
    }

    function datafetch(area, year) {
        var context = this;
        getD(area, year);

        function getD() {
            var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
            var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

            if (year_global) year = year_global;
            $.get(jsonUrl_global, function (pResponse) {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');

                    if (area == "") {
                        area = "六都";
                    }
                    var cityies = GLOBAL.geo[area].cities;
                    updateViewUi(area);
                    updateView(cityies, 'city', area);

                    var ct = updateViewUiCounty('');
                    //updateViewCounty(ct);

                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');
        }

        function updateData(category) {

            GLOBAL.geo[category] = { cities: [] };
            //找出有山地原住民
            var items = GLOBAL.constituencies;

            var cts = $.grep(items, function (item) {
                if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
            });

            //console.log(cts)
            var norepeatcts = _.groupBy(cts, function (ct) {
                return ct.county;
            });

            for (var ct in norepeatcts) {
                console.log('norepeatcts ...' + ct);
                var eng = findEngCounty(ct);
                GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
            }
        }

        function findEngCounty(countyval) {
            var all = GLOBAL.allcities;
            var cts = $.grep(all, function (item) {

                return item.cne.indexOf(countyval) >= 0;
            });
            return cts[0].eng;
        }
    }

    function init() {
        datafetch('六都', 2018);
        bind();
    }
    init();
}

function CountyMayo() {
    var dom = $('.sec2 .findmayor');
    var area = void 0;

    function bind() {
        dom.find('.select-area > a').click(function (e) {
            e.preventDefault();
            var vw = getBrowserWidth();
            var area = $(this).data('id');

            if (vw < 768) {
                location.href = prefixUrlMayor_global + '#' + area;
                return;
            }
            // context.datafetch(id);
            if (area == "") {
                area = "六都";
            }
            var cityies = GLOBAL.geo[area].cities;

            updateViewUi(area);
            updateView(cityies, area);
            updateViewUiCounty(0);
        });
    }
    this.findAreaBycounty = function (county) {
        var area = void 0;
        for (var i in GLOBAL.geo) {
            var cities = GLOBAL.geo[i].cities;
            console.log('iterate ...area:' + i);
            for (var j in cities) {
                var ct = GLOBAL.geo[i].cities[j].cne;
                if (county == ct) {
                    console.log('city match ...area:' + county);
                    area = i;
                    break;
                }
            }

            if (typeof area != 'undefined') break;
        }
        console.log('find ...area:' + area);
        if (area != undefined) {

            var cityies = GLOBAL.geo[area].cities;

            updateViewUi(area);
            updateView(cityies, area);
            updateViewUiCounty(county);
        } else {
            console.log('area undefined!...');
        }
    };

    function updateViewUiCounty(val) {
        if (val == 0) {
            val = dom.find('.select-county a:first').data('id');
        }
        $('.select-county  a').each(function () {
            var id = $(this).data('id');
            if (id == val) {
                dom.find(this).addClass('act');
            } else {
                dom.find(this).removeClass('act');
            }
        });
    }

    function updateViewUi(area) {
        dom.find('.select-area > a').each(function () {
            var id = $(this).data('id');
            if (id == area) {
                $(this).addClass('act');
            } else {
                $(this).removeClass('act');
            }
        });
    }

    function updateView(cityies, area) {
        var context = this;
        dom.find('.select-county').html('');
        for (var i in cityies) {
            dom.find('.select-county').append('\n             <a href="' + prefixUrlMayor_global + cityies[i].cne + '/#' + area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              ');
        }
    }

    function datafetch(area) {
        var context = this;
        console.log('data fetching....');
        if (area == "") {
            area = "六都";
        }
        var cityies = GLOBAL.geo[area].cities;

        updateViewUi(area);
        updateView(cityies, area);
        updateViewUiCounty(0);
    }

    function init() {
        datafetch("六都");
        bind();
    }
    init();
}

function MAP() {
    var step = 0;
    var countys = ["臺南市", "高雄市", "南投縣", "臺中市", "苗栗縣", "彰化縣", "雲林縣", "宜蘭縣", "花蓮縣", "澎湖縣", "新北市", "嘉義縣", "嘉義市", "連江縣", "金門縣", "臺東縣", "屏東縣", "臺北市", "桃園市", "新竹縣", "基隆市", "新竹市"];

    var zip = [];
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
        $('.pop-map .step1').fadeOut(200);
        $('.pop-map .step2').delay(200).show();
        var count = 0;
        $('.pop-map .step2 .tit,.pop-map .step2  .sub ,.pop-map .step2  .select , .pop-map .step2  .select-county-blk > div').each(function () {
            TweenMax.fromTo($(this), .5, { opacity: 0, y: 20 }, { delay: .5 + .05 * count, opacity: 1, y: 0, ease: Back.easeOut });
            count++;
        });
    }

    function updateStep1() {
        step = 1;
        $('.pop-map .step2').hide();
        $('.pop-map .step1').show();
        var count = 0;
        $('.pop-map .step1 .tit,.pop-map .step1  .sub ,.pop-map .step1  .select , .pop-map .step1  .select-county-blk > div').each(function () {
            TweenMax.fromTo($(this), .5, { opacity: 0, y: 20 }, { delay: .5 + .05 * count, opacity: 1, y: 0, ease: Back.easeOut });
            count++;
        });
    }
    this.removeMap = function () {
        rmMap();
    };

    function rmMap() {
        $('.pop-map').fadeOut(300);
        step = 1;
    }
    this.addMap = function () {
        $('.pop-map').fadeIn(300);

        if (step == 1) {
            updateStep1();
        }
    };

    function rebindArea(county) {
        $('.pop-map .step2 .select-area-blk a').each(function () {
            $(this).off('click').click(function () {
                var area = $(this).data('area');
                global_location.county = county;
                global_location.area = area;
                lu.updateLocation();
                rmMap();
                //route('MayorAndCouncilor')
            });
        });
    }

    function bind() {
        $('svg').find('.btn-county').each(function () {
            $(this).click(function () {
                var d = $(this).data('county');
                updateStep2(d);
            });
        });

        $('.pop-map .step1 select').change(function () {
            updateStep2($(this).val());
        });

        $('.pop-map .step1 .select-county-blk > div >a').each(function () {
            $(this).click(function (e) {
                e.preventDefault();
                var d = $(this).data('county');
                updateStep2(d);
            });
        });
    }

    function updateColors(dom) {
        var count = 0;
        var rnd = Math.random() * 30;
        var rndint = Math.ceil(rnd);
        var colorclass = 'bg-light-group-color';
        dom.each(function () {
            var n = (count + rndint) % 30 + 1;
            $(this).addClass(colorclass + n);
            count++;
        });
    }

    function updateAreaView(county) {

        $('.pop-map .step2 .select-area-blk').html('');
        for (var i in zip[county]) {

            $('.pop-map .step2 .select-area-blk').append('<div class="col-xs-6 col-sm-3"><a class="info" href="#" data-area="' + i + '">\n                <p>' + i + '</p>\n                <p class="eng">' + zip[county][i] + '</p></a></div>');
        }
        updateColors($('.pop-map .step2 .select-area-blk > div > a'));
    }

    function updatetwmapAttr() {
        var count = 0;
        $('svg g#ch > g ').each(function () {
            if (count < countys.length) {

                $(this).attr('data-county', countys[count]);
                $(this).addClass('btn-county');
            }

            $(this).hover(function () {
                $('svg g#ch > g ').css("opacity", .4);
                $(this).css("opacity", 1);
            }, function () {
                $('svg g#ch > g ').css("opacity", 1);
            });
            count++;
        });

        //update  mobile county selector
        $('.pop-map .step1 .select-county-blk > div >a').each(function () {
            var c = $(this).data('county');

            for (var i in GLOBAL.geo) {
                for (var j in GLOBAL.geo[i].cities) {
                    if (GLOBAL.geo[i].cities[j].cne == c) {
                        $(this).find('.eng').html(GLOBAL.geo[i].cities[j].eng);
                    }
                }
            }
        });

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
    var $body = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');
    var speed = 100;
    var top = void 0;
    var navh = $('nav').height();
    top = $("#" + hash).offset().top;
    var t = 700;
    //TweenMax.set(window, {scrollTo:{y:top}});
    $body.stop().animate({
        scrollTop: top - navh
    }, t);
}

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$1 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var RESUME = function (_Main) {
    inherits(RESUME, _Main);

    function RESUME() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'resume';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, RESUME);

        var _this = possibleConstructorReturn(this, (RESUME.__proto__ || Object.getPrototypeOf(RESUME)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        _this.slickTool();
        _this.updateView();
        return _this;
    }

    createClass(RESUME, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(RESUME.prototype.__proto__ || Object.getPrototypeOf(RESUME.prototype), 'init', this).call(this);
        }
    }, {
        key: 'updateView',
        value: function updateView() {
            var typ = $('.wrapper-header').data('type');
            $('.nav-resume-all  a').each(function () {
                var atyp = $(this).data('type');
                if (atyp == typ) {
                    $(this).addClass('act');
                }
            });

            $('nav.navbar , nav.navbar .bg-cover').addClass('bg-' + typ);
        }
    }, {
        key: 'slickTool',
        value: function slickTool() {
            $('.nav-resume-all').on('init', function () {
                console.log('carousel3 has init....');
                $('.nav-resume-all .slick-prev').html('<i class="fa fa-arrow-right"></i>');
                $('.nav-resume-all .slick-next').html('<i class="fa fa-arrow-right"></i>');
            });
            $('.nav-resume-all').slick({

                dots: false,
                infinite: false,
                speed: 700,
                slidesToShow: 5,
                slidesToScroll: 1,
                responsive: [{
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 4,
                        infinite: false

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: false

                    }
                }]
            });
        }
    }, {
        key: 'anim',
        value: function anim() {}
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {}
    }]);
    return RESUME;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$2 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var COUNTY_MAYER_AREA = function (_Main) {
    inherits(COUNTY_MAYER_AREA, _Main);

    function COUNTY_MAYER_AREA() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'county-mayer-area';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, COUNTY_MAYER_AREA);

        var _this = possibleConstructorReturn(this, (COUNTY_MAYER_AREA.__proto__ || Object.getPrototypeOf(COUNTY_MAYER_AREA)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(COUNTY_MAYER_AREA, [{
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
    }, {
        key: 'init',
        value: function init() {
            var context = this;
            get(COUNTY_MAYER_AREA.prototype.__proto__ || Object.getPrototypeOf(COUNTY_MAYER_AREA.prototype), 'init', this).call(this);
        }
    }, {
        key: 'datafetch',
        value: function datafetch(area) {
            var context = this;
            console.log('data fetching....');
            if (area == "") {
                area = "六都";
            }
            var cityies = GLOBAL.geo[area].cities;

            context.updateViewUi(area);
            context.updateView(cityies);
        }
    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.area-selector select').val(area);

            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateView',
        value: function updateView(cityies) {

            var context = this;

            $('.select-county-blk').html('');
            for (var i in cityies) {
                $('.select-county-blk').append('\n                <div class="col-xs-6 col-sm-3"><a class="info" href="/candidates/mayors/' + cityies[i].cne + '/#' + GLOBAL.area + '">\n              <p>' + cityies[i].cne + '</p>\n              <p class="eng">' + cityies[i].eng + '</p></a></div>\n              ');
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)
            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            $('.area-selector select').change(function () {
                var area = $(this).val();

                $('.select-area > a').each(function () {
                    var id = $(this).data('id');
                    if (id == area) $(this).trigger('click');
                });

                // location.href = `./#${id}`
                // context.datafetch(id);
            });
            $('.select-area > a').click(function () {
                var id = $(this).data('id');
                context.datafetch(id);
            });
        }
    }]);
    return COUNTY_MAYER_AREA;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$3 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var COUNTY_MAYER = function (_Main) {
    inherits(COUNTY_MAYER, _Main);

    function COUNTY_MAYER() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'county-mayer';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, COUNTY_MAYER);

        var _this = possibleConstructorReturn(this, (COUNTY_MAYER.__proto__ || Object.getPrototypeOf(COUNTY_MAYER)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);
        _this.anim();
        return _this;
    }

    createClass(COUNTY_MAYER, [{
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
                GLOBAL.area = hash;
            }
            return decodeURIComponent(hash);
        }
    }, {
        key: 'init',
        value: function init() {
            var context = this;
            get(COUNTY_MAYER.prototype.__proto__ || Object.getPrototypeOf(COUNTY_MAYER.prototype), 'init', this).call(this);
        }
    }, {
        key: 'datafetch',
        value: function datafetch(area) {
            var context = this;
            console.log('data fetching....' + area);
            if (area == "" || !checkArea(area)) {
                area = findAreaBycounty(county_global);
            }
            var cityies = GLOBAL.geo[area].cities;

            context.updateViewUi(area);
            context.updateView(cityies);
            context.updateViewUiCounty(county_global);

            function findAreaBycounty(county) {
                var area = void 0;
                for (var i in GLOBAL.geo) {
                    var cities = GLOBAL.geo[i].cities;
                    console.log('iterate ...area:' + i);
                    for (var j in cities) {
                        var ct = GLOBAL.geo[i].cities[j].cne;
                        if (county == ct) {
                            console.log('city match ...area:' + county);
                            area = i;
                            break;
                        }
                    }

                    if (typeof area != 'undefined') break;
                }
                return area;
            }

            function checkArea(a) {
                var areas = ['六都', '北部', '中部', '南部', '東部', '離島', '原住民'];

                for (var i in areas) {
                    if (a.indexOf(areas[i]) >= 0) {
                        return true;
                    }
                }
                return false;
            }
        }
    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {
            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateViewUiCounty',
        value: function updateViewUiCounty(val) {
            var tmp = val;
            if (val == 0) {
                val = $('.select-county a:first').data('id');
            }
            $('.select-county  a').each(function () {
                var id = $(this).data('id');
                if (id == val) {
                    if (tmp != 0) $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
        }
    }, {
        key: 'updateView',
        value: function updateView(cityies) {
            var context = this;

            $('.select-county').html('');
            for (var i in cityies) {
                $('.select-county').append('\n             <a href="' + prefixUrl_global + cityies[i].cne + '/#' + GLOBAL.area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              ');
            }
        }
    }, {
        key: 'anim',
        value: function anim() {
            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });

            context.detailbind();
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'detailbind',
        value: function detailbind() {
            var collapsestates = {};
            $('.content-item').each(function () {
                var id = $(this).data('id');
                $(this).find('.content-detail ').css('height', 0);
                collapsestates[id] = 0;
                $(this).find('.btn-detail').click(function () {
                    var dom = $(this).parent().parent().parent();
                    var ID = dom.data('id');
                    var detail = dom.find('.content-detail');

                    if (collapsestates[id] == 0) {
                        autoHeightAnimate(detail, 500);
                        TweenMax.to($(this).find('i'), .3, { rotation: 180 });
                        collapsestates[id] = 1;
                    } else {
                        detail.animate({ height: '0' }, 500);
                        TweenMax.to($(this).find('i'), .3, { rotation: 0 });
                        collapsestates[id] = 0;
                    }
                });
            });
            function autoHeightAnimate(element, time) {
                var curHeight = element.height(),
                    // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
                element.height(curHeight); // Reset to Default Height
                element.stop().animate({ height: autoHeight }, time); // Animate to Auto Height
            }
        }
    }, {
        key: 'bind',
        value: function bind() {
            console.log('binding....');
            var context = this;
            // $('.select-area > a').click(function(){
            //     let area = $(this).data('id');

            //     // context.datafetch(id);
            //     // if (area == "") {
            //     //     area = "六都"
            //     // }
            //     // let cityies = GLOBAL.geo[area].cities;

            //     // context.updateViewUi(area)
            //     // context.updateView(cityies)
            //     // context.updateViewUiCounty(0)
            // })
        }
    }]);
    return COUNTY_MAYER;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$4 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var COUNCILMEN_AREA = function (_Main) {
    inherits(COUNCILMEN_AREA, _Main);

    function COUNCILMEN_AREA() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'county-mayer-area';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, COUNCILMEN_AREA);

        var _this = possibleConstructorReturn(this, (COUNCILMEN_AREA.__proto__ || Object.getPrototypeOf(COUNCILMEN_AREA)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(COUNCILMEN_AREA, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(COUNCILMEN_AREA.prototype.__proto__ || Object.getPrototypeOf(COUNCILMEN_AREA.prototype), 'init', this).call(this);
        }
    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
    }, {
        key: 'datafetch',
        value: function datafetch() {
            var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
            var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

            var context = this;
            if (year_global) year = year_global;
            $.get(jsonUrl_global, function (pResponse) {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');
                    if (area == "") {
                        area = "六都";
                    }
                    var cityies = GLOBAL.geo[area].cities;
                    context.updateViewUi(area);
                    context.updateView(cityies, 'city');
                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');

            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {
            $('.area-selector select').val(area);
            $('.select-area > a').each(function () {

                var id = $(this).data('id');

                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
        }

        /**
         * 更新區域方塊們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {

            var context = this;

            $('.select-county-blk').html('');

            var hash = context.chkIgContainsHash();

            if (typ == 'city') {
                for (var i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3"><a class="info" href="/candidates/councilors/' + cityies[i].cne + '/#' + hash + '">\n                  <p>' + cityies[i].cne + '</p>\n                  <p class="eng">' + cityies[i].eng + '</p></a>\n                  </div>\n                  ');
                }
            } else {
                for (var _i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3">\n                  <a class="info councilmen-area" href="/candidates/councilors/' + cityies[_i].cne + '/#' + hash + '">\n                  <p></p>\n                  <p class="eng">01</p>\n                  <div class="area-info">\u6843\u6E90\u5340\u3001\u90A3\u746A\u590F\u5340\u3001\u7532\n                    \u4ED9\u5340\u3001\u516D\u9F9C\u5340\u3001\u6749\u6797\u5340\n                    \u3001\u5167\u9580\u5340\u3001\u65D7\u5C71\u5340\u3001\u7F8E\n                    \u6FC3\u5340\u3001\u8302\u6797\u5340 </div>\n                  </a>\n                  \n                  </div>\n                  ');
                }
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)
            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            $('.area-selector select').change(function () {
                var area = $(this).val();

                $('.select-area > a').each(function () {
                    var id = $(this).data('id');
                    if (id == area) $(this).trigger('click');
                });
            });
            $('.select-area > a').click(function () {
                var id = $(this).data('id');
                context.datafetch(id);
            });
        }
    }]);
    return COUNCILMEN_AREA;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$5 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var COUNCILMEN_COUNTY = function (_Main) {
    inherits(COUNCILMEN_COUNTY, _Main);

    function COUNCILMEN_COUNTY() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'councilmen county';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, COUNCILMEN_COUNTY);

        var _this = possibleConstructorReturn(this, (COUNCILMEN_COUNTY.__proto__ || Object.getPrototypeOf(COUNCILMEN_COUNTY)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(COUNCILMEN_COUNTY, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(COUNCILMEN_COUNTY.prototype.__proto__ || Object.getPrototypeOf(COUNCILMEN_COUNTY.prototype), 'init', this).call(this);
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

    }, {
        key: 'datafetch',
        value: function datafetch(area, year) {
            var context = this;
            getD(area, year);
            function getD() {
                var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
                var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

                if (year_global) year = year_global;
                $.get(jsonUrl_global, function (pResponse) {
                    if (pResponse) {
                        GLOBAL.constituencies = pResponse;
                        updateData('高山原住民');
                        updateData('平地原住民');

                        if (area == "") {
                            //area="六都"
                            area = findAreaBycounty(county_global);
                        }
                        var cityies = GLOBAL.geo[area].cities;
                        context.updateViewUi(area);
                        context.updateView(cityies, 'city');

                        var ct = context.updateViewUiCounty(county_global);
                        $('.select-county-blk').html('');
                        context.updateViewCounty(ct);
                    } else {
                        alert('出現錯誤，請稍後再試！');
                    }
                }, 'json');
            }
            function findAreaBycounty(county) {
                var area = void 0;
                for (var i in GLOBAL.geo) {
                    var cities = GLOBAL.geo[i].cities;
                    console.log('iterate ...area:' + i);
                    for (var j in cities) {
                        var ct = GLOBAL.geo[i].cities[j].cne;
                        if (county == ct) {
                            console.log('city match ...area:' + county);
                            area = i;
                            break;
                        }
                    }

                    if (typeof area != 'undefined') break;
                }
                return area;
            }
            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
        // datafetchCounty(){

        // }

    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateViewUiCounty',
        value: function updateViewUiCounty() {
            var county = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            var tmp = county;
            if (county == 0) {
                county = $('.select-county a:first').data('id');
            }
            GLOBAL.county = county;
            $('.select-county a').each(function () {

                var id = $(this).data('id');

                if (id == county) {
                    //if(tmp !=0)
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });

            return county;
        }

        /**
         * 更新區域option們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {
            var context = this;

            if ($('.select-county  a').length >= 10) {
                $('.select-county').slick('unslick');
            }

            $('.select-county').html('');

            for (var i in cityies) {
                $('.select-county').append('\n             <a href="#' + GLOBAL.area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              ');
            }
            context.bindcounty();
            if ($('.select-county  a').length >= 10) {

                $('.select-county').slick({
                    dots: false,
                    infinite: false,
                    speed: 700,
                    slidesToShow: 10,
                    slidesToScroll: 1,
                    responsive: [{
                        breakpoint: 1000,
                        settings: {
                            slidesToShow: 6,
                            slidesToScroll: 1,
                            infinite: false

                        }
                    }, {
                        breakpoint: 567,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3,
                            infinite: false

                        }
                    }]
                });
            }
        }
        /**
         * RENDER 每區的方塊資訊
         * @param  {[type]} cityies [description]
         * @return {[type]}         [description]
         */

    }, {
        key: 'updateViewCounty',
        value: function updateViewCounty(county) {

            var context = this;
            var cityies = void 0;
            if (GLOBAL.area.indexOf('原住民') < 0) {
                var items = GLOBAL.constituencies;
                cityies = $.grep(items, function (item) {
                    return item.county.indexOf(county) >= 0;
                });
            } else {
                var _items = GLOBAL.constituencies;
                var area = GLOBAL.area == "高山原住民" ? '山地原住民' : GLOBAL.area;
                cityies = $.grep(_items, function (item) {
                    return item.county.indexOf(county) >= 0 && item.district.indexOf(area) >= 0;
                });
            }

            //let hash = context.chkIgContainsHash();
            for (var i in cityies) {

                $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3">\n                  <a class="info councilmen-area" href="/candidates/councilors/' + cityies[i].county + '/' + cityies[i].constituency + '/#' + GLOBAL.area + '">\n                  <p></p>\n                  <p class="eng">' + cityies[i].constituency + '</p>\n                  <div class="area-info">\n                    <div class="areas">\n                    ' + cityies[i].district + '\n                    </div>\n                  </div>\n                  </a>\n                  \n                  </div>\n                  ');
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)


            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;

                var boxh = $(this).find('.area-info').height();
                var contenth = $(this).find('.area-info .areas').height();
                console.log("boxh..." + boxh);
                console.log("contenth..." + contenth);
                if (boxh < contenth) {
                    var t = 8; //(boxh + contenth) / 25
                    TweenMax.fromTo($(this).find('.area-info .areas'), t, { y: boxh }, { delay: 0 * count, y: -contenth, repeat: -1, ease: Linear.easeNone });
                }
            });

            //檢查高度
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bindcounty',
        value: function bindcounty() {
            var context = this;
            $('.select-county > a').off('click').click(function () {

                var id = $(this).data('id');

                console.log("id..." + id);

                var ct = context.updateViewUiCounty(id);
                $('.select-county-blk').html('');
                context.updateViewCounty(ct);
            });
        }
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            $('.select-area a').click(function () {
                var area = $(this).data('id');
                if (area == "") {
                    area = "六都";
                }
                var cityies = GLOBAL.geo[area].cities;

                context.updateViewUi(area);
                context.updateView(cityies, 'city');
                var ct = context.updateViewUiCounty(0);
                $('.select-county-blk').html('');
                // for( let ct of cityies){
                //     console.log(ct);
                context.updateViewCounty(ct);
                // }
            });
        }
    }]);
    return COUNCILMEN_COUNTY;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$6 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var COUNCILMEN = function (_Main) {
    inherits(COUNCILMEN, _Main);

    function COUNCILMEN() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'councilmen';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, COUNCILMEN);

        var _this = possibleConstructorReturn(this, (COUNCILMEN.__proto__ || Object.getPrototypeOf(COUNCILMEN)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        _this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(COUNCILMEN, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(COUNCILMEN.prototype.__proto__ || Object.getPrototypeOf(COUNCILMEN.prototype), 'init', this).call(this);
            new WatchMove();
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

    }, {
        key: 'datafetch',
        value: function datafetch(area, year) {
            var context = this;
            getD(area, year);
            function getD() {
                var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
                var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

                if (year_global) year = year_global;
                $.get(jsonUrl_global, function (pResponse) {
                    if (pResponse) {
                        GLOBAL.constituencies = pResponse;
                        updateData('高山原住民');
                        updateData('平地原住民');
                        console.log('area...' + area);
                        console.log('GLOBAL.county...' + GLOBAL.county);
                        if (area == "" || !checkArea(area)) {
                            area = findAreaBycounty(county_global);
                        }
                        var cityies = GLOBAL.geo[area].cities;
                        context.updateViewUi(area);
                        context.updateView(cityies, 'city');

                        var ct = context.updateViewUiCounty(county_global);
                        context.updateViewCounty(ct);
                        context.updateViewUiConstituency(constituency_global);
                    } else {
                        alert('出現錯誤，請稍後再試！');
                    }
                }, 'json');
            }
            function checkArea(a) {
                var areas = ['六都', '北部', '中部', '南部', '東部', '離島', '原住民'];

                for (var i in areas) {
                    if (a.indexOf(areas[i]) >= 0) {
                        return true;
                    }
                }
                return false;
            }

            function findAreaBycounty(county) {
                var area = void 0;
                for (var i in GLOBAL.geo) {
                    var cities = GLOBAL.geo[i].cities;
                    console.log('iterate ...area:' + i);
                    for (var j in cities) {
                        var ct = GLOBAL.geo[i].cities[j].cne;
                        if (county == ct) {
                            console.log('city match ...area:' + county);
                            area = i;
                            break;
                        }
                    }

                    if (typeof area != 'undefined') break;
                }
                return area;
            }
            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
        // datafetchCounty(){

        // }

    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateViewUiCounty',
        value: function updateViewUiCounty() {
            var county = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            var tmp = county;
            if (county == 0) {
                county = $('.select-county a:first').data('id');
            }
            GLOBAL.county = county;
            $('.select-county a').each(function () {

                var id = $(this).data('id');

                if (id == county) {
                    if (tmp != 0) $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });

            return county;
        }
    }, {
        key: 'updateViewUiConstituency',
        value: function updateViewUiConstituency() {
            var constituency = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            var tmp = constituency;
            if (constituency == 0) {
                constituency = $('.select-constituency a:first').data('id');
            }
            GLOBAL.constituency = constituency;
            $('.select-constituency a').each(function () {
                var id = $(this).data('id');
                if (id == constituency) {
                    if (tmp != 0) $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            var context = this;
            context.anim();
        }

        /**
         * 更新區域option們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {
            var context = this;
            if ($('.select-county  a').length >= 10) {
                $('.select-county').slick('unslick');
            }
            $('.select-county').html('');
            for (var i in cityies) {
                $('.select-county').append('\n             <a href="' + prefixUrl_global + cityies[i].cne + '/#' + GLOBAL.area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              \n              ');
            }
            context.bindcounty();
            enableSlick($('.select-county'));
        }
        /**
         * RENDER 每區的方塊資訊
         * @param  {[type]} cityies [description]
         * @return {[type]}         [description]
         */

    }, {
        key: 'updateViewCounty',
        value: function updateViewCounty(county) {

            var context = this;

            var cityies = void 0;
            if (GLOBAL.area.indexOf('原住民') < 0) {
                var items = GLOBAL.constituencies;
                cityies = $.grep(items, function (item) {
                    return item.county.indexOf(county) >= 0;
                });
            } else {
                var _items = GLOBAL.constituencies;
                var area = GLOBAL.area == "高山原住民" ? '山地原住民' : GLOBAL.area;
                cityies = $.grep(_items, function (item) {
                    return item.county.indexOf(county) >= 0 && item.district.indexOf(area) >= 0;
                });
            }

            if ($('.select-constituency  a').length >= 10) {
                $('.select-constituency').slick('unslick');
            }
            $('.select-constituency').html('');

            for (var i in cityies) {
                var consti = Number(cityies[i].constituency) < 10 ? "0" + cityies[i].constituency + "區" : cityies[i].constituency + "區",
                    district = cityies[i].district;
                $('.select-constituency').append('\n                <a href="' + prefixUrl_global + county + '/' + cityies[i].constituency + '/#' + GLOBAL.area + '" data-id="' + cityies[i].constituency + '" data-info="' + cityies[i].district + '">' + consti + '\n                </a>\n                  ');
            }

            enableSlick($('.select-constituency'));

            $('.select-constituency a').each(function () {

                $(this).off('hover').hover(function () {
                    var id = $(this).data('id');
                    var info = $(this).data('info');
                    console.log('hover....' + id);
                    $('.hover-info p').html('' + info);
                    $('.hover-info').show();
                }, function () {
                    $('.hover-info').hide();
                });
            });

            // context.anim()
        }
    }, {
        key: 'anim',
        value: function anim() {
            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });

            context.detailbind();
        }
    }, {
        key: 'detailbind',
        value: function detailbind() {
            var collapsestates = {};
            $('.content-item').each(function () {
                var id = $(this).data('id');
                $(this).find('.content-detail ').css('height', 0);
                collapsestates[id] = 0;
                $(this).find('.btn-detail').click(function () {
                    var dom = $(this).parent().parent().parent();
                    var ID = dom.data('id');
                    var detail = dom.find('.content-detail');

                    if (collapsestates[id] == 0) {
                        autoHeightAnimate(detail, 500);

                        TweenMax.to($(this).find('i'), .3, { rotation: 180 });
                        collapsestates[id] = 1;
                    } else {
                        detail.animate({ height: '0' }, 500);
                        TweenMax.to($(this).find('i'), .3, { rotation: 0 });
                        collapsestates[id] = 0;
                    }
                });
            });
            function autoHeightAnimate(element, time) {
                var curHeight = element.height(),
                    // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
                element.height(curHeight); // Reset to Default Height
                element.stop().animate({ height: autoHeight }, time); // Animate to Auto Height
            }
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bindcounty',
        value: function bindcounty() {
            var context = this;
            // $('.select-county > a').off('click').click(function(e){
            //     e.preventDefault();
            //     let id = $(this).data('id');
            //     console.log("id..."+id)
            //     let ct =  context.updateViewUiCounty(id)
            //     context.updateViewCounty(ct)
            //     context.updateViewUiConstituency(0);
            // })

        }
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            // $('.select-area a').off('click').click(function(){
            //     let area = $(this).data('id');
            //     if(area==""){area="六都"}
            //     let cityies = GLOBAL.geo[area].cities;
            //     context.updateViewUi(area);
            //     context.updateView(cityies , 'city');

            //     let ct = context.updateViewUiCounty(0);
            //     context.updateViewCounty(ct);
            //     context.updateViewUiConstituency(0);
            // })
        }
    }]);
    return COUNCILMEN;
}(Main);

function enableSlick(dom) {
    if (dom.find('a').length >= 10) dom.slick({
        dots: false,
        infinite: false,
        speed: 700,
        slidesToShow: 10,
        slidesToScroll: 1,
        responsive: [{
            breakpoint: 1000,
            settings: {
                slidesToShow: 6,
                slidesToScroll: 1,
                infinite: false

            }
        }, {
            breakpoint: 567,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: false

            }
        }]
    });
}

function WatchMove() {
    var data = {};
    var force = 0;

    function loop() {
        var bodyW = Number(getBrowserWidth());
        var vw = Number($('.head-j').width());
        var deltaX = GLOBAL.mousex - bodyW / 2;
        if (deltaX > 0) {
            $('.hover-area .tri').css('left', '75%');
            $('.hover-area').css('left', deltaX + vw / 2 - 90);
        } else {
            $('.hover-area .tri').css('left', '20px');
            $('.hover-area').css('left', deltaX + vw / 2);
        }

        requestAnimationFrame(loop);
    }
    function init() {
        $('body').mousemove(function (event) {
            var clientCoords = "( " + event.clientX + ", " + event.clientY + " )";
            GLOBAL.mousex = event.clientX;
        });
        loop();
    }
    init();
}

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$7 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var BILL_AREA = function (_Main) {
    inherits(BILL_AREA, _Main);

    function BILL_AREA() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'county-mayer-area';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, BILL_AREA);

        var _this = possibleConstructorReturn(this, (BILL_AREA.__proto__ || Object.getPrototypeOf(BILL_AREA)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(BILL_AREA, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(BILL_AREA.prototype.__proto__ || Object.getPrototypeOf(BILL_AREA.prototype), 'init', this).call(this);
        }
    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
    }, {
        key: 'datafetch',
        value: function datafetch() {
            var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
            var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

            var context = this;
            //if(year_global) year = year_global;
            $.get(jsonUrl_global, function (pResponse) {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');
                    updateData('不分區');
                    updateData('僑民');
                    if (area == "") {
                        area = "六都";
                    }
                    var cityies = GLOBAL.geo[area].cities;
                    context.updateViewUi(area);
                    context.updateView(cityies, 'city');
                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');

            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {
            $('.area-selector select').val(area);
            $('.select-area > a').each(function () {

                var id = $(this).data('id');

                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
        }

        /**
         * 更新區域方塊們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {

            var context = this;

            $('.select-county-blk').html('');

            var hash = context.chkIgContainsHash();

            if (typ == 'city') {
                for (var i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3"><a class="info" href="' + prefixUrl_global + cityies[i].cne + '/#' + hash + '">\n                  <p>' + cityies[i].cne + '</p>\n                  <p class="eng">' + cityies[i].eng + '</p></a>\n                  </div>\n                  ');
                }
            } else {
                for (var _i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3">\n                  <a class="info councilmen-area" href="' + prefixUrl_global + cityies[_i].cne + '/#' + hash + '">\n                  <p></p>\n                  <p class="eng">01</p>\n                  <div class="area-info">\u6843\u6E90\u5340\u3001\u90A3\u746A\u590F\u5340\u3001\u7532\n                    \u4ED9\u5340\u3001\u516D\u9F9C\u5340\u3001\u6749\u6797\u5340\n                    \u3001\u5167\u9580\u5340\u3001\u65D7\u5C71\u5340\u3001\u7F8E\n                    \u6FC3\u5340\u3001\u8302\u6797\u5340 </div>\n                  </a>\n                  \n                  </div>\n                  ');
                }
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)
            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            $('.area-selector select').change(function () {
                var area = $(this).val();

                $('.select-area > a').each(function () {
                    var id = $(this).data('id');
                    if (id == area) $(this).trigger('click');
                });
            });
            $('.select-area > a').click(function () {
                var id = $(this).data('id');
                context.datafetch(id);
            });
        }
    }]);
    return BILL_AREA;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$8 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var BILL_COUNTY = function (_Main) {
    inherits(BILL_COUNTY, _Main);

    function BILL_COUNTY() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'councilmen county';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, BILL_COUNTY);

        var _this = possibleConstructorReturn(this, (BILL_COUNTY.__proto__ || Object.getPrototypeOf(BILL_COUNTY)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(BILL_COUNTY, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(BILL_COUNTY.prototype.__proto__ || Object.getPrototypeOf(BILL_COUNTY.prototype), 'init', this).call(this);
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

    }, {
        key: 'datafetch',
        value: function datafetch(area, year) {
            var context = this;
            getD(area, year);
            function getD() {
                var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
                var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

                //if(year_global) year = year_global;
                $.get(jsonUrl_global, function (pResponse) {
                    if (pResponse) {
                        GLOBAL.constituencies = pResponse;
                        updateData('高山原住民');
                        updateData('平地原住民');
                        console.log('area...' + area);
                        console.log('GLOBAL.county...' + GLOBAL.county);
                        if (area == "") {
                            area = findAreaBycounty(county_global);
                        }
                        var cityies = GLOBAL.geo[area].cities;
                        context.updateViewUi(area);
                        context.updateView(cityies, 'city');

                        var ct = context.updateViewUiCounty(county_global);
                        context.updateViewCounty(ct);
                    } else {
                        alert('出現錯誤，請稍後再試！');
                    }
                }, 'json');
            }
            function findAreaBycounty(county) {
                var area = void 0;
                for (var i in GLOBAL.geo) {
                    var cities = GLOBAL.geo[i].cities;
                    console.log('iterate ...area:' + i);
                    for (var j in cities) {
                        var ct = GLOBAL.geo[i].cities[j].cne;
                        if (county == ct) {
                            console.log('city match ...area:' + county);
                            area = i;
                            break;
                        }
                    }

                    if (typeof area != 'undefined') break;
                }
                return area;
            }
            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
        // datafetchCounty(){

        // }

    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateViewUiCounty',
        value: function updateViewUiCounty() {
            var county = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            var tmp = county;
            if (county == 0) {
                county = $('.select-county a:first').data('id');
            }
            GLOBAL.county = county;
            $('.select-county a').each(function () {

                var id = $(this).data('id');

                if (id == county) {
                    if (tmp != 0) $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });

            return county;
        }

        /**
         * 更新區域option們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {
            var context = this;

            if ($('.select-county  a').length >= 10) {
                $('.select-county').slick('unslick');
            }
            $('.select-county').html('');

            for (var i in cityies) {
                $('.select-county').append('\n             <a href="' + prefixUrl_global + '#' + GLOBAL.area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              ');
            }
            context.bindcounty();
            if ($('.select-county  a').length >= 10) $('.select-county').slick({
                dots: false,
                infinite: false,
                speed: 700,
                slidesToShow: 10,
                slidesToScroll: 1,
                responsive: [{
                    breakpoint: 1000,
                    settings: {
                        slidesToShow: 6,
                        slidesToScroll: 1,
                        infinite: false

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: false

                    }
                }]
            });
        }
        /**
         * RENDER 每區的方塊資訊
         * @param  {[type]} cityies [description]
         * @return {[type]}         [description]
         */

    }, {
        key: 'updateViewCounty',
        value: function updateViewCounty(county) {
            return;
            var context = this;
            var cityies = void 0;
            if (GLOBAL.area.indexOf('原住民') < 0) {
                var items = GLOBAL.constituencies;
                cityies = $.grep(items, function (item) {
                    return item.county.indexOf(county) >= 0;
                });
            } else {
                var _items = GLOBAL.constituencies;
                var area = GLOBAL.area == "高山原住民" ? '山地原住民' : GLOBAL.area;
                cityies = $.grep(_items, function (item) {
                    return item.county.indexOf(county) >= 0 && item.district.indexOf(area) >= 0;
                });
            }
            $('.select-county-blk').html('');
            //let hash = context.chkIgContainsHash();
            for (var i in cityies) {

                $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3">\n                  <a class="info councilmen-area" href="' + prefixUrl_global + cityies[i].county + '/' + cityies[i].constituency + '/#' + GLOBAL.area + '">\n                  <p></p>\n                  <p class="eng">' + cityies[i].constituency + '</p>\n                  <div class="area-info">' + cityies[i].district + '</div>\n                  </a>\n                  \n                  </div>\n                  ');
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)
            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bindcounty',
        value: function bindcounty() {
            var context = this;
            $('.select-county > a').off('click').click(function () {

                var id = $(this).data('id');

                console.log("id..." + id);

                var ct = context.updateViewUiCounty(id);

                context.updateViewCounty(ct);
            });
        }
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            $('.select-area a').click(function () {
                var area = $(this).data('id');
                if (area == "") {
                    area = "六都";
                }
                var cityies = GLOBAL.geo[area].cities;

                context.updateViewUi(area);
                context.updateView(cityies, 'city');
                var ct = context.updateViewUiCounty(0);
                context.updateViewCounty(ct);
            });
        }
    }]);
    return BILL_COUNTY;
}(Main);

var ARROWS = function () {
    //name 属性
    //YTT_class.name  "YTT_class"
    function ARROWS(dom) {
        classCallCheck(this, ARROWS);

        console.log('Arrows class contrusct...');
        this._dom = dom;
        this._Total = this._dom.find('.pg').length;
        // console.log('total pages ....' + this._Total)
        this._curr = this._dom.find('.pg.act').data('id');

        if (typeof this._curr == 'undefined') {
            this._curr = 1;
        }

        this.NumPerPage = 10;

        this.chkPages = this.chkPages.bind(this);
        this.updateUIView = this.updateUIView.bind(this);
        this.updateView = this.updateView.bind(this);
        this.on = this.on.bind(this);
        this.init = this.init.bind(this);
        this.init();
    }

    createClass(ARROWS, [{
        key: 'init',
        value: function init() {
            this.chkPages();
            this.updateUIView();
            this.updateView();
            this.on();
        }
    }, {
        key: 'chkPages',
        value: function chkPages() {

            this.pgs = Math.ceil(this._curr / this.NumPerPage);
            this.maxPgs = Math.ceil(this._Total / this.NumPerPage);

            this.minpg = (this.pgs - 1) * this.NumPerPage;
            this.maxpg = this.pgs * this.NumPerPage;
        }
    }, {
        key: 'updateUIView',
        value: function updateUIView() {
            this._dom.find('.pg' + this._curr).addClass('act');
            this._dom.find('.btnNext,.btnPrev').show();

            if (this.pgs >= this.maxPgs || this.maxPgs == 0) {
                this._dom.find('.btnNext').hide();
            }
            if (this.pgs <= 1) {
                this._dom.find('.btnPrev').hide();
            }
        }
    }, {
        key: 'updateView',
        value: function updateView() {

            this.removePage(this.minpg, this.maxpg);
            this.addPage(this.minpg, this.maxpg);
        }
    }, {
        key: 'hidePage',
        value: function hidePage() {}
    }, {
        key: 'addPage',
        value: function addPage(min, max) {
            var count = 0;
            for (var i = 1; i <= this._Total; i++) {
                if (i > min && i <= max) {
                    this._dom.find('.pg' + i).css('opacity', 0).show();
                    TweenMax.fromTo(this._dom.find('.pg' + i), .2, { y: 5 }, { delay: .05 * count, y: 0, opacity: 1 });
                    count++;
                }
            }
        }
    }, {
        key: 'removePage',
        value: function removePage(min, max) {
            for (var i = 1; i <= this._Total; i++) {
                if (i <= min || i > max) this._dom.find('.pg' + i).hide();
            }
        }
    }, {
        key: 'on',
        value: function on() {
            var context = this;
            this._dom.find('.btnNext').click(function () {
                // console.log('next........')
                context._curr = context.pgs * context.NumPerPage + 1;

                trigger();
            });
            this._dom.find('.btnPrev').click(function () {

                context._curr = (context.pgs - 2) * context.NumPerPage + 1;
                // console.log('prev........'+context._curr)

                trigger();
            });

            function trigger() {
                context.chkPages();
                context.updateUIView();
                context.updateView();
            }
        }
        ///////////////////////////////
        //类的方法内部如果含有this，它默认指向类的实例。
        //但是，必须非常小心，一旦单独使用该方法，很可能报错。 //
        ///////////////////////////////
        /**
         * [_initplayer description]
         * 私有方法
         * 表示这是一个只限于内部使用的私有方法。
         * 但在类的外部，还是可以调用到这个方法。
         * (私有屬性)
         */
        /*
         */

        //https://aerotwist.com/blog/flip-your-animations/

    }]);
    return ARROWS;
}();

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$9 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var BILL = function (_Main) {
    inherits(BILL, _Main);

    function BILL() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'councilmen';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, BILL);

        var _this = possibleConstructorReturn(this, (BILL.__proto__ || Object.getPrototypeOf(BILL)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        _this.datafetch(hash);

        return _this;
    }

    createClass(BILL, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(BILL.prototype.__proto__ || Object.getPrototypeOf(BILL.prototype), 'init', this).call(this);
            new WatchMove$1();
            new ARROWS($('.pagemanager'));
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

    }, {
        key: 'datafetch',
        value: function datafetch(area, year) {
            var context = this;
            getD(area, year);
            function getD() {
                var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
                var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;


                $.get(jsonUrl_global, function (pResponse) {
                    if (pResponse) {
                        GLOBAL.constituencies = pResponse;
                        updateData('高山原住民');
                        updateData('平地原住民');
                        console.log('area...' + area);
                        console.log('GLOBAL.county...' + GLOBAL.county);
                        if (area == "") {
                            area = findAreaBycounty(county_global);
                        }
                        var cityies = GLOBAL.geo[area].cities;
                        context.updateViewUi(area);
                        context.updateView(cityies, 'city');

                        var ct = context.updateViewUiCounty(county_global);
                        context.updateViewCounty(ct);
                        context.updateViewUiConstituency(constituency_global);
                    } else {
                        alert('出現錯誤，請稍後再試！');
                    }
                }, 'json');
            }
            function findAreaBycounty(county) {
                var area = void 0;
                for (var i in GLOBAL.geo) {
                    var cities = GLOBAL.geo[i].cities;
                    console.log('iterate ...area:' + i);
                    for (var j in cities) {
                        var ct = GLOBAL.geo[i].cities[j].cne;
                        if (county == ct) {
                            console.log('city match ...area:' + county);
                            area = i;
                            break;
                        }
                    }

                    if (typeof area != 'undefined') break;
                }
                return area;
            }
            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
        // datafetchCounty(){

        // }

    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.select-area > a').each(function () {
                var id = $(this).data('id');
                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            GLOBAL.area = area;
        }
    }, {
        key: 'updateViewUiCounty',
        value: function updateViewUiCounty() {
            var county = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            var tmp = county;
            if (county == 0) {
                county = $('.select-county a:first').data('id');
            }
            GLOBAL.county = county;
            $('.select-county a').each(function () {

                var id = $(this).data('id');

                if (id == county) {
                    if (tmp != 0) $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });

            return county;
        }
    }, {
        key: 'updateViewUiConstituency',
        value: function updateViewUiConstituency() {
            var constituency = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;

            if (constituency == 0) {
                constituency = $('.select-constituency a:first').data('id');
            }
            GLOBAL.constituency = constituency;
            $('.select-constituency a').each(function () {
                var id = $(this).data('id');
                if (id == constituency) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
            var context = this;
            context.anim();
        }

        /**
         * 更新區域option們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {
            var context = this;
            if ($('.select-county  a').length >= 10) {
                $('.select-county').slick('unslick');
            }
            $('.select-county').html('');
            for (var i in cityies) {
                $('.select-county').append('\n             <a href="' + prefixUrl_global + cityies[i].cne + '/#' + GLOBAL.area + '" data-id="' + cityies[i].cne + '">' + cityies[i].cne + '</a>\n              \n              ');
            }
            context.bindcounty();
            enableSlick$1($('.select-county'));
        }
        /**
         * RENDER 每區的方塊資訊
         * @param  {[type]} cityies [description]
         * @return {[type]}         [description]
         */

    }, {
        key: 'updateViewCounty',
        value: function updateViewCounty(county) {
            return;
            var context = this;

            var cityies = void 0;
            if (GLOBAL.area.indexOf('原住民') < 0) {
                var items = GLOBAL.constituencies;
                cityies = $.grep(items, function (item) {
                    return item.county.indexOf(county) >= 0;
                });
            } else {
                var _items = GLOBAL.constituencies;
                var area = GLOBAL.area == "高山原住民" ? '山地原住民' : GLOBAL.area;
                cityies = $.grep(_items, function (item) {
                    return item.county.indexOf(county) >= 0 && item.district.indexOf(area) >= 0;
                });
            }

            if ($('.select-constituency  a').length >= 10) {
                $('.select-constituency').slick('unslick');
            }
            $('.select-constituency').html('');

            for (var i in cityies) {
                var consti = Number(cityies[i].constituency) < 10 ? "0" + cityies[i].constituency + "區" : cityies[i].constituency + "區",
                    district = cityies[i].district;
                $('.select-constituency').append('\n                <a href="' + prefixUrl_global + county + '/' + cityies[i].constituency + '/#' + GLOBAL.area + '" data-id="' + cityies[i].constituency + '" data-info="' + cityies[i].district + '">' + consti + '\n                </a>\n                  ');
            }

            enableSlick$1($('.select-constituency'));

            $('.select-constituency a').each(function () {

                $(this).off('hover').hover(function () {
                    var id = $(this).data('id');
                    var info = $(this).data('info');
                    console.log('hover....' + id);
                    $('.hover-info p').html('' + info);
                    $('.hover-info').show();
                }, function () {
                    $('.hover-info').hide();
                });
            });

            // context.anim()
        }
    }, {
        key: 'anim',
        value: function anim() {

            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                console.log('add color...');
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });

            context.detailbind();
        }
    }, {
        key: 'detailbind',
        value: function detailbind() {
            var collapsestates = {};
            $('.content-item').each(function () {
                var id = $(this).data('id');
                $(this).find('.content-detail ').css('height', 0);
                collapsestates[id] = 0;
                $(this).find('.btn-detail').click(function () {
                    var dom = $(this).parent().parent().parent();
                    var ID = dom.data('id');
                    var detail = dom.find('.content-detail');

                    if (collapsestates[id] == 0) {
                        autoHeightAnimate(detail, 500);
                        collapsestates[id] = 1;
                    } else {
                        detail.animate({ height: '0' }, 500);
                        collapsestates[id] = 0;
                    }
                });
            });
            function autoHeightAnimate(element, time) {
                var curHeight = element.height(),
                    // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
                element.height(curHeight); // Reset to Default Height
                element.stop().animate({ height: autoHeight }, time); // Animate to Auto Height
            }
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bindcounty',
        value: function bindcounty() {
            var context = this;
            $('.select-county > a').off('click').click(function () {
                var id = $(this).data('id');
                console.log("id..." + id);
                var ct = context.updateViewUiCounty(id);
                context.updateViewCounty(ct);
                context.updateViewUiConstituency(0);
            });
        }
    }, {
        key: 'bind',
        value: function bind() {

            var context = this;
            var currFilter = void 0;
            $('.select-area a').off('click').click(function () {
                var area = $(this).data('id');
                if (area == "") {
                    area = "六都";
                }
                var cityies = GLOBAL.geo[area].cities;
                context.updateViewUi(area);
                context.updateView(cityies, 'city');

                var ct = context.updateViewUiCounty(0);
                context.updateViewCounty(ct);
                context.updateViewUiConstituency(0);
            });

            // check if any .act in filters


            $('.filters > .f-item').each(function () {

                if ($(this).hasClass('act')) {
                    var id = $(this).data('id');
                    console.log('filters act id ...' + id);
                    currFilter = id;
                }

                $(this).click(function () {
                    var id = $(this).data('id');
                    $('.filters > .f-item').removeClass('act');
                    if (id != currFilter) {
                        currFilter = id;
                        $(this).addClass('act');
                    }
                });
            });
        }
    }]);
    return BILL;
}(Main);

function enableSlick$1(dom) {
    if (dom.find('a').length >= 10) dom.slick({
        dots: false,
        infinite: false,
        speed: 700,
        slidesToShow: 10,
        slidesToScroll: 1,
        responsive: [{
            breakpoint: 1000,
            settings: {
                slidesToShow: 6,
                slidesToScroll: 1,
                infinite: false

            }
        }, {
            breakpoint: 567,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: false

            }
        }]
    });
}

function WatchMove$1() {
    var data = {};
    var force = 0;

    function loop() {
        var bodyW = Number(getBrowserWidth());
        var vw = Number($('.head-j').width());
        var deltaX = GLOBAL.mousex - bodyW / 2;
        if (deltaX > 0) {
            $('.hover-area .tri').css('left', '75%');
            $('.hover-area').css('left', deltaX + vw / 2 - 90);
        } else {
            $('.hover-area .tri').css('left', '20px');
            $('.hover-area').css('left', deltaX + vw / 2);
        }

        requestAnimationFrame(loop);
    }
    function init() {
        $('body').mousemove(function (event) {
            var clientCoords = "( " + event.clientX + ", " + event.clientY + " )";
            GLOBAL.mousex = event.clientX;
        });
        loop();
    }
    init();
}

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$10 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var BALLOT = function (_Main) {
    inherits(BALLOT, _Main);

    function BALLOT() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'ballot';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, BALLOT);

        var _this = possibleConstructorReturn(this, (BALLOT.__proto__ || Object.getPrototypeOf(BALLOT)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );

        return _this;
    }

    createClass(BALLOT, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(BALLOT.prototype.__proto__ || Object.getPrototypeOf(BALLOT.prototype), 'init', this).call(this);
            this.anim();
            new ARROWS($('.pagemanager'));
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

        // datafetchCounty(){

        // }


    }, {
        key: 'anim',
        value: function anim() {

            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                console.log('add color...');
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            var currFilter = void 0;
            console.log('binding...........');
            $('.filters > .f-item').each(function () {

                if ($(this).hasClass('act')) {
                    var id = $(this).data('id');
                    console.log('filters act id ...' + id);
                    currFilter = id;
                }

                $(this).click(function () {
                    var id = $(this).data('id');
                    $('.filters > .f-item').removeClass('act');
                    if (id != currFilter) {
                        currFilter = id;
                        $(this).addClass('act');
                    }
                });
            });
        }
    }]);
    return BALLOT;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$11 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var WISH_LIST = function (_Main) {
    inherits(WISH_LIST, _Main);

    function WISH_LIST() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'wish list';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, WISH_LIST);

        var _this = possibleConstructorReturn(this, (WISH_LIST.__proto__ || Object.getPrototypeOf(WISH_LIST)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );

        return _this;
    }

    createClass(WISH_LIST, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(WISH_LIST.prototype.__proto__ || Object.getPrototypeOf(WISH_LIST.prototype), 'init', this).call(this);
            this.anim();
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

        // datafetchCounty(){

        // }


    }, {
        key: 'anim',
        value: function anim() {

            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                console.log('add color...');
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            var currFilter = void 0;
            console.log('binding...........');
            $('.filters > .f-item').each(function () {

                if ($(this).hasClass('act')) {
                    var id = $(this).data('id');
                    console.log('filters act id ...' + id);
                    currFilter = id;
                }

                $(this).click(function () {
                    var id = $(this).data('id');
                    $('.filters > .f-item').removeClass('act');
                    if (id != currFilter) {
                        currFilter = id;
                        $(this).addClass('act');
                    }
                });
            });
            $('.select-county-blk > div ').hover(function () {

                TweenMax.to($(this).find('.hover-info'), .3, { opacity: 1 });
            }, function () {
                TweenMax.to($(this).find('.hover-info'), .3, { opacity: 0 });
            });
        }
    }]);
    return WISH_LIST;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$12 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var WISH = function (_Main) {
    inherits(WISH, _Main);

    function WISH() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'wish';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, WISH);

        var _this = possibleConstructorReturn(this, (WISH.__proto__ || Object.getPrototypeOf(WISH)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );
        new ARROWS($('.pagemanager'));
        return _this;
    }

    createClass(WISH, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(WISH.prototype.__proto__ || Object.getPrototypeOf(WISH.prototype), 'init', this).call(this);
            this.anim();
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

        // datafetchCounty(){

        // }


    }, {
        key: 'anim',
        value: function anim() {

            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';

            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                console.log('add color...');
                $(this).find('.bg').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            var context = this;
            var currFilter = void 0;
            console.log('binding...........');
            $('.filters > .f-item').each(function () {

                if ($(this).hasClass('act')) {
                    var id = $(this).data('id');
                    console.log('filters act id ...' + id);
                    currFilter = id;
                }

                $(this).click(function () {
                    var id = $(this).data('id');
                    $('.filters > .f-item').removeClass('act');
                    if (id != currFilter) {
                        currFilter = id;
                        $(this).addClass('act');
                    }
                });
            });
            // $('.select-county-blk > div ').hover(function(){

            //     TweenMax.to($(this).find('.hover-info') , .3 , {opacity:1})
            // } , function(){
            //      TweenMax.to($(this).find('.hover-info') , .3 , {opacity:0})
            // })
        }
    }]);
    return WISH;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$13 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var WISH_EDITOR = function (_Main) {
    inherits(WISH_EDITOR, _Main);

    function WISH_EDITOR() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'wish editor';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, WISH_EDITOR);

        var _this = possibleConstructorReturn(this, (WISH_EDITOR.__proto__ || Object.getPrototypeOf(WISH_EDITOR)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );

        return _this;
    }

    createClass(WISH_EDITOR, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(WISH_EDITOR.prototype.__proto__ || Object.getPrototypeOf(WISH_EDITOR.prototype), 'init', this).call(this);

            simplemde = new SimpleMDE({ element: document.getElementById("simplemde") });
        }
        /**
         * 檢查有沒有給#區域
         * @return HASH
         */

        /**
         * 抓特定年份重新整理資料到  GLOBAL.geo
         * @param  {[type]} area [description]
         * @param  {[type]} year [description]
         * @return {[type]}      [description]
         */

        // datafetchCounty(){

        // }


    }, {
        key: 'anim',
        value: function anim() {}
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {}
    }]);
    return WISH_EDITOR;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$14 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var RESUME_BILLS = function (_Main) {
    inherits(RESUME_BILLS, _Main);

    function RESUME_BILLS() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'resume-bills';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, RESUME_BILLS);

        var _this = possibleConstructorReturn(this, (RESUME_BILLS.__proto__ || Object.getPrototypeOf(RESUME_BILLS)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        _this.slickTool();
        _this.updateView();
        _this.anim();
        _this.detailbind();
        new ARROWS($('.pagemanager'));
        return _this;
    }

    createClass(RESUME_BILLS, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(RESUME_BILLS.prototype.__proto__ || Object.getPrototypeOf(RESUME_BILLS.prototype), 'init', this).call(this);
        }
    }, {
        key: 'updateView',
        value: function updateView() {
            var typ = $('.wrapper-header').data('type');
            $('.nav-resume-all  a').each(function () {
                var atyp = $(this).data('type');
                if (atyp == typ) {
                    $(this).addClass('act');
                }
            });

            $('nav.navbar , nav.navbar .bg-cover').addClass('bg-' + typ);
        }
    }, {
        key: 'slickTool',
        value: function slickTool() {
            $('.nav-resume-all').on('init', function () {
                console.log('carousel3 has init....');
                $('.nav-resume-all .slick-prev').html('<i class="fa fa-arrow-right"></i>');
                $('.nav-resume-all .slick-next').html('<i class="fa fa-arrow-right"></i>');
            });
            $('.nav-resume-all').slick({

                dots: false,
                infinite: false,
                speed: 700,
                slidesToShow: 5,
                slidesToScroll: 1,
                responsive: [{
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 4,
                        infinite: false

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: false

                    }
                }]
            });
        }
    }, {
        key: 'detailbind',
        value: function detailbind() {
            var collapsestates = {};
            $('.content-item').each(function () {
                var id = $(this).data('id');
                $(this).find('.content-detail ').css('height', 0);
                collapsestates[id] = 0;
                $(this).find('.btn-detail').click(function () {
                    var dom = $(this).parent().parent().parent();
                    var ID = dom.data('id');
                    var detail = dom.find('.content-detail');

                    if (collapsestates[id] == 0) {
                        autoHeightAnimate(detail, 500);

                        TweenMax.to($(this).find('i'), .3, { rotation: 180 });
                        collapsestates[id] = 1;
                    } else {
                        detail.animate({ height: '0' }, 500);
                        TweenMax.to($(this).find('i'), .3, { rotation: 0 });
                        collapsestates[id] = 0;
                    }
                });
            });
            function autoHeightAnimate(element, time) {
                var curHeight = element.height(),
                    // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
                element.height(curHeight); // Reset to Default Height
                element.stop().animate({ height: autoHeight }, time); // Animate to Auto Height
            }
        }
    }, {
        key: 'anim',
        value: function anim() {
            var context = this;
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-dark-group-color';
            $('.content-list > .content-item ').each(function () {
                var n = (count + rndint) % 30 + 1;
                console.log('add color...');
                $(this).addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {}
    }]);
    return RESUME_BILLS;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$15 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var SEEMORE = function (_Main) {
    inherits(SEEMORE, _Main);

    function SEEMORE() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'seemore';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, SEEMORE);

        var _this = possibleConstructorReturn(this, (SEEMORE.__proto__ || Object.getPrototypeOf(SEEMORE)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        var hash = _this.chkIgContainsHash();
        //this.datafetch( hash );

        return _this;
    }

    createClass(SEEMORE, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(SEEMORE.prototype.__proto__ || Object.getPrototypeOf(SEEMORE.prototype), 'init', this).call(this);
            this.anim();
        }
    }, {
        key: 'chkIgContainsHash',
        value: function chkIgContainsHash() {
            var link = location.href;
            var hash = $.param.fragment(link); //.split('#')[1];

            if (hash) {
                console.log("hash " + hash);
            }
            return decodeURIComponent(hash);
        }
    }, {
        key: 'datafetch',
        value: function datafetch() {
            var area = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '六都';
            var year = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2018;

            var context = this;
            if (year_global) year = year_global;
            $.get(jsonUrl_global, function (pResponse) {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');
                    if (area == "") {
                        area = "六都";
                    }
                    var cityies = GLOBAL.geo[area].cities;
                    context.updateViewUi(area);
                    context.updateView(cityies, 'city');
                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');

            function updateData(category) {

                GLOBAL.geo[category] = { cities: [] };
                //找出有山地原住民
                var items = GLOBAL.constituencies;

                var cts = $.grep(items, function (item) {
                    if (category == '高山原住民') return item.district.indexOf('山地原住民') >= 0;else return item.district.indexOf(category) >= 0;
                });

                //console.log(cts)
                var norepeatcts = _.groupBy(cts, function (ct) {
                    return ct.county;
                });

                for (var ct in norepeatcts) {
                    console.log('norepeatcts ...' + ct);
                    var eng = findEngCounty(ct);
                    GLOBAL.geo[category].cities.push({ cne: ct, eng: eng });
                }
            }

            function findEngCounty(countyval) {
                var all = GLOBAL.allcities;
                var cts = $.grep(all, function (item) {

                    return item.cne.indexOf(countyval) >= 0;
                });
                return cts[0].eng;
            }
        }
    }, {
        key: 'updateViewUi',
        value: function updateViewUi(area) {

            $('.select-area > a').each(function () {

                var id = $(this).data('id');

                if (id == area) {
                    $(this).addClass('act');
                } else {
                    $(this).removeClass('act');
                }
            });
        }

        /**
         * 更新區域方塊們
         * @param  {[type]} cityies [description]
         * @param  {[type]} typ     要更新的內容為城市或是選區
         * @return {[type]}         NULL
         */

    }, {
        key: 'updateView',
        value: function updateView(cityies, typ) {

            var context = this;

            $('.select-county-blk').html('');

            if (typ == 'city') {
                for (var i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3"><a class="info" href="/candidates/councilors/' + cityies[i].cne + '">\n                  <p>' + cityies[i].cne + '</p>\n                  <p class="eng">' + cityies[i].eng + '</p></a>\n                  </div>\n                  ');
                }
            } else {
                for (var _i in cityies) {

                    $('.select-county-blk').append('\n                  <div class="col-xs-6 col-sm-3">\n                  <a class="info councilmen-area" href="/candidates/councilors/' + cityies[_i].cne + '">\n                  <p></p>\n                  <p class="eng">01</p>\n                  <div class="area-info">\u6843\u6E90\u5340\u3001\u90A3\u746A\u590F\u5340\u3001\u7532\n                    \u4ED9\u5340\u3001\u516D\u9F9C\u5340\u3001\u6749\u6797\u5340\n                    \u3001\u5167\u9580\u5340\u3001\u65D7\u5C71\u5340\u3001\u7F8E\n                    \u6FC3\u5340\u3001\u8302\u6797\u5340 </div>\n                  </a>\n                  \n                  </div>\n                  ');
                }
            }

            context.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {
            console.log('update View...');
            var count = 0;
            var rnd = Math.random() * 30;
            var rndint = Math.ceil(rnd);
            var colorclass = 'bg-light-group-color';
            //console.log(rndint)
            $('.select-county-blk > div ').each(function () {
                var n = (count + rndint) % 30 + 1;
                //console.log('n....'+n)
                $(this).find('.info').addClass(colorclass + n);
                TweenMax.fromTo($(this), .7, { opacity: 0, y: 20 }, { delay: .5 + count * .05, opacity: 1, y: 0, ease: Back.easeOut });
                count++;
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {
            // const context = this;
            // $('.select-area > a').click(function(){
            //     let id = $(this).data('id');
            //     context.datafetch(id)
            // })

            $('.select-county-blk > div ').hover(function () {

                TweenMax.to($(this).find('.hover-info'), .3, { opacity: 1 });
            }, function () {
                TweenMax.to($(this).find('.hover-info'), .3, { opacity: 0 });
            });
        }
    }]);
    return SEEMORE;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$16 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var SEEMORE_DETAIL = function (_Main) {
    inherits(SEEMORE_DETAIL, _Main);

    function SEEMORE_DETAIL() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'see more detail';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, SEEMORE_DETAIL);

        var _this = possibleConstructorReturn(this, (SEEMORE_DETAIL.__proto__ || Object.getPrototypeOf(SEEMORE_DETAIL)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch(hash);
        //this.anim();
        return _this;
    }

    createClass(SEEMORE_DETAIL, [{
        key: 'init',
        value: function init() {
            get(SEEMORE_DETAIL.prototype.__proto__ || Object.getPrototypeOf(SEEMORE_DETAIL.prototype), 'init', this).call(this);
            $('.select-opt2').slick({
                dots: false,
                infinite: false,
                speed: 700,
                slidesToShow: 4,
                slidesToScroll: 1,
                responsive: [{
                    breakpoint: 1000,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        infinite: false

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 3,
                        infinite: false

                    }
                }]
            });
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {

            // console.log('binding....');
            // const context = this;
            // $('.select-area > a').click(function(){
            //     let area = $(this).data('id');
            //     // context.datafetch(id);
            //     if(area==""){area="六都"}
            //         let cityies = GLOBAL.geo[area].cities;

            //         context.updateViewUi(area)
            //         context.updateView(cityies)
            //         context.updateViewUiCounty(0)
            // })
        }
    }]);
    return SEEMORE_DETAIL;
}(Main);

//import _ from 'underscore';
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body$17 = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');

var DEFAULT = function (_Main) {
    inherits(DEFAULT, _Main);

    function DEFAULT() {
        var NAME = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'default';
        var ifFB = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
        var ifYT = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        var ifScrollHandle = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
        classCallCheck(this, DEFAULT);

        var _this = possibleConstructorReturn(this, (DEFAULT.__proto__ || Object.getPrototypeOf(DEFAULT)).call(this, NAME, ifFB, ifYT, ifScrollHandle));

        _this.TEST = false;
        // this.data = new DATA();
        // this.data.init();

        _this.init();
        _this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );

        return _this;
    }

    createClass(DEFAULT, [{
        key: 'init',
        value: function init() {
            var context = this;
            get(DEFAULT.prototype.__proto__ || Object.getPrototypeOf(DEFAULT.prototype), 'init', this).call(this);
            this.anim();
        }
    }, {
        key: 'anim',
        value: function anim() {

            var pg = $('#page').val();
            console.log('anim init...' + pg);
            if (pg == 'about') {
                TweenMax.fromTo($('.part-left'), .5, { y: -50, opacity: 0 }, { delay: .8, y: 0, opacity: 1, ease: Expo.easeOut });
                TweenMax.fromTo($('.part-right'), .5, { y: 50, opacity: 0 }, { delay: .8, y: 0, opacity: 1, ease: Expo.easeOut });
                TweenMax.fromTo($('.bg-right'), .5, { scaleY: 0 }, { delay: .5, scaleY: 1, transformOrigin: "0 100%" });
            }
        }
    }, {
        key: 'watchScroll',
        value: function watchScroll() {}
    }, {
        key: 'bind',
        value: function bind() {}
    }]);
    return DEFAULT;
}(Main);

function MENU() {
    var curr = 0,
        last = 0,
        sanim = void 0,
        interval = void 0,
        state = void 0,
        bgState = 'off';
    function route(hash) {
        var $body = window.opera ? document.compatMode == "CSS1Compat" ? $('html') : $('body') : $('html,body');
        var top = void 0;
        var navh = $('nav').height() + 20;
        top = $("#" + hash).offset().top;
        //TweenMax.set(window, {scrollTo:{y:top}});
        $body.animate({
            scrollTop: top - navh
        }, 700);
        updateState(hash);
    }

    function getHash() {
        var hash = document.location.hash;
        //     id = hash.match(re); // for some reason this matches both the full string and the number
        // id = id.pop();
        return hash;
    }

    function scrollBy() {
        var typ = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "share";

        if (typ != "body") {
            $('html , body').css("overflow-y", "hidden");
        } else {
            $('html , body').css("overflow-y", "auto");
        }
    }

    function showPop() {
        var typ = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "game";

        console.log("showPop:" + typ);
        if (typ == 'game') $(".btn-qa-kv").trigger("click");else {
            var id = typ.replace("result", "");
            console.log("result:" + id);
            $('#result' + id + '_pop').trigger('click');
            GLOBAL.ga.GT('/bot-web', '.pv.' + typ, '');
        }
    }

    function bind() {
        $('.navbar-search').hover(function () {

            TweenMax.to($(this).find('input'), .5, { 'width': 100 });
            var toggle = $('.navbar-menu').attr('data-toggle');

            if (toggle != 'collapse') {
                var bg = $('.navbar .bg-cover');
                $('#navbar').animate({ height: 0 }, 300);
                $('.navbar-menu').attr('data-toggle', 'collapse');
                TweenMax.to($(".navbar-toggle .icon-bar.top"), .3, { y: 0, x: 0, rotation: 0, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.mid"), .3, { opacity: 1, rotation: 0, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.bottom"), .3, { y: 0, x: 0, rotation: 0, transformOrigin: "50% 50%" });
                $('#navbar ul li ').each(function () {
                    TweenMax.to($(this), .3, { opacity: 0, y: 20 });
                });
                if ($(window).scrollTop() < 60) {
                    TweenMax.to(bg, .5, { delay: .2, opacity: 0, ease: Expo.easeOut });
                }
            }
        }, function () {
            TweenMax.to($(this).find('input'), .5, { 'width': 1 });
        });
        $('.navbar-menu').click(function () {
            var toggle = $(this).attr('data-toggle');
            collapseNav(toggle);
        });
        function collapseNav(toggle) {
            var bg = $('.navbar .bg-cover');
            var autoHeight = parseInt($('#navbar').css('height', 'auto').height());
            if (toggle == "collapse") {
                $('#navbar').css('height', 0);
                $('.navbar-menu').attr('data-toggle', 'expand');
                // TweenMax.to($('#navbar') , .5,{height:'auto'})
                $('#navbar').animate({ height: autoHeight }, 300);
                TweenMax.to(bg, .5, { opacity: 1, ease: Expo.easeOut });
                TweenMax.to($(".navbar-toggle .icon-bar.top"), .2, { y: 6, x: 0, rotation: 45, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.mid"), .2, { opacity: 0, rotation: 45, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.bottom"), .2, { y: -6, x: 0, rotation: -45, transformOrigin: "50% 50%" });
                var count = 0;
                $('#navbar ul li ').each(function () {
                    TweenMax.fromTo($(this), .5, { opacity: 0, y: 20 }, { opacity: 1, y: 0, delay: .05 * count, ease: Back.easeOut });
                    count++;
                });
            } else {

                $('#navbar').animate({ height: 0 }, 300);
                $('.navbar-menu').attr('data-toggle', 'collapse');
                TweenMax.to($(".navbar-toggle .icon-bar.top"), .3, { y: 0, x: 0, rotation: 0, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.mid"), .3, { opacity: 1, rotation: 0, transformOrigin: "50% 50%" });
                TweenMax.to($(".navbar-toggle .icon-bar.bottom"), .3, { y: 0, x: 0, rotation: 0, transformOrigin: "50% 50%" });

                $('#navbar ul li ').each(function () {
                    TweenMax.to($(this), .3, { opacity: 0, y: 20 });
                });
                if ($(window).scrollTop() < 60) {
                    TweenMax.to(bg, .5, { delay: .2, opacity: 0, ease: Expo.easeOut });
                }
            }
        }

        $("a.hash").each(function () {
            console.log("hash");
            $(this).click(function (e) {
                e.preventDefault();
                var ga = $(this).data("ga");
                var link = $(this).attr('href');
                var hash = $.param.fragment(link).split('/')[1];
                console.log("hash " + hash);
                if ($('#' + hash).parents('html').length > 0) {
                    var toggle = $('.navbar-toggle');
                    if (toggle.attr('aria-expanded') == 'true') toggle.trigger('click');

                    GLOBAL.ga.GT($(this).parent().hasClass('banner') ? '/nav-banner' : '/nav', '.btn.' + ga, "");
                    switch (ga) {
                        case "game":

                            if (GLOBAL.started != 1) showPop(hash);
                            break;
                        case "promo":
                            route(ga);
                            break;
                        case "blogger":
                            route(ga);
                            break;
                        case "trial":
                            sendTrackParam('JYfp037zYK7Q', "btn A", "", "", "", "", "", "", "", "", "", "", "");
                            route(ga);
                            break;

                    }
                } else {
                    GLOBAL.ga.GT($(this).parent().hasClass('banner') ? '/nav-banner' : '/nav', '.btn.' + ga, "");
                    if ($(this).parent().hasClass('banner')) {
                        if (ga == 'trial') {
                            sendTrackParam('JYfp037zYK7Q', "", "btn B", "", "", "", "", "", "", "", "", "", "");
                            findoutRedeemNow();
                        } else findoutPetCombination();
                    }
                    setTimeout(function () {
                        location.href = link;
                    }, 300);
                }

                return false;
            });
        });
        $("nav ul li ").each(function () {
            $(this).hover(function () {

                TweenMax.to($(this).find('.line'), .5, { opacity: 1, scaleX: 1, transformOrigin: "0% 0%", ease: Cubic.easeOut });
            }, function () {
                if (!$(this).hasClass('act')) TweenMax.to($(this).find('.line'), .5, { opacity: 0, scaleX: 0, transformOrigin: "0% 0%", ease: Cubic.easeIn });
            });
        });
        // $('.dropdown').on('show.bs.dropdown', function() {
        //     $(this).find('.dropdown-menu').first().slideDown(500);
        //     $(this).find('.dropdown-toggle .plus').html('-')
        // });

        // // Add slideUp animation to Bootstrap dropdown when collapsing.
        // $('.dropdown').on('hide.bs.dropdown', function() {
        //     $(this).find('.dropdown-menu').first().hide();
        //     $(this).find('.dropdown-toggle .plus').html('+')
        // });

        // $('#navbar .btn-close img').click(function(){
        //     $('.navbar-toggle').trigger("click")
        // })
    }
    this.getupdateState = function (id) {
        updateState(id);
    };

    function updateState(id) {

        curr = id;
        $('nav #navbar > ul > li ').each(function () {
            var ga = $(this).data('ga');
            if (curr == ga) {
                $(this).addClass('act');
                //TweenMax.to($(this).find('.line') , .5 ,{opacity:0 , scaleX:0, transformOrigin:"0% 0%",ease:Cubic.easeOut})
            } else {
                $(this).removeClass('act');
                TweenMax.to($(this).find('.line'), .5, { opacity: 0, scaleX: 0, transformOrigin: "0% 0%", ease: Cubic.easeOut });
            }
        });
    }

    function chgState(obj, id, typ) {
        clearTimeout(interval);
        if (typ == "act") {
            if (id != 'fb') {}
        } else {

            //sanim.setPolyOpen(curr)
        }
    }

    function bind_html_link() {
        $('nav li ').not('.hash').each(function () {
            // $(this).hover(function() {
            //     let id = $(this).data('id');
            //     if (id != curr)
            //         chgState($(this), id, 'act')
            // }, function() {
            //     let id = $(this).data('id');
            //     if (id != curr)
            //         chgState($(this), id, 'dis')
            // })
            $(this).find('.tracklink').hover(function () {
                TweenMax.to($(this).find('i'), .2, { x: 5 });
            }, function () {
                TweenMax.to($(this).find('i'), .2, { x: 0 });
            });
            $(this).find('.tracklink').click(function (e) {

                var target = $(this).attr('target');
                var href = $(this).attr('href');
                var act = $(this).data('act');

                var ga = $(this).data('ga');
                //GLOBAL.ga.GT('/nav', '.click' , ga );

                GLOBAL.ga.GT('/nav', '.btn.' + ga, "");
                if (ga == 'tobuy') {
                    console.log('tobuy ...... media');
                    //cy_action_conver('5558404','sccvbrgm','53','2');
                }
                clk(target, href, act, ga, e);

                return false;
            });
        });

        $(".wrapper .tracklink").click(function (e) {
            var target = $(this).attr('target');
            var href = $(this).attr('href');
            var act = $(this).data('act');
            var ga = $(this).data('ga');
            //GLOBAL.ga.GT('/nav', '.click' , ga );
            var page = $('#page').val();
            GLOBAL.ga.GT('/' + page, '.btn.' + ga, "");

            if (ga == 'tobuy1' || ga == 'tobuy2' || ga == 'tobuy3') {
                console.log('tobuy ......media');
                switch (ga) {
                    case 'tobuy1':
                        //活力保養組
                        momBuyEnergy();
                        break;
                    case 'tobuy2':
                        //水乳霜組
                        momBuyWaterMilk();
                        break;
                    // case 'tobuy3':
                    //     cy_action_conver('5558404','zlfzrecu','53','2');
                    // break;
                }
            }
            clk(target, href, act, ga, e);
            return false;
        });

        $('.navbar-header').find('.tracklink').click(function (e) {

            var target = $(this).attr('target');
            var href = $(this).attr('href');
            var act = $(this).data('act');
            var ga = $(this).data('ga');
            GLOBAL.ga.GT('/nav', '.btn.' + ga);
            clk(target, href, act, ga, e);
            return false;
        });

        function clk(target, href, act, ga, e) {
            e.preventDefault();
            //GLOBAL.ga.GT('/menu', '.btn.' + ga);
            if (act == "disable") {
                alert("敬請期待!");
            } else if (target === '_blank') {
                if (ga == "tvc") {
                    //window.open(href, target  , "width=600,height=400");
                    $('.pop-tvc').fadeIn('fast');
                    TweenMax.to($('.banner'), .5, { x: 140, ease: Cubic.easeOut });
                } else window.open(href, target);
            } else {
                setTimeout(function () {
                    window.open(href, '_self');
                }, 300);
            }
        }
    }

    function chkIgContainsHash() {
        var link = location.href;
        var hash = $.param.fragment(link); //.split('#')[1];
        console.log("hash " + hash);
        if (hash) {
            try {
                if ($('#' + hash).parents('html').length > 0) {
                    if (hash == "game" || hash.indexOf("result") >= 0) {
                        showPop(hash);
                        return;
                    }
                    setTimeout(function () {
                        route(hash);
                    }, 1000);
                } else {
                    //location.href = link;
                }
            } catch (err) {}

            // } catch (err) {}
        }
    }
    function loop() {
        var top = GLOBAL.top;

        if (top > 0) {
            if (bgState != 'on') {
                TweenMax.killTweensOf($('.navbar >.container >.bg'));
                TweenMax.to($('.navbar >.container >.bg'), 1, { opacity: 1, ease: Expo.easeOut });
            }
            bgState = 'on';
        } else {
            if (bgState != 'off') {
                TweenMax.killTweensOf($('.navbar >.container >.bg'));
                TweenMax.to($('.navbar >.container >.bg'), 1, { opacity: 0, ease: Expo.easeOut });
            }

            bgState = 'off';
        }
        setTimeout(loop, 20);
    }
    this.init = function () {
        setTimeout(chkIgContainsHash, 100);
        //updateState(curr);
        bind_html_link();
        bind();
        loop();
    };
    this.init();
}

//import {COUNCILMEN_COUNTY} from './pages/councilmen_county.js';
//import {COUNCILMEN} from './pages/councilmen.js';

var app = {};
function APP() {
	var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame || function (callback) {
		window.setTimeout(callback, 1000 / 60);
	};
	window.requestAnimationFrame = requestAnimationFrame;

	function route() {
		var page = $('#page').val();
		switch (page) {

			case 'index':
				new INDEX();
				return true;
				break;
			case 'county-mayor-area':
				new COUNTY_MAYER_AREA();
				return true;
				break;
			case 'county-mayor':
				new COUNTY_MAYER();
				return true;
				break;
			case 'resume':
				new RESUME();
				return true;
				break;

			case 'councilmen-area':
				new COUNCILMEN_AREA();
				return true;
				break;
			case 'councilmen-county':
				new COUNCILMEN_COUNTY();
				return true;
				break;
			case 'councilmen':
				new COUNCILMEN();
				return true;
				break;
			case 'seemore':
				new SEEMORE();
				return true;
				break;
			case 'seemore-detail':
				new SEEMORE_DETAIL();
				return true;
				break;
			case 'bill-area':
				new BILL_AREA();
				return true;
				break;
			case 'bill-county':
				new BILL_COUNTY();
				return true;
				break;
			case 'bill':
				new BILL();
				return true;
				break;
			case 'ballot':
				new BALLOT();
				return true;
				break;
			case 'wish-list':
				new WISH_LIST();
				return true;
				break;
			case 'wish':
				new WISH();
				return true;
				break;
			case 'wish-editor':
				new WISH_EDITOR();
				return true;
				break;
			case 'resume-bills':
				new RESUME_BILLS();
				return true;
				break;
			default:
				new DEFAULT();
				return true;
				break;
		}
	}

	function init() {
		new LoadModle($('body img'), function () {
			//GLOBAL.ga = new GA();
			app.menu = new MENU();
			var tof = route();
			if (tof) {

				$('.loading img').fadeOut(500);
				$('.loading').delay(500).fadeOut(500);
			}
		});
	}
	init();
	console.log('app start.....');
}
app.start = new APP();

}());
