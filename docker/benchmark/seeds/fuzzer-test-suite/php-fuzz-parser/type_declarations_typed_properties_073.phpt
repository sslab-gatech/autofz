<?php

class Test {
    public $prop = "42";
    public int $val;

    public function &__get($name) {
        return $this->prop;
    }
}

$test = new Test;
unset($test->val);
var_dump($test);
var_dump($val = &$test->val);
var_dump($test);

$test->prop = "x";
var_dump($test, $val);

?>