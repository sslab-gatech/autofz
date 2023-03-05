<?php

class A {
    function foo(array $a): array {
        return $a;
    }
}

echo new ReflectionClass("A");
?>