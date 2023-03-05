<?php

class Test {
    public int $i;
    public string $s;
}

$test = new Test;
var_dump($test->i = "42");
var_dump($test->s = 42);

?>