<?php
function change(&$ref) {
    $ref = range(1, 10);
    return;
}

$array = [1];
change(list($val) = $array);
var_dump($array);
?>