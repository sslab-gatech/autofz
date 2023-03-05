<?php

function gen() {
    f();
    yield;
}

function f() {
    exit('Done');
}

$gen = gen();
$gen->current();

?>