var BASE_URL;
var notifyLoading;
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

String.prototype.rjust = function(width, char) {
	s = this;
	
	while(s.length < width)
		s = char + s;
	return s;
}
$(document).ready(function(){
	
	BASE_URL = $('body').data('base-url');
	
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	
	$(document).ajaxStart(function(){
		notifyLoading = $.notify({
			'theme': 'carregando',
			'title': 'Aguarde...',
			'time': -1
		});	
	});
	$(document).ajaxStop(function() {
		$.notify.destroy(notifyLoading);
	});

	$('.date').mask('99/99/9999');
    $('.time').mask('99:99');
	$('.telefone').mask('(99)9999-9999');
	$('.tooltip-iniciar').tooltip({html:true,placement:'top'});
	
});

function abrirModal(url) {
	$.bsmodal({remote:url});
}
