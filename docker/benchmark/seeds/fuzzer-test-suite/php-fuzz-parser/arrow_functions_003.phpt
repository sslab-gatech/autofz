<?php

$a = 1;
$var = "a";
$fn = fn() => $$var;
var_dump($fn());

${5} = 2;
$fn = fn() => ${5};
var_dump($fn());

?>