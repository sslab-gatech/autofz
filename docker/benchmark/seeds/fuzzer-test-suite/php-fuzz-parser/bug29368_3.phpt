<?php
class Foo {
    function __construct() {
        echo __METHOD__ . "\n";
    }
    function __destruct() {
        echo __METHOD__ . "\n";
    }
}
class Bar {
    function __construct() {
        echo __METHOD__ . "\n";
        throw new Exception;
    }
    function __destruct() {
        echo __METHOD__ . "\n";
    }
}

try {
    new Foo() + new Bar();
} catch(Exception $exc) {
    echo "Caught exception!\n";
}
?>