<?php

spl_autoload_register(function($class) {
    if ($class === 'A') {
        class A {
            public function method() : C {}
        }
    } else if ($class == 'B') {
        class B extends A {
            public function method() : B {}
        }
    } else {
        class C extends B {
        }
    }
});

$b = new B;

?>