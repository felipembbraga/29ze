/* Tecnoplace - 2012 */

var notifyAtual = 0;

var themeDict = {
		'erro':'alert-danger',
		'sucesso': 'alert-success',
		'aviso': 'alert-warning',
		'carregando': 'alert-info'
};

jQuery.notify = function (settings)
{	
	// Default
	var config = {
            'theme': 'aviso',
            'title': 'Erro',
            'list': '',
            'redirect_url': '',
            'time': 3000,
            'click': true
        };
	
    if (settings){ $.extend(config, settings); }
    
    // Caso seja para redirecionar
    if (config.redirect_url) {
    	document.location.href = config.redirect_url;
    	return false;
    }
    
        
    // Verifica se o container principal está criado
    if (parent.$('.tecno_notify_main').length == 0)
    	parent.$('body').append($('<div></div>').attr('class', 'tecno_notify_main'));
    
    // Adiciona o container para exibição de mensagem
    parent.$('.tecno_notify_main').append($('<div></div>').attr('id', 'tecno_notify' + notifyAtual)
    								 			   .attr('class', 'notify alert ' + themeDict[config.theme])
    								 			   .append($('<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'))
    								 			   .append($('<div></div>').append($('<div></div>').attr('class', 'image'))
    										 				 			   .append($('<strong></strong>').attr('class', 'title').text(config.title)))						 						 				   
			    								   .append('<br style="clear: both" />')
			    								   .hide());
    
    // Adiciona lista, caso tenha sido passado
    if ($.isArray(config.list))
    {
    	parent.$('#tecno_notify' + notifyAtual).append('<ul></ul>');
    	
    	$.each(config.list, function(index, valor){
    		
    		parent.$('#tecno_notify' + notifyAtual + ' ul').append($('<li></li>').text(valor));
    	});
    }    
    
    // Mostra o notify com efeito
    parent.$('#tecno_notify' + notifyAtual).slideDown('fast');
    
    // Define o tempo para o aviso ser removido. "-1" não remove o aviso
    if (config.time >= 0)
    	parent.setTimeout('$.notify.destroy(' + notifyAtual + ')', config.time);
    
    notifyAtual++;
    
    return notifyAtual-1;
}


// Remove o container do aviso
jQuery.notify.destroy = function (atual)
{	
	// Oculta caso o objeto esteja criado
	if (parent.$('#tecno_notify' + atual).length > 0){
		parent.$('#tecno_notify' + atual).slideUp('fast', function() { $(this).remove() });
	}
}