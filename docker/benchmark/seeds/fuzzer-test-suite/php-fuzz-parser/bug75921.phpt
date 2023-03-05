<?php

try {
    $null->a = 42;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($null);
unset($null);

try {
    $null->a['hello'] = 42;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($null);
unset($null);

try {
    $null->a->b = 42;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($null);
unset($null);

try {
    $null->a['hello']->b = 42;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($null);
unset($null);

try {
    $null->a->b['hello'] = 42;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($null);
unset($null);

?>