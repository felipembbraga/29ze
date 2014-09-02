/**
 *
 * '||''|.                            '||
 *  ||   ||    ....  .... ...   ....   ||    ...   ... ...  ... ..
 *  ||    || .|...||  '|.  |  .|...||  ||  .|  '|.  ||'  ||  ||' ''
 *  ||    || ||        '|.|   ||       ||  ||   ||  ||    |  ||
 * .||...|'   '|...'    '|     '|...' .||.  '|..|'  ||...'  .||.
 *                                                  ||
 * --------------- By Display:inline ------------- '''' -----------
 *
 * Confirmation plugin
 *
 * Structural good practices from the article from Addy Osmani 'Essential jQuery plugin patterns'
 * @url http://coding.smashingmagazine.com/2011/10/11/essential-jquery-plugin-patterns/
 */

/*
 * The semi-colon before the function invocation is a safety
 * net against concatenated scripts and/or other plugins
 * that are not closed properly.
 */
;(function($, document){
	/*
	 * document is passed through as local variable rather than as global, because this (slightly)
	 * quickens the resolution process and can be more efficiently minified.
	 */

	// Objects cache
	var doc = $(document);

	/**
	 * Display the confirm message (older syntax kept for backward compatibility)
	 * @param jQuery target the clicked element
	 * @param event event the initial event
	 * @return void
	 */
	$.bsmodal = function(target, event)
	{

		// Show confirmation
		$(target).bsmodal();
	};

	/**
	 * Display the confirm message
	 * @param object options additional options (optional)
	 */
	$.fn.bsmodal = function(options)
	{
		return this.each(function() {
			var target = $(this),

			// Options
			settings = $.extend({}, $.bsmodal.defaults, options),

			//modal
			montador = $('<div class="modal" id="meuModal"></div>');
			modal = $('<div class="modal-dialog modal-lg"></div>');
			content = $('<div class="modal-content"></div>'); 
			modal.append(content);
			montador.append(modal);
			console.log(montador);
			// Open modal
			montador.modal({remote:settings.url, keyboard:settings.keyboard, show: settings.show, backdrop: settings.backdrop});
		});

	};
		/**
		 * Confirmation defaults
		 * @var object
		 */
		$.bsmodal.defaults = $.fn.bsmodal.defaults = {
				url: false,
				keyboard:true,
				show:true,
				backdrop:true
		};

		// Event binding
		doc.on('click', '.bsmodal', function(event)
				{

			// Show confirmation
			$(this).bsmodal();
				});

	})(jQuery, document);