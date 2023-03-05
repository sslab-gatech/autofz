<?php

function func() {
    return [0];
}

$x = $y =& func();
var_dump($x, $y);

?>