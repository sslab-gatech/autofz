<?php

spl_autoload_register(function($class) {
    if ($class === 'A') {
        class A {
            public function method() : B {}
        }
        var_dump(new A);
    } else if ($class == 'B') {
        class B extends A {
            public function method() : C {}
        }
        var_dump(new B);
    } else {
        class C extends B {
        }
        var_dump(new C);
    }
});

// Same as autoload1 test case, but with a different autoloading root
var_dump(new B);

?>