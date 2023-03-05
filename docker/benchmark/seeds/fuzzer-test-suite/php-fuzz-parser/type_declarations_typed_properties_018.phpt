<?php
class Foo {
    public int $bar,
                $qux;
}

$reflector = new ReflectionClass(Foo::class);

$prop = $reflector->getProperty("qux");

var_dump($prop->getType()->getName());
?>