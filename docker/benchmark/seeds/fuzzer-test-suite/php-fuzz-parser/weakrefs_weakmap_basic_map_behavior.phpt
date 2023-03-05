<?php

$map = new WeakMap;
var_dump(count($map));

$obj = new stdClass;
$obj->value = 1;
$obj2 = new stdClass;
$obj2->value = 2;

$map[$obj] = $obj2;
var_dump(count($map));
var_dump($map);
var_dump(isset($map[$obj]));
var_dump(!empty($map[$obj]));
var_dump($map[$obj]);

$map[$obj] = 42;
var_dump($map);
var_dump(isset($map[$obj]));
var_dump(!empty($map[$obj]));
var_dump($map[$obj]);

$map[$obj] = false;
var_dump($map);
var_dump(isset($map[$obj]));
var_dump(!empty($map[$obj]));
var_dump($map[$obj]);

$map[$obj] = null;
var_dump($map);
var_dump(isset($map[$obj]));
var_dump(!empty($map[$obj]));
var_dump($map[$obj]);

unset($map[$obj]);
var_dump($map);
var_dump(isset($map[$obj]));
var_dump(!empty($map[$obj]));
try {
    var_dump($map[$obj]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\nIndirect modification:\n";
$map[$obj] = [];
$map[$obj][] = 42;
$map[$obj2] = 41;
$map[$obj2]++;
var_dump($map);

echo "\nMethods:\n";
var_dump($map->offsetSet($obj2, 43));
var_dump($map->offsetGet($obj2));
var_dump($map->offsetExists($obj2));
var_dump($map->count());
var_dump($map->offsetUnset($obj2));
var_dump($map->count());

?>