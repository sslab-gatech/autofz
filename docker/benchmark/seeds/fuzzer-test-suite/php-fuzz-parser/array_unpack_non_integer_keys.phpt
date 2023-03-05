<?php
function gen() {
    yield [] => 1;
    yield 1.23 => 123;
}

try {
    [...gen()];
} catch (Error $ex) {
    echo "Exception: " . $ex->getMessage() . "\n";
}
