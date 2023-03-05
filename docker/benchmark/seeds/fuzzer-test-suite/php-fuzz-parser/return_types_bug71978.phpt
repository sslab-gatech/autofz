<?php
class A1 {
    function foo(int $a): int {}
}
class B1 extends A1 {
    function foo(string $a): int {}
}
?>