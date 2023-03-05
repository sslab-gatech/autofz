<?php

try {
    var_dump(func_get_arg(1));
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}

function bar() {
    var_dump(func_get_arg(1));
}

function foo() {
    bar(func_get_arg(1));
}

try {
    foo(1,2);
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}

?>