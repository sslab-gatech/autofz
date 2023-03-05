<?php

class Test {
    private int $prop;

    public function __get($name) {
        return "foobar";
    }
}

$test = new Test;
var_dump($test->prop);

?>