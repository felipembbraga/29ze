

$(document).ready(function(){
	secao = new Secao();
	
	$('.bt-desacoplar').click(function(event){
		$(this).confirmar({
			message: "Você deseja desacoplar estas seções?",
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
		$(this).confirmar({
			message: "Você deseja excluir esta seção?",
			onConfirm: function() {
				secao.agregarSecoes();
			}
		})
	});
	
});