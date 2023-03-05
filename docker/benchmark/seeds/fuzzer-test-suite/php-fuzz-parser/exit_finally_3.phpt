<?php

// TODO: In the future, we should execute the finally block.

function test() {
    try {
        exit("Exit\n");
    } finally {
        return 42;
    }
}
var_dump(test());

?>