var Equipe = function() {
	this.idEquipe = null;
	this.url_root = BASE_URL + '/eleicao/equipe';
	this.setIdEquipe = function(idEquipe) {
		this.idEquipe = idEquipe;
	};
	
	this.excluirEquipe = function(){
		var url = this.url_root + '/excluir/' + this.idEquipe + '/';
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