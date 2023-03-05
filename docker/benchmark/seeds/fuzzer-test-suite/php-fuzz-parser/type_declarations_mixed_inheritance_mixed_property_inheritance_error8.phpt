<?php

class Foo
{
    public bool|int|float|string|array|object|null $property1;
}

class Bar extends Foo
{
    public mixed $property1;
}

?>