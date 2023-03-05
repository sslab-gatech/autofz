<?php

function test1() {
    $a = [1, 2];
    $c =& $a;
    list($c, $b) = $a;
    var_dump($a, $b);
}

function test2() {
    $a = [1, 2];
    $_a = "a";
    list($$_a, $b) = $a;
    var_dump($a, $b);
}

test1();
test2();

?>