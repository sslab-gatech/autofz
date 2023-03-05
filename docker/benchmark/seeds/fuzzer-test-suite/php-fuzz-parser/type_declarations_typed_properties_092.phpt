<?php

function &ref(&$foo) {
    return $foo;
}

class Test {
    public array $prop;
    public int $prop2;

    public function foo() {
        $array = [];
        $ref =& $array;
        $this->prop = $array;
    }

    public function bar() {
        $str = "123";
        $this->prop2 = ref($str);
    }
}

$test = new Test;
$test->foo();
$test->foo();
$test->bar();
$test->bar();
var_dump($test);

?>