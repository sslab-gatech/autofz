<?php

function test() {
    try {
        ((string) 'extract')(['a' => 42]);
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }
}
test();

?>