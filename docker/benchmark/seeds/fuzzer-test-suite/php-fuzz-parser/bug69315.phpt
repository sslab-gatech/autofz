<?php

var_dump(function_exists("strlen"));
var_dump(is_callable("strlen"));
try {
    var_dump(strlen("xxx"));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(defined("PHP_VERSION"));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(constant("PHP_VERSION"));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(call_user_func("strlen"));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(is_string("xxx"));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(is_string());
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>