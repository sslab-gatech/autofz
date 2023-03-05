<?php

class A {
    function test(): B {}
}
class B extends A {}
class C extends B {
    function test(): parent {}
}

?>
===DONE===