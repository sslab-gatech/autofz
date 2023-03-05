<?php
class A {
    public B $c;
}

$class = new ReflectionClass(A::class);

$defaults = $class->getDefaultProperties();

var_dump($defaults);
var_dump(array_key_exists('c', $defaults));
?>