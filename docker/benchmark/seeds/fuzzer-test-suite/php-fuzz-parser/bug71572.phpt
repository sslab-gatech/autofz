<?php

$str = "abc";
try {
    var_dump($str[0] = "");
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}
try {
    var_dump($str[1] = "");
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}
try {
    var_dump($str[3] = "");
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}
try {
    var_dump($str[10] = "");
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}
var_dump($str);
?>