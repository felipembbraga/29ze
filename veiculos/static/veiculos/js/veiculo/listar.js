function requisicaoVeiculo(id_veiculo) {
    $('#modal-requisicao-veiculo').modal();
    Dajaxice.veiculos.requisicao_veiculo(Dajax.process, {'id_veiculo':id_veiculo, 'formulario': {}});
}