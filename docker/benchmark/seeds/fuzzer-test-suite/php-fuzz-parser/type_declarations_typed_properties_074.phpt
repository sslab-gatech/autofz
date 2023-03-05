<?php

class Test {
    public $prop = "x";
    public int $val;

    public function &__get($name) {
        return $this->prop;
    }
}

$test = new Test;
$dummyRef = &$test->prop;
unset($test->val);
var_dump($test);
try {
    var_dump($test->val);
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump($test);

$test->prop = "y";
var_dump($test->prop);

?>