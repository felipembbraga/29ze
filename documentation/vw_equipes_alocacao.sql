CREATE OR REPLACE VIEW vw_equipes_alocacao AS
 SELECT e.id AS equipe_id,
    e.eleicao_id,
    ( SELECT ( SELECT sum(veiculos_alocacao.quantidade) AS sum
                   FROM veiculos_alocacao
                  WHERE veiculos_alocacao.equipe_id = e.id) AS sum) AS total_estimativa,
    ( SELECT ( SELECT sum(va.quantidade) AS sum
                   FROM veiculos_alocacao va
                     JOIN veiculos_perfilveiculo vpv ON va.perfil_veiculo_id = vpv.id AND vpv.perfil_equipe = true
                  WHERE va.equipe_id = e.id) AS sum) AS estimativa_equipe,
    ( SELECT ( SELECT sum(va.quantidade) AS sum
                   FROM veiculos_alocacao va
                     JOIN veiculos_perfilveiculo vpv ON va.perfil_veiculo_id = vpv.id AND vpv.perfil_equipe = false
                  WHERE va.equipe_id = e.id) AS sum) AS estimativa_local,
    ( SELECT count(*) AS count
           FROM veiculos_veiculoalocado
          WHERE veiculos_veiculoalocado.equipe_id = e.id) AS veiculos_alocados,
    ( SELECT count(vva.*) AS count
           FROM veiculos_veiculoalocado vva
             JOIN veiculos_perfilveiculo vpv ON vva.perfil_id = vpv.id AND vpv.perfil_equipe = true
          WHERE vva.equipe_id = e.id) AS veiculos_alocados_equipe,
    ( SELECT count(vva.*) AS count
           FROM veiculos_veiculoalocado vva
             JOIN veiculos_perfilveiculo vpv ON vva.perfil_id = vpv.id AND vpv.perfil_equipe = false
          WHERE vva.equipe_id = e.id) AS veiculos_alocados_local
   FROM eleicao_equipe e
  WHERE ((( SELECT ( SELECT sum(veiculos_alocacao.quantidade) AS sum
                   FROM veiculos_alocacao
                  WHERE veiculos_alocacao.equipe_id = e.id) AS sum)) - (( SELECT count(*) AS count
           FROM veiculos_veiculoalocado
          WHERE veiculos_veiculoalocado.equipe_id = e.id))) > 0;

ALTER TABLE vw_equipes_alocacao
  OWNER TO zona_eleitoral;