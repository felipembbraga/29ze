function default_callback(data){
    $.unblockUI();
    Dajax.process(data);
    aplica_mascaras();
}

function block_screen(){
    $.blockUI({ message: '<img src="/static/veiculos/img/loader.gif"/> <div class="loading-blockui">Processando...<br>Um momento por favor.</div>',
                css: { 'z-index': '9991', 'border-radius': '10px', 'border-color': '#D1D1D1'},
                overlayCSS: { 'z-index': '9990', 'background-color': '#F7F7F7'} });
}

function requisitar_veiculo(){
    block_screen();
    var turno = false;
    if (parseInt($('#turno').val()) > 0)
        turno = true;
    Dajaxice.veiculos.requisitar_veiculo(default_callback, {'placa':$('#placa-veiculo').val(), 'turno': turno});
}

function add_veiculo(formulario){
    $('#modal-novo-veiculo').modal('hide');
    block_screen();
    var turno = false;
    if (parseInt($('#turno').val()) > 0)
        turno = true;
    Dajaxice.veiculos.cadastrar_veiculo(default_callback, {'placa':$('#placa-veiculo').val(), 'formulario': formulario, 'turno': turno});
}

function buscar_placa(val){
    var error = $('#error-field-busca-placa');
    if (val != '') {
        block_screen();
        error.hide();
        var turno = false;
        if (parseInt($('#turno').val()) > 0)
            turno = true;
        Dajaxice.veiculos.consultar_veiculo(default_callback, {'placa': val, 'turno': turno});
    }else{
        error.show();
        error.html('Informe um valor válido!');
    }
}

function change_marca(val){
    block_screen();
    Dajaxice.veiculos.change_marca(default_callback, {'marca': val});
}

function change_motorista(val){
    block_screen();
    var turno = false;
    if (parseInt($('#turno').val()) > 0)
        turno = true;
    Dajaxice.veiculos.consulta_motorista(default_callback, {'id_motorista': val, 'turno': turno});
}

function salva_vistoria(val){
    block_screen();
    var turno = false;
    if (parseInt($('#turno').val()) > 0)
        turno = true;

    var alocacao_2_turno = false;
    if ($('#id_alocacao_2_turno').is(':checked'))
        alocacao_2_turno = true;
    Dajaxice.veiculos.cadastrar_vistoria(default_callback, {'formulario': val, 'turno': turno, 'alocacao_2_turno': alocacao_2_turno});
}

function desalocar_veiculo(val){
    block_screen();
    var turno = false;
    if (parseInt($('#turno').val()) > 0)
        turno = true;
    Dajaxice.veiculos.desalocar_veiculo(default_callback, {'id_veiculo': $('#id_veiculo_alocado').val(), 'exibe_vistoria': true, 'turno': turno})
}

function aplica_mascaras(){
	$('input[id*="placa"]').mask('aaa-9999');
}

function nova_busca(modal){
    $.unblockUI();
    if (modal)
        modal.modal('hide');

    var field_placa = $('#placa-veiculo');
    field_placa.val('');
    field_placa.focus();
}

function outro_motorista(){
    var motorista_sl2 = $('#s2id_id_motorista');
    motorista_sl2.find('span.select2-chosen').html('Selecione uma equipe');
    motorista_sl2.removeClass('select2-allowclear');
    $('#id_titulo_eleitoral').val('');
    $('#id_nome').val('');
    $('#id_endereco').val('');
    $('#id_id').val('');
    $('#id_motorista').val('');
    $('#modal-requisitar-motorista').modal('hide');
}

function alocacao_por_equipe(e){
    var div_alocacao = $('#alocacao-por-equipe');
    var choice_alocacao_man = $('#choice-alocacao-manual');
    if (e == '1') {
        div_alocacao.show();
        choice_alocacao_man.hide()
    }else{
        div_alocacao.hide();
        choice_alocacao_man.show()
    }
}

function alocacao_manual(e){
    var div_equipe_manual = $('#div-equipe-manual');
    var equipe_manual_sl2 = $('#s2id_id_equipe_manual');
    var equipe_manual = $('#id_equipe_manual');
    var local_manual_sl2 = $('#s2id_id_local_manual');
    var local_manual = $('#id_local_manual');
    var perfil_manual_sl2 = $('#s2id_id_perfil_manual');
    var perfil_manual = $('#id_perfil_manual');
    if (e) {
        div_equipe_manual.show();
    }else{
        div_equipe_manual.hide();
        equipe_manual_sl2.find('span.select2-chosen').html('Selecione uma equipe');
        equipe_manual_sl2.removeClass('select2-allowclear');
        equipe_manual.val('');
        local_manual_sl2.find('span.select2-chosen').html('Selecione um local');
        local_manual_sl2.removeClass('select2-allowclear');
        local_manual.val('');
        perfil_manual_sl2.find('span.select2-chosen').html('Selecione uma função');
        perfil_manual_sl2.removeClass('select2-allowclear');
        perfil_manual.val('');
    }
}

function alocacao_2_turno(e){
    var div_dados_1_turno = $('#detalhes_alocacao_1_turno');
    var div_dados_alocacao = $('#dados_alocacao');
    if (e) {
        div_dados_alocacao.show();
        div_dados_1_turno.hide();
    }else{
        div_dados_alocacao.hide();
        div_dados_1_turno.show();
    }
}

$(document).ready(function(){
    aplica_mascaras();

    $('body').on('change', '#id_marca', function() {
        change_marca($(this).val());
    });

    $('body').on('change', '#turno', function() {
        $('#message-status').hide();
        var vistoria = $('#cadastrar-vistoria');
        vistoria.hide();
        vistoria.find('.panel-body').html('');
        var field_placa = $('#placa-veiculo');
        field_placa.focus();
    });

    $('body').on('change', '#id_alocacao', function() {
        alocacao_por_equipe($(this).val());
    });

    $('body').on('change', '#id_motorista', function() {
        if ($(this).val())
            change_motorista($(this).val());
        else{
            $('#id_titulo_eleitoral').val('');
            $('#id_nome').val('');
            $('#id_endereco').val('');
            $('#id_id').val('');
        }
    });

    $('body').on('click', '#id_alocacao_manual', function() {
        alocacao_manual($(this).is(':checked'));
    });

    $('body').on('click', '#id_alocacao_2_turno', function() {
        alocacao_2_turno($(this).is(':checked'));
    });

    $('#placa-veiculo').keypress(function(event){
        if(event.keyCode == 13)
            buscar_placa($(this).val());
    });
});
