<?php

spl_autoload_register(function($class) {
    throw new Exception("Class $class does not exist");
});

class A {}

// Graceful failure allowed
for ($i = 0; $i < 2; $i++) {
    try {
        class B extends A implements I {
        }
    } catch (Exception $e) {
        echo $e->getMessage(), "\n";
    }
}

interface J {}

spl_autoload_register(function($class) {
    // Tie up B in a variance obligation.
    class X {
        public function test(): J {}
    }
    class Y extends X {
        public function test(): B {}
    }
}, true, true);

// Fallback to fatal error, as we can't unlink class B anymore.
try {
    class B extends A implements I, J {
    }
} catch (Exception $e) {
    echo $e->getMessage(), "\n";
}

?>