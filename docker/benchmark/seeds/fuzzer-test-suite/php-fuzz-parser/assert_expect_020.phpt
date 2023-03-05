<?php
assert(0 && ($a = function () {
    $var = 'test';
    $str = "$var, $var[1], {$var}[], {$var[1]}[], ${var}[], ${var[1]}[]";
}));
?>