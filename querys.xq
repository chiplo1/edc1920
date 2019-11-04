(:recebe id de um interesse, retorna nome, tipo, municipio, distrito, falta imagem:)
declare function local:interesse ($id as xs:string) as element()* {
  for $i in doc("portugal.xml")//interesse
  where $i/idinteresse = $id
  let $n := $i/ancestor::distrito
  let $m := $i/ancestor::municipio/nomeconcelho
  let $interesse := ($i/nome, $i/tipo, $m, $n/nomedistrito)
  return <interesse>{$interesse}</interesse>
};
(:<interesse>{local:interesse("1")}</interesse>:)

(:recebe id do distrito retorna toda a info:)
declare function local:distrito($id as xs:string) as element()*{
  for $i in doc("portugal.xml")//distrito
  where $i/iddistrito = $id
  return $i 
};
<distrito>{local:distrito("2")}</distrito>

