<?php

class Test {
    private $x;
    public function &__get($name) {
        return $this->x;
    }
}

$test = new Test;
$y = 5;
$test->x =& $y;
var_dump($test->x);

?>