<?php

function f($reqParam, $optParam = null, ...$params) {
    var_dump($reqParam, $optParam, $params);
}

f(1);
f(1, 2);
f(1, 2, 3);
f(1, 2, 3, 4);
f(1, 2, 3, 4, 5);

?>