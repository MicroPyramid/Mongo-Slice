;(function($,document,window){
	function Itip(element, options) {
		this.showItip = function(){
			showItip();
		};

		this.hideItip = function(){
			hideItip();
		};

		var defaults = {
			position: 'right',
			color: "#fff",
			backGround: '#24B2DA',
			fontSize: '12',
			interaction: false,
			content : false, //'false'
			autoClose: true,
			triggerBy: 'hover',
			animate: '',
			minWidth : "100", //auto, px
			maxWidth : "150",
			AfterOpen: function(){},
			AfterClose: function(){}

		},$this, arrowColor,seftMain=this,
		_init = function(){
			
			seftMain.options = $.extend(true,{},defaults,options);
			arrowColor = seftMain.options.position;
			seftMain.el = $(element);

			seftMain.elPos = {};
			seftMain.elementPos = {};
			_getElementPos();
			_setProperty();
			_setTooltipPos(seftMain.options.position);
			_initEvent();
		},
		_getElementPos = function(){
			
			seftMain.elPos.left = seftMain.el.offset().left;
			seftMain.elPos.top = seftMain.el.offset().top - $(window).scrollTop();
			seftMain.elPos.width = seftMain.el.width();
			seftMain.elPos.height = seftMain.el.height();
			if(seftMain.options.position === 'LorR') {
				arrowColor = seftMain.elPos.left < ($(window).width()-(seftMain.elPos.width+seftMain.elPos.left)) ? 'right':'left';
			}

		}, 

		setArrowColor = function(){
		
			var bc = 'border-'+arrowColor+'-color',
				obj = {};
			obj[bc] = seftMain.options.backGround;
			seftMain.mainTooltip.find('.arrow').css(obj);
		},

		_setProperty = function(){
			
			seftMain.tooltipWrapEl = $('<div>',{class: 'Itip-wrap'});
			defaultCss = {
				'position' : 'fixed',
				'top': '20px',
				'left': '50px'
			};
			seftMain.options.content = seftMain.options.content == false ? seftMain.el.attr('data-Itip') : seftMain.options.content;
			seftMain.tooltipWrapEl.css(defaultCss).addClass("itip");
			seftMain.itipInner = $('<div>',{ class: 'Itip-inner'});
			seftMain.arrow = $('<span>',{class : 'arrow',id : "arrow"});
			seftMain.itipInner.append(seftMain.arrow,$('<div class="Itip-content">'+seftMain.options.content+'</div>'));
			seftMain.tooltipWrapEl.append(seftMain.itipInner);
			$('body').append(seftMain.tooltipWrapEl);
			seftMain.mainTooltip = seftMain.tooltipWrapEl;//-> can xem lai doan nay
			seftMain.mainTooltip.addClass('animated '+seftMain.options.animate).css({display: 'none','background': seftMain.options.backGround});
			seftMain.mainTooltip.find('.Itip-content').css({'font-size': seftMain.options.fontSize + 'px','color': seftMain.options.color });
			setArrowColor();
			
			

			if (seftMain.options.minWidth != "auto" ) {
				seftMain.mainTooltip.css({"min-width": seftMain.options.minWidth + "px"});
			};
			if (seftMain.options.maxWidth != "auto" ) {
				seftMain.mainTooltip.css({"max-width": seftMain.options.maxWidth + "px"});
			};
		},
		_setTooltipPos = function(pos){
			
			var SetPos = function(arrow,top,right,bottom,left){
				seftMain.mainTooltip.css({top: top ,right: right,bottom: bottom,left: left  });	
				seftMain.arrow.removeClass();
				seftMain.arrow.addClass(arrow + ' arrow');
			}
			if(pos=='left'){
				SetPos("right",(seftMain.elPos.top + (seftMain.elPos.height/2) - seftMain.mainTooltip.height()/2),$(window).width()-seftMain.elPos.left,"auto","auto");
			}
			if(pos=='right'){
				SetPos("left",(seftMain.elPos.top + (seftMain.elPos.height/2) - seftMain.mainTooltip.height()/2),"auto","auto",(seftMain.elPos.left + seftMain.elPos.width));
			}
			if(pos=='bottom'){
				SetPos("top",(seftMain.elPos.top + seftMain.elPos.height),'auto','auto',(seftMain.elPos.left + (seftMain.elPos.width-seftMain.mainTooltip.width())/2));
			}
			if(pos=='top'){
				SetPos('bottom',seftMain.elPos.top - seftMain.mainTooltip.height(),'auto','auto',seftMain.elPos.left + (seftMain.elPos.width-seftMain.mainTooltip.width())/2);
			}
			if(pos=='LorR'){	
				if(seftMain.elPos.left < ($(window).width()-(seftMain.elPos.width+seftMain.elPos.left))) {
						SetPos("left",(seftMain.elPos.top + (seftMain.elPos.height/2) - seftMain.mainTooltip.height()/2),"auto","auto",(seftMain.elPos.left + seftMain.elPos.width));
						arrowColor = 'right';
						setArrowColor();
						//seftMain.options.position = 'right';
				} else{
				SetPos("right",(seftMain.elPos.top + (seftMain.elPos.height/2) - seftMain.mainTooltip.height()/2),$(window).width()-seftMain.elPos.left,"auto","auto");
					//seftMain.options.position = 'left';
					arrowColor = 'left';
						setArrowColor();
				}
				
			}	
		},
		_setInScreen =function(){

			if(seftMain.mainTooltip.offset().left<0){
				seftMain.mainTooltip.css({left: 0,right:"auto"});	
			}else if(  (seftMain.mainTooltip.offset().left + seftMain.mainTooltip.width()) > $(window).width()){
				seftMain.mainTooltip.css({right: 0,left: "auto"});
			}
		 } ,
		showItip =function(){
			
			seftMain.mainTooltip.show(50,function(){
				seftMain.options.AfterOpen();
				_setInScreen();
			});
		} ,
		hideItip =function(){
			
			seftMain.mainTooltip.hide(10,function(){
				seftMain.options.AfterClose();
			});
		} ,
		_initEvent = function(){
			
			$(window).scroll(function(event) {
				/* Act on the event */
				setTimeout(function(){
					_getElementPos();
					_setTooltipPos(seftMain.options.position);
					
				},10);
			});

			$(window).resize(function(event) {
				/* Act on the event */
				setTimeout(function(){
					_getElementPos();
					_setTooltipPos(seftMain.options.position);
					
				},10);
			});

			var self = seftMain,attr = $(seftMain.el).attr('id') != undefined ? '#'+$(seftMain.el).attr('id') : '.' + $(seftMain.el).attr('class');
			if(seftMain.options.triggerBy == "hover"){
				
				$(seftMain.el).on('mouseenter', function(e) {
					if(!self.mainTooltip.is(':visible')) {
						showItip();
					}
					e.preventDefault();
				});
				
				if(seftMain.options.autoClose == true ){
					if( seftMain.options.interaction == true) {

						$(seftMain.el).on('mouseleave', function(e) {
							if($('.Itip-wrap:hover').length <= 0){
								hideItip();
							}
							e.preventDefault();
						});

						self.mainTooltip.on('mouseleave', function(event) {
							if($(attr+':hover').length ==0){
								hideItip();
							}
						});	

					}else {
						$(seftMain.el).on('mouseleave', function(e) {
							
								hideItip();
							
							e.preventDefault();
						});
					}

					
				}
			} else if(seftMain.options.triggerBy == "click"){
				
				$(seftMain.el).on('click', function(e) {
					if($(".Itip-wrap").is(':visible') == false) {
						showItip();
					}else {
						hideItip();
					}
					e.preventDefault();
				});
			}
		};
		

		_init();
	}

	$.fn["Itip"] = function(options){
		var args = arguments;
		//debugger;
		if(options === undefined || typeof options === 'object') {
			return this.each(function(){
				if(!$(this).data('Itip')){
					$(this).data('Itip',new Itip(this,options));
				}
			});
		} else if(typeof options === 'string' && options[0] !== '_' && options){
			var returns;
			this.each(function(){
				var instance = $(this).data('Itip') == undefined ? $(this).data('Itip',new Itip(this,options)) : $(this).data('Itip') ;
				if(instance instanceof Itip && typeof instance[options] === 'function') {
					returns = instance[options].apply(instance,Array.prototype.slice.call(args,1));
				}
			});
			return returns !== undefined ? returns : this;
		}
	}

	
}(jQuery,document,window));
