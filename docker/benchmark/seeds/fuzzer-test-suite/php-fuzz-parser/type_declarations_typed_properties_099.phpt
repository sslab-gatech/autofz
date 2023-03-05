<?php

class Test {
    public array $ary = [];
}

$test = new Test;
foreach ($test->ary as &$value) {}
var_dump($test);

?>