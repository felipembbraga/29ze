var Secao = function(){
	
	this.url_root = BASE_URL + '/eleicao/secao';
	this.idSecao = null;
	
	this.setIdSecao = function(id){
		this.idSecao = id;
	};
	
	this.agregarSecoes = function() {
		var url = this.url_root + '/agregar/';
		$.ajax({
			type: 'POST',
		    url: url,
		    data: $('#form-agregar-secoes').serialize() + '&id-local=' + $('#form-agregar-secoes').data('id-local'),
		    success: function(resultado) {
		    	$.notify(resultado);
		    	if(resultado.theme=='sucesso')
		    		location.href = location.href;
		    	
			},
			error: function(elemento, status, erro){
				$.notify({theme:'erro', title:status, list: new Array(erro)});
			}
		});
	};
	
	this.desagregarSecao = function() {
		var url = this.url_root + '/desagregar/' + this.idSecao + '/';
		$.ajax({
			type: 'POST',
		    url: url,
		    			
		    success: function(resultado) {
		    	$.notify(resultado);
		    	if(resultado.theme=='sucesso')
		    		location.href = location.href;
			},
			error: function(elemento, status, erro){
				$.notify({theme:'erro', title:status, list: new Array(erro)});
			}
		});
	};
	
}