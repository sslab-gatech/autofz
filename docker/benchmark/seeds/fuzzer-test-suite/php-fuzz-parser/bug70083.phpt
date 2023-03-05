<?php

class foo {
    private $var;
    function __get($e) {
        return $this;
    }
}

function &noref() { $foo = 1; return $foo; }

$foo = new foo;
try {
    $foo->i = &noref();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($foo);

?>