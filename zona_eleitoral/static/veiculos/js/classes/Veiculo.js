Veiculo = function() {
	this.url_root = BASE_URL + '/veiculos/veiculo';
	this.idVeiculo = null;
	
	this.getModelos = function(id_marca, element) {
		var url = this.url_root + '/get-modelos/' + id_marca + '/';
		$.ajax({
			type: 'POST',
		    url: url,
		    success: function(resultado) {
		    	$.each(resultado, function(i, item){
		    		option = $('<option></option>');
		    		option.val(item.pk);
		    		option.text(item.fields.nome);
		    		element.append(option);
		    	});	
		    			    	
			},
			error: function(elemento, status, erro){
				$.notify({theme:'erro', title:status, list: new Array(erro)});
			}
		});
	};
	
	this.setIdVeiculo = function(idVeiculo) {
		this.idVeiculo = idVeiculo;
	};
	
	this.excluirVeiculo = function(){
		var url = this.url_root + '/excluir/' + this.idVeiculo + '/';
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
};