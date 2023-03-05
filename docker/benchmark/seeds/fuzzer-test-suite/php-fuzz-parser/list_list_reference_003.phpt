<?php
$arr = [1, 2];
function no_ref($a) {
    return $a;
}

function no_ref_by_ref(&$a) {
    return $a;
}

function &ref_return(&$a) {
    return $a;
}

function &ref_return_global() {
    global $arr;
    return $arr;
}

$a = [1, 2];
[&$var] = no_ref($a);
var_dump($var);
var_dump($a);

$a = [1, 2];
[&$var] = no_ref_by_ref($a);
var_dump($var);
var_dump($a);

$a = [1, 2];
[&$var] = ref_return($a);
var_dump($var);
var_dump($a);

[,&$var] = ref_return_global();
var_dump($var);
var_dump($arr);
?>