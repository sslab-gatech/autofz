<?php

class Test {
    public static $test;

    public static function method() {
        static $foo;
        $foo = [&$foo];
    }
}

function test() {
    static $foo;
    $foo = [&$foo];
}

$foo = [&$foo];
Test::$test = $foo;
test();
Test::method();

?>
===DONE===