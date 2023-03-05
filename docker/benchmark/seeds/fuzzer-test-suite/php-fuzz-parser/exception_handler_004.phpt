<?php

try {
    set_exception_handler("fo");
} catch (\TypeError $e) {
    echo $e->getMessage() . \PHP_EOL;
}
try {
    set_exception_handler(array("", ""));
} catch (\TypeError $e) {
    echo $e->getMessage() . \PHP_EOL;
}

?>