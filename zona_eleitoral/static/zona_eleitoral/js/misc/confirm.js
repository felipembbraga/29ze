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
;(function($, document)
		{
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
	$.confirmar = function(target, event)
	{
		// Prevent default
		event.preventDefault();
		event.stopPropagation();

		// Show confirmation
		$(target).confirmar();
	};

	/**
	 * Display the confirm message
	 * @param object options additional options (optional)
	 */
	$.fn.confirmar = function(options)
	{
		return this.each(function()
				{
			var target = $(this),

			// Options
			settings = $.extend({}, $.confirmar.defaults, options),

			// Has the user made his choice?
			choose = false,

			// Callbacks
			onShow, onRemove,

			// Message
			message,

			// Buttons
			buttons, confirmButton, cancelButton,

			// Functions
			confirmFunc, cancelFunc;

			// If already confirmed, run
			if (target.data('confirmed'))
			{
				call = true;

				// Function on confirm
				if (settings.onConfirm)
				{
					if (settings.onConfirm.call(target[0]) !== false)
					{
						_runDefault(target);
					}
				}
				else
				{
					_runDefault(target);
				}

				return;
			}

			// Callback on show
			if (settings.onShow)
			{
				onShow = function()
				{
					settings.onShow.call(target[0], $(this));
				};
			}

			// Callback on remove
			onRemove = function()
			{
				// Abort callback
				if (!choose && settings.onAbort)
				{
					settings.onAbort.call(target[0]);
				}

				// Remove callback
				if (settings.onRemove)
				{
					settings.onRemove.call(target[0]);
				}
			};

			// Function on confirm button
			confirmFunc = function()
			{
				var call = true;

				// Mark as done
				choose = true;

				// Function on confirm
				if (settings.onConfirm)
				{
					if (settings.onConfirm.call(target[0]) === false)
					{
						call = false;
					}
				}

				$(this).closest('.modal').modal('hide');


				// Run original event
				if (call)
				{
					_runDefault(target);
				}

				// Should the element remind confirmation?
				if (settings.remind)
				{
					target.data('confirmed', true);
				}
			};

			// Function on cancel button
			if (settings.cancel)
			{
				cancelFunc = function()
				{
					// Mark as done
					choose = true;

					// Function on cancel
					if (settings.onCancel)
					{
						settings.onCancel.call(target[0]);
					}

					// Remove message
					$(this).closest('.modal').modal('hide');
				};
			}
			
			//modal
			montador = $('<div class="modal" id="myModal"></div>');
			modal = $('<div class="modal-dialog modal-sm"><div class="modal-content"></div></div>');
			content = $('<div class="modal-content"></div>'); 
			//modal_header = $('<div class="modal-header"><button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button></div>');
			//content.append(modal_header);
			modal_body = $('<div class="modal-body"></div>');
			modal_body.append(settings.message);
			content.append(modal_body);
			modal_footer = $('<div class="modal-footer"></div>');
			// Buttons
			buttons = {};

			// Cancel button - after
			if (settings.cancel && settings.cancelFirst)
			{
				bt_cancelar = $('<button type="button" class="btn btn-default" data-dismiss="modal">' + settings.cancelText + '</button>');
				modal_footer.append(bt_cancelar);
			}

			// Confirm
			bt_confirmar = $('<button type="button" class="btn btn-primary">' + settings.confirmText + '</button>');
			bt_confirmar.click(confirmFunc);
			modal_footer.append(bt_confirmar);
			content.append(modal_footer);
			modal.append(content);
			montador.append(modal);
			// Open modal
			montador.modal('toggle');
				});
	};

	/**
	 * Run the target default action
	 * @param jQuery target the target element
	 * @return void
	 */
	function _runDefault(target)
	{
		var actions = $.confirmar.defaults.actions,
		name;

		// Run through actions
		for (name in actions)
		{
			if (actions.hasOwnProperty(name) && typeof actions[name] === 'function' && target.is(name))
			{
				actions[name](target);
				return;
			}
		}

		// Not found
		//console.log('No default action specified for this target ('+target[0].nodeName+')');
	}

	/**
	 * Confirmation defaults
	 * @var object
	 */
	$.confirmar.defaults = $.fn.confirmar.defaults = {
			/**
			 * Default message
			 * @var string
			 */
			message: 'Você tem certeza disso?',

			/**
			 * Text of confirm button
			 * @var string
			 */
			confirmText: 'Sim',

			/**
			 * Classes of confirm button
			 * @var string
			 */
			confirmClasses: [],

			/**
			 * Display cancel button?
			 * @var boolean
			 */
			cancel: true,

			/**
			 * Text of cancel button
			 * @var string
			 */
			cancelText: 'Cancelar',

			/**
			 * Classes of cancel button
			 * @var string
			 */
			cancelClasses: [],

			/**
			 * Display cancel button before confirm
			 * @var boolean
			 */
			cancelFirst: true,

			/**
			 * Use tooltip (true) or confirm (false)
			 * @var boolean
			 */
			tooltip: true,

			/**
			 * Tooltip options
			 * @var object
			 */
			tooltipOptions: {},

			/**
			 * Confirm once or every time?
			 * @var boolean
			 */
			remind: false,

			/**
			 * Default actions depending on node type
			 * This list can be extended with further selectors and functions: $.extend($.confirm.defaults.actions, { selector: function(target) { ... } })
			 * @var object
			 */
			actions: {

				// Links
				'a': function(target)
				{
					document.location.href = target[0].href;
				},

				// Submit buttons
				'[type="submit"]': function(target)
				{
					target.closest('form').submit();
				}

			},

			/**
			 * Callback when message is shown: function(modalOrTooltip)
			 * Scope: the target element
			 * @var function
			 */
			onShow: null,

			/**
			 * Callback when confirm
			 * Note: the function may return false to prevent the target's default action (ie: opening a link)
			 * Scope: the target element
			 * @var function
			 */
			onConfirm: null,

			/**
			 * Callback when cancel (no called if cancel button is disabled)
			 * Scope: the target element
			 * @var function
			 */
			onCancel: null,

			/**
			 * Callback when message is removed (with or without active confirmation)
			 * Scope: the tooltip/modal
			 * @var function
			 */
			onRemove: null,

			/**
			 * Callback when the user closes the confirmation without make a choice (for instance, click outside the tooltip)
			 * Scope: the target element
			 * @var function
			 */
			onAbort: null
	};

	// Event binding
	doc.on('click', '.confirm', function(event)
			{
		// Prevent default
		event.preventDefault();
		event.stopPropagation();

		// Show confirmation
		$(this).confirm();
			});

		})(jQuery, document);