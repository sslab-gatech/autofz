<?php

function foo($foo, int ...$bar) {}

try {
    foo(1, []);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    foo(1, 1, 1, []);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}
