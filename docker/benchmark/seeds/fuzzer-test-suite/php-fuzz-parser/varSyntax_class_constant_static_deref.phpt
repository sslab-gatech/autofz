<?php

class Test {
    const NAME = 'Test2';
}

class Test2 {
    const FOO = 42;
    public static $foo = 42;

    public static function foo() {
        return 42;
    }
}

var_dump(Test::NAME::FOO);
var_dump(Test::NAME::$foo);
var_dump(Test::NAME::foo());

?>