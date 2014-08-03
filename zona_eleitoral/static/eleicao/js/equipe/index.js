$(document).ready(function(){
	var equipe = new Equipe();
	$('.delete').click(function(event){
		
		$(this).confirmar({
			message: "Você deseja excluir esta equipe?",
			onConfirm: function() {
				equipe.setIdEquipe($(this).data('id'));
				equipe.excluirEquipe();
			}
		})
	});
});