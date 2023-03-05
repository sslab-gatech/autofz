<?php

function test() {
    $i = 1;
    try {
        array_map('extract', [['i' => new stdClass]]);
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }
    $i += 1;
    var_dump($i);
}
test();

?>