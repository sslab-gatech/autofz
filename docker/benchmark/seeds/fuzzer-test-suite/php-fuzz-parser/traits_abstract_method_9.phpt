<?php

spl_autoload_register(function($class) {
    if ($class == T::class) {
        trait T {
            abstract private function method($x): self;
        }
    } else if ($class == C::class) {
        class C {
            use T;

            private function method($x): D {
                return new D;
            }
        }
    } else if ($class == D::class) {
        class D extends C {}
    }
});

new C;

?>
===DONE===