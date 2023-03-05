<?php

// Same as autoload_error1, but for argument types.
spl_autoload_register(function($class) {
    if ($class === 'A') {
        class A {
            public function method(B $x) {}
        }
    } else if ($class == 'B') {
        class B extends A {
            public function method(C $x) {}
        }
    } else {
        class C extends B {
        }
    }
});

$b = new B;
$c = new C;

?>