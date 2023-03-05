<?php

class Foo
{
    public function method(stdClass|Foo $a) {}
}

class Bar extends Foo
{
    public function method(mixed $a) {}
}

?>