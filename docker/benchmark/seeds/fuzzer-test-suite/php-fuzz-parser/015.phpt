<?php

var_dump(trigger_error("error"));

try {
    var_dump(trigger_error("error", -1));
} catch (\ValueError $e) {
    echo $e->getMessage() . \PHP_EOL;
}
try {
    var_dump(trigger_error("error", 0));
} catch (\ValueError $e) {
    echo $e->getMessage() . \PHP_EOL;
}

var_dump(trigger_error("error", E_USER_WARNING));
var_dump(trigger_error("error", E_USER_DEPRECATED));

?>