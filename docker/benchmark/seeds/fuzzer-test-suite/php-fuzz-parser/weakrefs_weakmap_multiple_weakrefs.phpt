<?php

$obj = new stdClass;

$ref = WeakReference::create($obj);
$map = new WeakMap;
$map[$obj] = 1;
$map2 = new WeakMap;
$map2[$obj] = 1;
$map3 = clone $map2;

var_dump($ref->get(), $map, $map2, $map3);
unset($obj);
var_dump($ref->get(), $map, $map2, $map3);
unset($ref, $map, $map2);

$obj = new stdClass;
$ref = WeakReference::create($obj);
$map = new WeakMap;
$map[$obj] = 1;
$map2 = new WeakMap;
$map2[$obj] = 1;
$map3 = clone $map2;

unset($ref, $map, $map2, $map3);
var_dump($obj);
unset($obj);

?>