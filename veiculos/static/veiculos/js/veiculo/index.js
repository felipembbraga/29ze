$(document).ready(function(){
	var veiculo = new Veiculo();
	$('.delete').click(function(event) {
		$(this).confirmar({
			message: "Você deseja excluir este veículo?",
			onConfirm: function() {
				veiculo.setIdVeiculo($(this).data('id'));
				veiculo.excluirVeiculo();
			}
		});
	});
});
