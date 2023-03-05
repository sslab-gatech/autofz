<?php

spl_autoload_register(function($class) {
    echo new ReflectionClass(A::class), "\n";
});

class A implements I {
}

?>