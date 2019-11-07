xquery version "3.0";

module namespace funcs = "com.funcs.my.index";

(:recebe id de um interesse, retorna nome, tipo, municipio, distrito, falta imagem:)
declare function funcs:interesse ($id as xs:integer) as element()* {
  for $i in doc('portugal')//interesse
  where $i/idinteresse = $id
  let $n := $i/ancestor::distrito
  let $m := $i/ancestor::municipio/nomeconcelho
  let $interesse := ($i/nome, $i/tipo, $m, $n/nomedistrito)
  return <interesse>{$interesse}</interesse>
};
(:<interesse>{local:interesse("1")}</interesse>:)

(:recebe um id de um distrito e retorna os seus interesses:)
declare function funcs:interesseDist($id as xs:integer) as element()*{
  for $i in doc('portugal')//distrito
  where $i/iddistrito = $id
  let $interesse := $i//interesse
  return<interesse>{$interesse}</interesse>
};


(:recebe id do distrito retorna toda a info perguntar como quer que retorne a info:)
declare function funcs:distrito($id as xs:integer) as element()*{
  for $i in doc('portugal')//distrito
  where $i/iddistrito = $id
  let $numpop := sum($i//populacao)
   let $areatotal := sum($i//area)
  let $densidadepop := $numpop div $areatotal
  return <distrito>{ <numpopulacao>{$numpop}</numpopulacao>, <areatotal>{$areatotal}</areatotal>, <densidadedistrito>{$densidadepop}</densidadedistrito>, $i/iddistrito, $i/nomedistrito, $i/imagemdistrito, $i/municipios}</distrito>
};

declare function funcs:interesses($tipo as xs:string) as element()*{
  <interesses>{
  for $i in doc('portugal')//interesse
  where contains($i/tipo,$tipo)
  let $n := $i/ancestor::distrito
  let $m := $i/ancestor::municipio/nomeconcelho
  let $o := $i/ancestor::municipio/regiao
  order by $i/nome
  return <interesse>{$i/nome, $i/tipo, $m, $n/nomedistrito,$o, $i/idinteresse}</interesse>
  }</interesses>
};

(:recebe um id de um municipio e retorna os seus interesses:)
declare function funcs:interesseMunicipio($id as xs:integer) as element()*{
  for $i in doc('portugal')//municipio
  where $i/idmunicipio = $id
  let $interesse := $i//interesse
  return<interesse>{$interesse}</interesse>
};

(:declare
updating function funcs:add($id as xs:integer, $nome as xs:string, $tipo as xs:string){
for $i in doc("portugal.xml")//municipio
let $lastid := $i//idinteresse[last()]
where $i/idmunicipio = $id
return( if (exists($i/interesses)) then (
  insert node
<interesse>
  <idinteresse>$lastid+1</idinteresse>,
  <nome>$nome</nome>,
  <tipo>$tipo</tipo>
</interesse>
as last into $i/interesses
)
else (
  insert node
<interesses>
 <interesse>
   <idinteresse>$lastid+1</idinteresse>,
  <nome>$nome</nome>,
  <tipo>$tipo</tipo>
 </interesse>
</interesses> into $i ))
};:)

declare updating function funcs:deleteinteresse($id as xs:integer){
  for $i in doc('portugal')//interesses
  where $i/interesse/idinteresse = $id
  return delete node $i/interesse
};

declare updating function funcs:editarnome($id as xs:integer, $nome as xs:string){
  for $i in doc('portugal')//interesses
  where $i/idinteresse = $id
  return replace node $i/interesse/nome/text() with $nome 
};

declare updating function funcs:editartipo($id as xs:integer, $tipo as xs:string){
  for $i in doc('portugal')//interesses
  where $i/idinteresse = $id
  return replace node $i/interesse/tipo/text() with $tipo 
};