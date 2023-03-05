<?php

function val() {
    return 42;
}

$var = 24;
$arr = [PHP_INT_MAX => "foo"];
try {
    var_dump($arr[] =& $var);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump(count($arr));
try {
    var_dump($arr[] =& val());
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump(count($arr));

?>