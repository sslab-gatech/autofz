<?php

spl_autoload_register(function($class) {
    class X extends B {}
});

try {
    class B extends A {
    }
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>