<?php
$foo = new class {
    public int $bar = 10, $qux;
};

var_dump($foo);