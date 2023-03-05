<?php

interface I {
    public function test(): iterable|false;
}

class C implements I {
    public function test(): iterable|false {
        yield;
    }
}

var_dump((new C)->test());

?>