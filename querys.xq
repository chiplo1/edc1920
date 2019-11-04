xquery version "3.0";

module namespace funcs = "com.funcs.my.index";

(:recebe id de um interesse, retorna nome, tipo, municipio, distrito, falta imagem:)
declare function funcs:interesse ($id as xs:integer) as element()* {
  for $i in doc("portugal.xml")//interesse
  where $i/idinteresse = $id
  let $n := $i/ancestor::distrito
  let $m := $i/ancestor::municipio/nomeconcelho
  let $interesse := ($i/nome, $i/tipo, $m, $n/nomedistrito)
  return <interesse>{$interesse}</interesse>
};
(:<interesse>{local:interesse("1")}</interesse>:)

(:recebe id do distrito retorna toda a info perguntar como quer que retorne a info:)
declare function funcs:distrito($id as xs:integer) as element()*{
  for $i in doc("portugal.xml")//distrito
  where $i/iddistrito = $id
  return $i 
};
(:<distrito>{local:distrito("2")}</distrito>:)

