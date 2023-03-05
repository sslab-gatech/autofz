<?php
trait Foo{
    private int $baz;
}

class Baz{
    use Foo;

    function get(){
        return $this->baz;
    }
}

var_dump((new Baz)->get());