

$(document).ready(function(){
	secao = new Secao();
	
	$('.bt-desacoplar').click(function(event){
		$(this).confirmar({
			message: "Você deseja desagregar estas seções?",
			onConfirm: function() {
				secao.setIdSecao($(this).data('secao'));
				secao.desagregarSecao();
			}
		})
	});
	
	$('.bt-excluir').click(function(event){
		$(this).confirmar({
			message: "Você deseja excluir esta seção?",
			onConfirm: function() {
			}
		})
	});
	
	$('#bt-agregar').click(function(event){
		if($('[name=pk_secao]:checked').length<2){
			$.notify({title:'Selecione pelo menos duas seções'});
			return;
		}
		$(this).confirmar({
			message: "Você deseja agregar esta seção?",
			onConfirm: function() {
				secao.agregarSecoes();
			}
		})
	});
	
});