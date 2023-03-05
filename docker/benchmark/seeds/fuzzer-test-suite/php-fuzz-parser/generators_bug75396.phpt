<?php

$gen = (function () {
    yield 42;

    try {
        echo "Try\n";
        exit("Exit\n");
    } finally {
        echo "Finally\n";
    }
})();

$gen->send("x");

?>