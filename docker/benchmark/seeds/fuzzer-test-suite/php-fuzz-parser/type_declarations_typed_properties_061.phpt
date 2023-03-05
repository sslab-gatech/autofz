<?php

$a = new class {
    public int $foo = 1;

    function &__get($x) {
        return $this->foo;
    }

    function __set($x, $y) {
        echo "set($y)\n";
    }
};

$a->_ += 1;
var_dump($a->foo);

$a->_ .= "1";
var_dump($a->foo);

$a->_ .= "e50";
var_dump($a->foo);

$a->_--;
var_dump($a->foo);

--$a->_;
var_dump($a->foo);

$a->foo = PHP_INT_MAX;

$a->_++;
var_dump($a->foo);

++$a->_;
var_dump($a->foo);

?>