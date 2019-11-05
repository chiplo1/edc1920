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

(:recebe um id de um distrito e retorna os seus interesses:)
declare function funcs:interesseDist($id as xs:integer) as element()*{
  for $i in doc("portugal.xml")//distrito
  where $i/iddistrito = $id
  let $interesse := $i//interesse
  return<interesse>{$interesse}</interesse>
};


(:recebe id do distrito retorna toda a info perguntar como quer que retorne a info:)
declare function funcs:distrito($id as xs:integer) as element()*{
  for $i in doc("portugal.xml")//distrito
  where $i/iddistrito = $id
  let $numpop := sum($i//populacao)
   let $areatotal := sum($i//area)
  let $densidadepop := $numpop div $areatotal
  return <distrito>{ <numpopulacao>{$numpop}</numpopulacao>, <areatotal>{$areatotal}</areatotal>, <densidadedistrito>{$densidadepop}</densidadedistrito>, $i/iddistrito, $i/nomedistrito, $i/imagemdistrito, $i/municipios}</distrito>
};
