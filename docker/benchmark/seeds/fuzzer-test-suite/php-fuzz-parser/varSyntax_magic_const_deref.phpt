<?php

function test() {
    var_dump(__FUNCTION__[0]);
    var_dump(__FUNCTION__->prop);
    try {
        __FUNCTION__->method();
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
}

test();

?>