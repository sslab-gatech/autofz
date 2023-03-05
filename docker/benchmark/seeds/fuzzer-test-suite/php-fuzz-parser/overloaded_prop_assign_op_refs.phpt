<?php

class Test {
    protected $a = 0;
    protected $b = 0;
    protected $c = 0;

    public function &__get($name) {
        echo "get($name)\n";
        return $this->$name;
    }

    public function __set($name, $value) {
        echo "set($name, $value)\n";
    }
}

$test = new Test;

var_dump($test->a += 1);
var_dump($test->b++);
var_dump(++$test->c);

var_dump($test);

?>