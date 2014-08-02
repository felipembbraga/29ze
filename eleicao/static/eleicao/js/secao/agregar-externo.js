$(document).ready(function(){
	var secao = new Secao();
	
	$('#id_local').change(function(event){
		$('#id_secao option:gt(0)').remove();
		if($(this).val()==''){
			$('#id_secao').prop('disabled', true);
			return;
		}
		secao.selecionarSecoes($(this).val(), $('#id_secao'));
		$('#id_secao').prop('disabled', false);
	});
	$('#id_local').trigger('change');
	
});