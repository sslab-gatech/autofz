<?php

$map = new WeakMap;

echo "\nEmpty loop:\n";
foreach ($map as $key => $value) {
    var_dump($key, $value);
}

echo "\nSimple loop:\n";
$obj0 = new stdClass;
$obj1 = new stdClass;
$obj2 = new stdClass;
$map[$obj0] = 0;
$map[$obj1] = 1;
$map[$obj2] = 2;
foreach ($map as $key => $value) {
    var_dump($key, $value);
}

echo "\nObject removed during loop:\n";
foreach ($map as $key => $value) {
    if (isset($obj1) && $key === $obj1) unset($obj1);
    var_dump($key, $value);
}

echo "\nBy reference iteration:\n";
foreach ($map as $key => &$value) {
    $value++;
}
var_dump($map);

?>