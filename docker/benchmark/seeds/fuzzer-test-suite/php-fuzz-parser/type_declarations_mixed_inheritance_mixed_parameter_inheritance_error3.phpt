<?php

class Foo
{
    public function method(mixed $a) {}
}

class Bar extends Foo
{
    public function method(bool|int|float|string|array|object|null $a) {}
}

?>